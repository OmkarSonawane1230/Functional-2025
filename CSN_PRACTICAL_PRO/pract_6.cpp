#include <iostream>
using namespace std;

struct node {
    int dist[20];
    int from[20];
};

int main() {
    int no; // number of nodes
    node route[10]; // assuming maximum 10 nodes
    int dm[20][20]; // distance matrix

    cout << "Enter number of nodes: ";
    cin >> no;

    cout << "Enter the distance matrix:\n";
    for (int i = 0; i < no; i++) {
        for (int j = 0; j < no; j++) {
            cin >> dm[i][j];
            dm[i][i] = 0; // distance to self is always 0
            route[i].dist[j] = dm[i][j];
            route[i].from[j] = j;
        }
    }

    int flag;
    do {
        flag = 0;
        for (int i = 0; i < no; i++) {
            for (int j = 0; j < no; j++) {
                for (int k = 0; k < no; k++) {
                    if (route[i].dist[j] > route[i].dist[k] + route[k].dist[j]) {
                        route[i].dist[j] = route[i].dist[k] + route[k].dist[j];
                        route[i].from[j] = k;
                        flag = 1;
                    }
                }
            }
        }
    } while (flag);

    for (int i = 0; i < no; i++) {
        cout << "\nRouting table for router " << i + 1 << ":\n";
        cout << "Destination\tNext Hop\tDistance\n";
        for (int j = 0; j < no; j++) {
            cout << j + 1 << "\t\t" << route[i].from[j] + 1 << "\t\t" << route[i].dist[j] << endl;
        }
    }

    return 0;
}