#include <iostream>
#include <vector>
#include <thread>
#include <mutex>
#include <atomic>

class ThreadCounter {
public:
    ThreadCounter() : counter(0) {}

    void increment() {
        for (int i = 0; i < 10000; ++i) {
            counter++;
        }
    }

    void decrement() {
        for (int i = 0; i < 5000; ++i) {
            counter--;
        }
    }

    void append_results(int value) {
        for (int i = 0; i < 1000; ++i) {
            results.push_back(value);
        }
    }

    void run_threads(int num_threads) {
        std::vector<std::thread> threads;

        for (int i = 0; i < num_threads / 2; ++i) {
            threads.emplace_back(&ThreadCounter::increment, this);
        }

        for (int i = 0; i < num_threads / 4; ++i) {
            threads.emplace_back(&ThreadCounter::decrement, this);
        }

        for (int i = 0; i < num_threads / 4; ++i) {
            threads.emplace_back(&ThreadCounter::append_results, this, i);
        }

        for (auto& thread : threads) {
            if (thread.joinable()) {
                thread.join();
            }
        }

        std::cout << "Expected counter value (approx): "
                  << (num_threads / 2 * 10000 - num_threads / 4 * 5000) << std::endl;
        std::cout << "Actual counter value: " << counter << std::endl;
        std::cout << "Expected results length: " << (num_threads / 4 * 1000) << std::endl;
        std::cout << "Actual results length: " << results.size() << std::endl;
    }

    void reset() {
        counter = 0;
        results.clear();
        std::cout << "Counter and results reset!" << std::endl;
    }

private:
    std::atomic<int> counter;
    std::vector<int> results;
};

int main() {
    ThreadCounter counter;

    std::cout << "=== Test ===" << std::endl;
    counter.run_threads(100);
    getchar();

    return 0;
}
