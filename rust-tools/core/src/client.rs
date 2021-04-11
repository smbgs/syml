use serde_json::Value;
use std::io::{BufReader, BufWriter, BufRead, Write};
use std::os::unix::net::UnixStream;

use crate::protocol::{Command, Response, get_socket_path};
use uuid::Uuid;
use std::borrow::Borrow;

pub struct Client {
    pub service_name: String,
    stream: UnixStream,
}

impl Client {

    pub fn new(service_name: &str) -> Client {

        let service_name= String::from(service_name);
        let socket_path = get_socket_path(service_name.borrow());

        let stream = UnixStream::connect(socket_path).unwrap();

        Client {
            service_name: service_name,
            stream: stream,
        }
    }

    pub fn call(&self, mut command: Command) -> Value {

        // TODO: consider low-level usage
        command.cid = Uuid::new_v4().to_string();

        // TODO: move to constructor
        let mut reader =  BufReader::new(self.stream.try_clone().unwrap());
        let mut writer = BufWriter::new(self.stream.try_clone().unwrap());

        let cmd = serde_json::to_string(&command).unwrap();

        let _ = writer.write(cmd.as_ref());
        let _ = writer.write("\n".as_ref());
        let _ = writer.flush();

        // TODO: reading should actually be done in async connection instead of this
        let mut line = String::new();
        let _ = reader.read_line(&mut line);
        let response: Response = serde_json::from_str(&*line).unwrap();

        return response.data;
    }
}
