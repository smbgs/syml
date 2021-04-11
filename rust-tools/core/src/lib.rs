use std::{fs, thread};
use std::io::{BufRead, BufReader, BufWriter, Write};
use std::os::unix::net::{UnixListener};
use std::path::{Path};
use std::collections::HashMap;

use home::home_dir;
use serde::{Deserialize, Serialize};
use serde_json::{Value};

#[derive(Serialize, Deserialize, Debug)]
pub struct Command {
    name: String,
    cid: String,
    args: Value,
    shape: Value,
    info: bool,
    errors: bool,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Response {
    cid: String,
    data: Value,
}

type CommandHandler = fn(command: Command) -> Value;
type Commands = HashMap<String, CommandHandler>;

#[derive(Clone)]
pub struct Service {
    name: String,
    commands: Commands,
}

impl Service {

    pub fn new(name: &str) -> Service {
        Service {
            name: String::from(name),
            commands: HashMap::new(),
        }
    }

    pub fn cmd(&mut self, name: &str, handler: CommandHandler) {
        self.commands.insert(String::from(name), handler);
    }

    pub fn serve(&self) -> std::io::Result<()> {

        let socket_path =
            home_dir().unwrap().join(
                Path::new(format!(".syml/sockets/{}.sock", self.name).as_str())
            );

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
