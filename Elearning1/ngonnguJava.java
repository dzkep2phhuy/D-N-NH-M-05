import java.net.*;
import java.io.*;

public class TcpOptimization {
    public static void main(String[] args) throws Exception {
        Socket socket = new Socket("localhost", 8080);
        socket.setTcpNoDelay(true);
        socket.setReceiveBufferSize(65536);
        socket.setSendBufferSize(65536);
        System.out.println("TCP_NODELAY và buffer đã được cấu hình.");
        socket.close();
    }
}