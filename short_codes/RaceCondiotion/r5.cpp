#include <iostream>
#include <thread>
#include <vector>

int counter = 0;

void increment() {
    for (int i = 0; i < 10000; ++i) {
        ++counter;
    }
}

int main() {
    std::vector<std::thread> threads;

    for (int i = 0; i < 10; ++i) {
        threads.emplace_back(increment);
    }

    for (auto& th : threads) {
        th.join();
    }

    std::cout << "Expected counter value: 100000\n";
    std::cout << "Actual counter value: " << counter << std::endl;

    getchar();
    return 0;
}
