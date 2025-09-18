/* MyServer.java */

import java.io.*;
import java.net.*;

public class MyServer {
    public static void main(String[] args) {
        try {
            ServerSocket ss = new ServerSocket(6666);
            Socket s = ss.accept();// establishes connection
            DataInputStream dis = new DataInputStream(s.getInputStream());
            String str = (String) dis.readUTF();
            System.out.println("Message: " + str);
            // Send response to client
            DataOutputStream dout = new DataOutputStream(s.getOutputStream());
            dout.writeUTF("I got the message");
            dout.flush();
            dout.close();
            dis.close();
            s.close();
            ss.close();

        } catch (Exception e) {
            System.out.println(e);
        }
    }
}