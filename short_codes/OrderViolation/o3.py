import random
import time

class 식당시스템:
    def __init__(self):
        self.주문목록 = []
        self.조리중 = []
        self.완료 = []
    
    def 주문접수(self, 메뉴):
        주문번호 = len(self.주문목록) + 1
        self.주문목록.append((주문번호, 메뉴))
        print(f"[주문접수] 주문번호 {주문번호}: {메뉴}")
        return 주문번호
    
    def 요리시작(self):
        if not self.주문목록:
            return False
        
        # 무작위로 주문 선택 (순서 위반 발생)
        선택_인덱스 = random.randint(0, len(self.주문목록)-1)
        주문번호, 메뉴 = self.주문목록.pop(선택_인덱스)
        
        self.조리중.append((주문번호, 메뉴))
        print(f"[조리시작] 주문번호 {주문번호}: {메뉴} - 순서 위반 가능성 있음!")
        return True
    
    def 요리완료(self):
        if not self.조리중:
            return False
        
        # 무작위로 조리 완료 선택 (순서 위반 발생)
        선택_인덱스 = random.randint(0, len(self.조리중)-1)
        주문번호, 메뉴 = self.조리중.pop(선택_인덱스)
        
        self.완료.append((주문번호, 메뉴))
        print(f"[요리완료] 주문번호 {주문번호}: {메뉴} - 순서 위반 가능성 있음!")
        return True

# 시뮬레이션 실행
def 시뮬레이션():
    식당 = 식당시스템()
    메뉴목록 = ["비빔밥", "김치찌개", "불고기", "된장찌개", "떡볶이"]
    
    # 5개 주문 접수
    for 메뉴 in 메뉴목록:
        식당.주문접수(메뉴)
    
    # 요리 과정 시뮬레이션
    while 식당.주문목록 or 식당.조리중:
        if 식당.주문목록 and random.random() < 0.7:
            식당.요리시작()
        if 식당.조리중 and random.random() < 0.5:
            식당.요리완료()
        time.sleep(0.5)
    
    print("\n최종 완료된 주문:")
    for 번호, 메뉴 in 식당.완료:
        print(f"주문번호 {번호}: {메뉴}")

시뮬레이션()