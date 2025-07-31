package main

import (
    "fmt"
    "net"
    "syscall"
)

func main() {
    conn, _ := net.Dial("tcp", "localhost:8080")
    rawConn, _ := conn.(*net.TCPConn).SyscallConn()
    rawConn.Control(func(fd uintptr) {
        syscall.SetsockoptInt(int(fd), syscall.IPPROTO_TCP, syscall.TCP_NODELAY, 1)
        syscall.SetsockoptInt(int(fd), syscall.SOL_SOCKET, syscall.SO_RCVBUF, 65536)
        syscall.SetsockoptInt(int(fd), syscall.SOL_SOCKET, syscall.SO_SNDBUF, 65536)
    })
    fmt.Println("TCP_NODELAY và buffer đã được cấu hình.")
    conn.Close()
}