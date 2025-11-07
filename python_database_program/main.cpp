#include <iostream>
#include "libraries/bank_services.hpp"
#include <string.h>

using namespace std;

int main() {
    cout << "Hello World" << endl;
    MyClass m;
    m.doSomething();

    cout << "\n" << "2 + 56 = " << add(2, 56) << endl; 
    return 0;
}