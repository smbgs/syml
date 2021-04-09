use std::{thread, fs};
use std::os::unix::net::{UnixStream, UnixListener};
use std::io::{BufReader, BufRead, BufWriter, Write};
use json;
use json::object;
use home::home_dir;
use std::path::{PathBuf, Path};
use std::borrow::Borrow;

fn handle_client(stream: UnixStream) {

    let mut reader = BufReader::new(stream.try_clone().unwrap());
    let mut writer = BufWriter::new(stream.try_clone().unwrap());

    let mut line = String::new();
    let num_bytes = reader.read_line(&mut line);

    let command = json::parse(&*line).unwrap();

    println!("Recieved command: {:?}", command);

    let mut cid = command["cid"].clone();

    let response = object!{
        cid: cid,
        data: {
            key1: "ok",
            errors: [],
            info: []
        }
    };

    writer.write(json::stringify(response).as_ref());
    writer.write("\n".as_ref());
    writer.flush();
}

fn main() -> std::io::Result<()> {
    let socket_path =
        home_dir().unwrap().join(Path::new(".syml/sockets/test-rust-socket.sock"));

    println!("Listening at {:?}", &socket_path);

    fs::remove_file(&socket_path);
    let listener = UnixListener::bind(&socket_path)?;

    // accept connections and process them, spawning a new thread for each one
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                /* connection succeeded */
                thread::spawn(|| handle_client(stream));
            }
            Err(err) => {
                /* connection failed */
                break;
            }
        }
    }

    fs::remove_file(&socket_path);

    Ok(())
}