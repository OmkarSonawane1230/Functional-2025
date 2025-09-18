#include <iostream>
#include <sys/socket.h>
#include <string.h>
#include <arpa/inet.h>
#include <stdlib.h>
#define PORT 21124
#define SERVER_ADDRESS "127.0.0.1"
using namespace std;
int main()
{
    sockaddr_in servadd;
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1)
    {
        cout << "Socket error";
        exit(1);
    }
    servadd.sin_family = AF_INET;
    servadd.sin_port = htons(PORT);
    servadd.sin_addr.s_addr = inet_addr(SERVER_ADDRESS);
    socklen_t cli = sizeof(servadd);
    int connstat = connect(sock, (sockaddr *)&servadd, cli);
    if (connstat == 0)
    {
        cout << "Success in connection\n";
    }
    else
    {
        cout << "Connection failed\n";
        exit(1);
    }
    char a[20], b[20], op[2], ans[20];
    while (1)
    {
        cout << "Enter first number: ";
        cin >> a;
        send(sock, a, strlen(a), 0);

        cout << "Enter second number: ";
        cin >> b;
        send(sock, b, strlen(b), 0);

        cout << "Enter operator (+, -, *, /): ";
        cin >> op;
        send(sock, op, strlen(op), 0);

        bzero(ans, sizeof(ans));
        recv(sock, ans, 20, 0);
        cout << "Result is : " << ans << endl;
    }
    return 0;
}