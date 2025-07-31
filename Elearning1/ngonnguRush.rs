use std::net::TcpStream;
use socket2::{Socket, Domain, Type, Protocol};

fn main() {
    let stream = TcpStream::connect("127.0.0.1:8080").unwrap();
    let socket = Socket::from(stream);
    socket.set_nodelay(true).unwrap();
    socket.set_recv_buffer_size(65536).unwrap();
    socket.set_send_buffer_size(65536).unwrap();
    println!("TCP_NODELAY và buffer đã được cấu hình.");
}