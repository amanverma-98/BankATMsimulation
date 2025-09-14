# ---------------- ATM Class ----------------
class ATM:
    def __init__(self,account_number,pin,balance=0):
        #__init__ -> constructor : kisi object k attributes ko intialize krne k liye use kiya jata hai 
        self.account_number = account_number
        self.__pin = pin          # __ -> private attribute bnane k liye use kiya hai  (Encapsulation)
        self.__balance = balance  # __balance bhi private hai, direct access nahi hoga (Encapsulation)


    def __verify_pin(self,pin):
        # ye method sirf class ke andar hi use ho skta hai (private method) (Encapsulation)
        return self.__pin == pin    
    
    
    def check_balance(self,pin):   
        # Abstraction -> user ko sirf balance dekhna hai, pin check ka internal logic hide hai
        if self.__verify_pin(pin):
            print(f"Account {self.account_number} -> Balance: {self.__balance}")
        else:
            print("Wrong Pin!")

    def deposit(self,amount,pin):
        # Abstraction + Encapsulation -> user ko simple interface diya deposit ke liye
        if self.__verify_pin(pin):
            if amount > 0:
                self.__balance += amount
                print(f"{amount} deposited. New Balance: {self.__balance}")
                #f" -> f-strings use hoti hai variables ko string k saath use krne ke liye
            else:
                print("Deposit must be positive")
        else:
            print("Wrong Pin!")        


    def withdraw(self,amount,pin):
        # Polymorphism ke liye ye method child classes override kr skti hai (CurrentAccount me)
        if self.__verify_pin(pin):
            if amount <= self.__balance:    #withdraw amount hmesha available balance se km hona chahiye 
                self.__balance -= amount
                print(f"{amount} withdrawn. Remaining Balance: {self.__balance}")
            else:
                print("Insufficient Balance")
        else:
                print("Wrong Pin!")                        
    

    def _get_balance(self):    #getter (Encapsulation -> indirectly data ko access krne ka way)
        return self.__balance
    

    def _set_balance(self, value):    #setter (Encapsulation -> indirectly data ko modify krne ka way)
        self.__balance = value



# Inheritance -> SavingsAccount ATM class se inherit kr rha hai
class SavingsAccount(ATM):
    def __init__(self, account_number, pin, balance=0, interest_rate=0.05):
        super().__init__(account_number, pin, balance)
        #super() -> iska use hm parent class ki properties ko access krne k liye krte h child class m -> inheritance
        self.interest_rate = interest_rate


    def add_interest(self):
        # Polymorphism -> SavingsAccount ka apna extra feature (CurrentAccount me ye nahi hai)
        balance = self._get_balance()
        interest = balance * self.interest_rate
        self._set_balance(balance + interest)
        print(f"Interest {interest:.2f} added. New Balance: {self._get_balance()}")


# Inheritance -> CurrentAccount bhi ATM class se inherit krta hai
class CurrentAccount(ATM):
    def __init__(self, account_number, pin, balance=0, overdraft_limit=1000):
        super().__init__(account_number, pin, balance)
        self.overdraft_limit = overdraft_limit


    def withdraw(self, amount, pin):
        # Polymorphism -> yaha withdraw method override kiya gya hai (overdraft allow krne ke liye)
        balance = self._get_balance()
        if self._ATM__verify_pin(pin):   # private method ko access karne ka tarika
            if amount <= balance + self.overdraft_limit:
                self._set_balance(balance - amount)
                print(f"{amount} withdrawn (Current A/C). New Balance: {self._get_balance()}")
            else:
                print("Overdraft limit exceeded!")
        else:
            print("Wrong Pin!")



# multiple users ke liye
class ATMSystem:
    def __init__(self):
        # Composition -> ATMSystem ke andar multiple accounts store ho rhe hai
        self.accounts = {}


    def add_account(self, account):
        self.accounts[account.account_number] = account


    def get_account(self, account_number):
        return self.accounts.get(account_number, None)  



#Main Function 
def main():
    system = ATMSystem()


    #pehle se created demo account
    system.add_account(SavingsAccount(101,1234,5000))
    system.add_account(CurrentAccount(102, 4321, 2000, overdraft_limit=1500))


    print("Welcome to the ATM Simulation")
    acc_no = int(input("Enter Account Number: "))

    account = system.get_account(acc_no)

    if not account:
        print("Account not found!")
        return 


 # max 3 times m user ko correct pin dalni hogi 
    attempts = 0
    pin = None
    while attempts < 3:
        pin = int(input("Enter PIN: "))
        if account._ATM__verify_pin(pin):
            break
        else:
            print("Wrong PIN! Try again.")
            attempts += 1
    if attempts == 3:
        print("Too many wrong attempts. Exiting...")
        return
    


    #main interface
    while True:
        print("\n------FEATURES------")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("0. Exit")


        choice = input("Enter choice: ")

        if choice == "1":
            # Agar account SavingsAccount hai to interest add karo before showing balance
            if isinstance(account, SavingsAccount):
                account.add_interest()
            account.check_balance(pin)
        elif choice == "2":
            amount = float(input("Enter the amount to deposit: "))
            account.deposit(amount, pin)
        elif choice == "3":
            amount = float(input("Enter amount to withdraw: "))
            account.withdraw(amount, pin)
        elif choice == "0":
            print("Thankyou for using ATM. Goodbye!")
            break
        else:
            print("Invalid choice, try again.")



if __name__ == "__main__":
    main()