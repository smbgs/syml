use core::option::Option::None;
use core::result::Result::{Err, Ok};
use std::{fs, thread};
use std::io::{BufReader, BufRead, BufWriter, Write};
use std::os::unix::net::UnixListener;

use crate::protocol::{Command, Commands, CommandHandler, Response, get_socket_path};
use std::borrow::Borrow;

#[derive(Clone)]
pub struct Service {
    name: String,
    commands: Commands,
}

impl Service {

    pub fn new(name: &str) -> Service {
        Service {
            name: String::from(name),
            commands: Commands::new(),
        }
    }

    pub fn cmd(&mut self, name: &str, handler: CommandHandler) {
        self.commands.insert(String::from(name), handler);
    }

    pub fn serve(&self) -> std::io::Result<()> {

        let socket_path = get_socket_path(self.name.borrow());
        println!("Listening at {:?}", &socket_path);

        let _ = fs::remove_file(&socket_path);

        let listener = UnixListener::bind(&socket_path)?;

        // accept connections and process them, spawning a new thread for each one
        for stream in listener.incoming() {
            match stream {
                Ok(stream) => {
                    /* connection succeeded */
                    let mut reader = BufReader::new(stream.try_clone().unwrap());
                    let mut writer = BufWriter::new(stream.try_clone().unwrap());

                    let inner_self = self.clone();

                    thread::spawn(move || {

                        let mut line = String::new();
                        let _ = reader.read_line(&mut line);
                        let command: Command = serde_json::from_str(&*line).unwrap();

                        let command_handler = inner_self.commands.get(&command.name);

                        if command_handler != None  {
                            let response = Response {
                                cid: command.cid.clone(),
                                data: command_handler.unwrap()(command),
                            };

                            let _ = writer.write(serde_json::to_string(&response).unwrap().as_ref());
                            let _ = writer.write("\n".as_ref());
                            let _ = writer.flush();

                        } else {
                            // TODO: command nof found, fuck off handler
                        }

                    });
                }
                Err(_err) => {
                    /* connection failed */
                    break;
                }
            }
        }

        fs::remove_file(&socket_path)?;

        Ok(())
    }

}
