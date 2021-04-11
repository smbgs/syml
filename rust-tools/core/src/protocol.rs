use std::collections::HashMap;

use serde::{Deserialize, Serialize};
use serde_json::{Value};
use std::path::{PathBuf, Path};
use home::home_dir;

#[derive(Serialize, Deserialize, Debug)]
pub struct Command {
    pub name: String,
    pub cid: String,
    pub args: Value,
    pub shape: Value,
    pub info: bool,
    pub errors: bool,
}

#[derive(Serialize, Deserialize, Debug)]
pub struct Response {
    pub cid: String,
    pub data: Value,
}

pub type CommandHandler = fn(command: Command) -> Value;
pub type Commands = HashMap<String, CommandHandler>;

pub fn get_socket_path(name: &String) -> PathBuf {
    return home_dir().unwrap().join(
        Path::new(format!(".syml/sockets/{}.sock", name).as_str())
    );
}
