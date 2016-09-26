use std::io::prelude::*;
use std::net::TcpStream;

fn main() {
    let mut sock = TcpStream::connect("127.0.0.1:4222").unwrap();
    let mut buf = [0; 1024];
    loop {
        let len = sock.read(&mut buf).unwrap();
        if len == 0 {
            break;
        }
        let s = std::str::from_utf8(&buf[..len]).unwrap();
        if s.starts_with("INFO") {
            println!("{}", s);
        } else if s.starts_with("PING") {
            let _ = sock.write_all(b"PONG\r\n");
        }
    }
}
