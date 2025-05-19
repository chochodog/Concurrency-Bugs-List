#include <iostream>
#include <vector>
#include <thread>
#include <mutex>
#include <atomic>

class ThreadCounter {
public:
    ThreadCounter() : counter(0) {}

    void increment() {
        // Counter 값을 증가시키는 메서드
        for (int i = 0; i < 10000; ++i) {
            counter++;
        }
    }

    void decrement() {
        // Counter 값을 감소시키는 메서드
        for (int i = 0; i < 5000; ++i) {
            counter--;
        }
    }

    void append_results(int value) {
        // 공유 리스트에 값을 추가
        for (int i = 0; i < 1000; ++i) {
            results.push_back(value);
        }
    }

    void run_threads(int num_threads) {
        std::vector<std::thread> threads;

        // Increment 작업을 하는 스레드 생성
        for (int i = 0; i < num_threads / 2; ++i) {
            threads.emplace_back(&ThreadCounter::increment, this);
        }

        // Decrement 작업을 하는 스레드 생성
        for (int i = 0; i < num_threads / 4; ++i) {
            threads.emplace_back(&ThreadCounter::decrement, this);
        }

        // Append 작업을 하는 스레드 생성
        for (int i = 0; i < num_threads / 4; ++i) {
            threads.emplace_back(&ThreadCounter::append_results, this, i);
        }

        // 모든 스레드가 종료될 때까지 대기
        for (auto& thread : threads) {
            if (thread.joinable()) {
                thread.join();
            }
        }

        // 결과 출력
        std::cout << "Expected counter value (approx): "
                  << (num_threads / 2 * 10000 - num_threads / 4 * 5000) << std::endl;
        std::cout << "Actual counter value: " << counter << std::endl;
        std::cout << "Expected results length: " << (num_threads / 4 * 1000) << std::endl;
        std::cout << "Actual results length: " << results.size() << std::endl;
    }

    void reset() {
        // Counter와 결과를 초기화
        counter = 0;
        results.clear();
        std::cout << "Counter and results reset!" << std::endl;
    }

private:
    std::atomic<int> counter; // 공유 자원
    std::vector<int> results; // 결과 리스트
};

int main() {
    ThreadCounter counter;

    // 테스트 실행
    std::cout << "=== Test ===" << std::endl;
    counter.run_threads(100);
    getchar();

    return 0;
}
