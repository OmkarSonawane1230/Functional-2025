/* Error Detection & Correction using Hamming Code */
/* Program at sender to generate code word for a give data word */

#include <iostream>
#include <vector>
#include <string>

using namespace std;

int main() {
    string data;

    int dataTx[12] = {0};
    int dataRx[12] = {0};
    int syndrome, p1, p2, p4, p8;

    cout << "\nEnter 7 bits of data one by one: ";
    cin >> data;

    for (int i = 11, j = 0; i >= 3; i--) {
        if (i == 8 || i == 4 || i == 2 || i == 1) {
            continue;
        }

        dataTx[i] = data[j] - '0';
        j++;
    }

    // Calculate parity bits
    dataTx[1] = dataTx[3] ^ dataTx[5] ^ dataTx[7] ^ dataTx[9] ^ dataTx[11];
    dataTx[2] = dataTx[3] ^ dataTx[6] ^ dataTx[7] ^ dataTx[10] ^ dataTx[11];
    dataTx[4] = dataTx[5] ^ dataTx[6] ^ dataTx[7] ;
    dataTx[8] = dataTx[9] ^ dataTx[10] ^ dataTx[11];

    cout << "\nEncoded Data is: ";
    for (int i = 11; i >= 1; i--) {
        cout << dataTx[i];
    }

    /* Correction of Error at reciever side */

    cout << "\n\nEnter received bits of data: ";
    cin >> data;

    for (int i = 11, j = 0; i >= 1; i--, j++) {
        dataRx[i] = data[j] - '0';
    }

    // Calculate parity bits at receiver
    p1 = dataRx[1] ^ dataRx[3] ^ dataRx[5] ^ dataRx[7] ^ dataRx[9] ^ dataRx[11];
    p2 = dataRx[2] ^ dataRx[3] ^ dataRx[6] ^ dataRx[7] ^ dataRx[10] ^ dataRx[11];
    p4 = dataRx[4] ^ dataRx[5] ^ dataRx[6] ^ dataRx[7];
    p8 = dataRx[8] ^ dataRx[9] ^ dataRx[10] ^ dataRx[11];

    syndrome = p8 * 8 + p4 * 4 + p2 * 2 + p1;

    if (syndrome == 0) {
        cout << "\nNo error detected in received data.";
    } else {
        cout << "\nError detected at position: " << syndrome;
        cout << "\n\nCorrected data is: ";
        dataRx[syndrome] = (dataRx[syndrome] == 0) ? 1 : 0; // Correct the error
        for (int i = 11; i >= 3; i--) {
            if (i == 8 || i == 4 || i == 2 || i == 1) continue;
            cout << dataRx[i];
        }
    }

    cout << endl;
    return 0;
}