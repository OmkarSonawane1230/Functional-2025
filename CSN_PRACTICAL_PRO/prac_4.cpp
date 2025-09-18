/* Sliding Window Protocols  */
/* Part A program for Go back N sliding window protocol */

#include <bits/stdc++.h>
#include <ctime>
#define ll long long int

using namespace std;

void transmission(ll &i, ll &N, ll &tf, ll &tt) {
    while (i <= tf) {
        int z = 0;
        for (int k = i; k < i + N && k <= tf; k++) {
            cout << "Sending Frame " << k << "..." << endl;
            tt++;
        }

        for (int k = i; k < i + N && k <= tf; k++) {
            int f = rand() % 2;
            if (!f) {
                cout << "Retransmitting from Frame " << k << "..." << endl;
                z++;
            } else {
                cout << "Timeout!!! Frame Number; " << k << " not received." << endl;
                cout << "Retransmitting from Frame " << k << "..." << endl;
                break;
            }
        }

        cout << endl;
        i += z;
    }
}

int main() {
    ll tf, N, tt = 0;
    srand(time(NULL));

    cout << "Enter the Total Number of Frames: ";
    cin >> tf;
    cout << "Enter the Window Size: ";
    cin >> N;

    ll i = 1;
    transmission(i, N, tf, tt);
    cout << "Total number of frame which were send and resent are: " << tt << endl;
    return 0;
}