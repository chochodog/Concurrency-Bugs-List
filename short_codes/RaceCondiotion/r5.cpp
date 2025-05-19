#include <iostream>
#include <thread>
#include <vector>

// 공유 변수
int counter = 0;

// 스레드가 실행할 함수: counter 변수 증가
void increment() {
    for (int i = 0; i < 10000; ++i) {
        ++counter;  // 공유 변수 수정
    }
}

int main() {
    std::vector<std::thread> threads;

    // 10개의 스레드 생성
    for (int i = 0; i < 10; ++i) {
        threads.emplace_back(increment);
    }

    // 모든 스레드가 종료될 때까지 대기
    for (auto& th : threads) {
        th.join();
    }

    // 결과 출력
    std::cout << "Expected counter value: 100000\n";
    std::cout << "Actual counter value: " << counter << std::endl;

    getchar();
    return 0;
}
