/* Client.java */

import java.io.*;
import java.net.*;

public class MyClient {
    public static void main(String[] args) {
        try {
            Socket s = new Socket("localhost", 6666);
            DataOutputStream dout = new DataOutputStream(s.getOutputStream());
            dout.writeUTF("Hello Server");
            dout.flush();
            // Read response from server
            DataInputStream dis = new DataInputStream(s.getInputStream());
            String response = dis.readUTF();
            System.out.println("Server says: " + response);
            dis.close();
            dout.close();
            s.close();
        } catch (Exception e) {
            System.out.println(e);
        }
    }
}
