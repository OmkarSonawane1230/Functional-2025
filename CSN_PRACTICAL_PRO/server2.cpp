#include <iostream>
#include <sys/socket.h>
#include <string.h>
#include <arpa/inet.h>
#include <stdlib.h>
#define PORT 21124
using namespace std;
int main()
{
    sockaddr_in servadd, clientadd;
    int sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1)
    {
        cout << "Socket error";
        exit(1);
    }
    servadd.sin_family = AF_INET;
    servadd.sin_port = htons(PORT);
    servadd.sin_addr.s_addr = INADDR_ANY;
    socklen_t cli = sizeof(clientadd);
    int bindstat = bind(sock, (sockaddr *)&servadd, sizeof(servadd));
    cout << "Waiting for client..\n";
    listen(sock, 4);
    int aaccept = accept(sock, (struct sockaddr *)&clientadd, &cli);
    cout << "Connected\n";
    char op[2];
    char num1[20];
    char num2[20];
    float a, b, res;
    while (1)
    {
        int n;
        bzero(num1, sizeof(num1));
        n = recv(aaccept, num1, 20, 0);
        a = atof(num1);

        int n1;
        bzero(num2, sizeof(num2));
        n1 = recv(aaccept, num2, 20, 0);
        b = atof(num2);

        cout << "First number : " << num1 << endl;
        cout << "Second Number : " << num2 << endl;

        int pp;
        bzero(op, sizeof(op));
        pp = recv(aaccept, op, 2, 0);
        cout << "Operator : " << op << endl;

        char ans[20];
        bzero(ans, sizeof(ans));
        switch (op[0])
        {
        case '+':
            res = a + b;
            sprintf(ans, "%f", res);
            break;
        case '-':
            res = a - b;
            sprintf(ans, "%f", res);
            break;
        case '*':
            res = a * b;
            sprintf(ans, "%f", res);
            break;
        case '/':
            if (b == 0)
                sprintf(ans, "Error");
            else
                sprintf(ans, "%f", a / b);
            break;
        default:
            sprintf(ans, "Invalid");
        }
        cout << "Result: " << ans << endl;
        send(aaccept, ans, strlen(ans), 0);
    }
    return 0;
}