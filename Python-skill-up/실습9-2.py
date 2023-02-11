class BankAcct:
    def __init__(self, name, num, deposit, interest_rate):
        self.name = name
        self.num = num
        self.deposit = deposit
        self.interest_rate = interest_rate
    
    # 이자율을 재설정합니다.
    def set_interest_rate(self, new_interest_rate):
        self.interest_rate = new_interest_rate

    # 입출금을 합니다.
    def banking(self, sum, type):
        if type.lower() == 'd' or 'deposit':
            self.deposit += sum
        else:
            self.deposit -= sum
    
    # 시간의 경과에 따른 잔고를 계산합니다.
    def change_due_to_time(self, elapsed_year):
        for i in range(int(elapsed_year)):
            self.deposit = self.deposit * (1 + self.interest_rate)

    def __str__(self):
        return '예금주: {}, 계좌번호: {}, 잔고: {}, 이자율: {}'.format(self.name, self.num, self.deposit, self.interest_rate)


my_account = BankAcct('Kim','777-777-777-777', 100000000, 0.01)

print(my_account)

my_account.change_due_to_time(10)

print(my_account)
