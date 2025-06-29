from abc import ABC, abstractmethod
from datetime import datetime
import random
from typing import Dict,List, Optional

#-----------1.Account Management Module------------#
class Account(ABC):
    def __init(self,account_number:str,customer_id:str,balance:float=0.0):
        self.__account_number = account_number #protected attribute
        self._customer_id = customer_id #private attribute
        self._balance = balance
        self._opening_date = datetime.now()
        self._transactions : List[Transaction] = []

    @property
    def account_number(self) -> str:
        return self.__account_number
    
    @property
    def balance(self) -> float:
        return self._balance
    
    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self._balance += amount
            transaction = Transaction(amount, "Deposit", self.__account_number)
            self._transactions.append(transaction)
            return True
        return False
    
    @abstractmethod
    def withdraw(self, amount: float) -> bool:
        pass

    def get_transaction(self) -> List['Transaction']:
        return self._transactions
    
    def __str__(self):
        return f"Account Number: {self.__account_number} - Balance: {self._balance}"
    
class SavingAccount(Account): 
    def __init__(self, account_number: str, customer_id: str, balance: float = 0.0, interest_rate:float = 0.01):
        super().__inti__(account_number, customer_id, balance)
        self._interest_rate = interest_rate

    def withdraw(self, amount:float) -> bool:
        if amount > 0  and self._balance >= amount:
            self._balance -= amount
            transaction = Transaction(amount, "Withdraw", self.account_number)
            self._transactions.append(transaction)
            return True
        return False
    
    def apply_interest(self):
        interest = self._balance * self._interest_rate
        self.deposit(interest)
        return interest
    
class CurrentAccount(Account):  # Inheritence
    OVERDRAFT_LIMIT = 1000.0 #class varible for overdraft limit

    def withdraw(self, amount: float) -> bool: #Polymorphism
        if amount > 0 and (self._balance + CurrentAccount.OVERDRAFT_LIMIT) >= amount:
            self._balance -= amount
            transaction = Transaction(amount, "Withdraw", self.account_number)
            self._transactions.append(transaction)
            return True
        return False
    
    #-----------2. Customer Management Module------------#

    class Customer:
        def __init(self, customer_id: str, name: str, email: str, phone:str):
            self._customer_id = customer_id
            self._name = name
            self._email = email
            self._phone = phone
            self._accounts: Dict[str, Account] = {}

        def add_account(self, account: Account) -> bool:
            if account.account_number not in self.accounts:
                self._accounts[account.account_number] = account
                return True
            return False
        
        def get_account(self, account_number: str) -> Optional[Account]:
            return self._accounts.get(account_number)
        
        def get_all_accounts(self) -> Dict[str, Account]:
            return self._accounts
        
        def __str__(self) -> str:
            return f"Customer ID: {self._customer_id}, Name: {self._name}, Email: {self._email}"

#-------------3. Transaction Processing Module------------#
class Transaction:
    def __init__(self, amount: float, transaction_type: str, account_number: str):
        self._amount = amount
        self._type = transaction_type
        self._account_number = account_number
        self._timestamp = datetime.now()
        self._transaction_id = f"TXN{random.randint(1000, 99999)}"

    def __str__(self) -> str:
        return f"{self._timestamp} - {self._transaction_id}:{self._type} of {self._amount} on Account {self._account_number}"
    
#-------------4. Loan Management Module------------#
class Loan:
    def __init__(self, loan_id:str, customer_id:str, amount:float, interest_rate:float, term:int):
        self._loan_id = loan_id
        self._customer_id = customer_id
        self._principal = amount
        self._term = term
        self._remaining_balance = amount
        self._start_date = datetime.now()
        self._payments : List[float] = []

    def make_payment(self, amount: float) -> bool:
        if amount <= 0 or amount > self._remaining_balance:
            return False
        self._remaining_balance -= amount
        self._payments.append(amount)
        return True
    
    def calculate_interest(self) -> float:
        monthly_rate = self._interest_rate/12
        return (self._principal * monthly_rate * (1 + monthly_rate) ** self._term)/((1+monthly_rate)**self._term - 1)
    
    def __str__(self) -> str:
        return f"Loan ID: {self._loan_id}, Principal: {self._principal}, Remaining : {self._remaining_balance"}

#--------------5. Interest Calculation Module------------#
class InterestCalculator:
    @staticmethod
    def calculate_simple_interest(principal:float,rate:float,time:float) -> float:
        return principal * rate * time

    @staticmethod
    def calculate_compound_interest(principal:float,rate:float,time:float,compounding_frequency:int=1)->float:
        return principal * (1 + rate/compounding_frequency) ** (compounding_frequency * time) - principal


#-----------6. ATM Simulation Module------------#
class ATM:
    def __init__(self, atm_id: str, location: str, cash_balance:float = 10000.0):
        self._atm_id = atm_id
        self._location = location
        self._cash_balance = cash_balance

    def withdraw(self, account: Account, amount: float) -> bool:
        if self._cash_balance >= amount and account.withdraw(amount):
            self._cash_balance -= amount
            return True
        return False

    def deposit(self, account: Account, amount: float) -> bool:
        if account.deposit(amount):
            self._cash_balance += amount
            return True
        return False

    def check_balance(self, account: Account) -> float:
        return account.balance

#--------------7. Online Banking Module------------#
class OnlineBanking:
    def __init__(self, bank):
        self._bank = bank
        self._logged_in_users: Dict[str, str] = {}

    def login(self, customer_id: str, password: str) -> Optional[str]:
        session_token = f"SESSION_{random.randint(1000, 99999)}"
        self._logged_in_users[customer_id] = session_token
        return session_token

    def transfer(self,session_token:str, from_account:str,to_account:str, amount:float) -> bool:
        if session_token not in self._logged_in_user.values():
            return False

        from_acc = self._bank.get_account(from_account)
        to_acc = self._bank.get_account(to_account)

        if from_acc and to_acc and from_acc.withdraw(amount):
            return to_acc.deposit(amount)
        return False

#-------------8. Fraud Detection Module------------#
class FraudDetection:
    @staticmethod
    def detect_unusual_activity(account: Account, transaction_amount:float) -> bool:
        return transaction_amount > (account.balance * 0.5)

#--------------9. Reporting Module-----------------#
class ReportGenerator:
    @staticmethod
    def generate_account_statement(account: Account) -> str:
        statement = f"Account Statement for {account.account_number}\n"
        statement += f"Current Balance: {account.balance}\n"
        statement += f"Transactions History:\n"
        for txn in account.get_transactions():
            statement +-f"-{txn}\n"
        return statement

#-----------------10. Notification System Module-----------------#
class NotificationService:
    @staticmethod
    def send_email(email: str, message:str) -> bool:
        print(f"Email sent to {email}: {message}")
        return True

    @staticmethod
    def send_sms(phone:str, message:str) -> bool:
        print(f"SMS sent to {phone}:{message}")
        return True

#-----------------11. Investment Protofolio Module---------------#
class Investment:
    def __init__(self,investment_id:str,customer_id:str,amount:float,investment_type:str):
        self._investment_id = investment_id
        self._customer_id = customer_id
        self._initial_amount = amount
        self._current_value = amount
        self._investment_type = investment_type
        self._start_date = datetime.now()

    def update_value(self, new_value:float) -> None:
        self._current_value = new_value

    def get_return(self) -> float:
        return self._current_value - self._intital_amount
    
    def __str__(self) -> str:
        return f"Investment ID: {self._investment_id}, {self._investment_type}, Value: {self._current_value}"
    
#-----------------12. Credit Card Processing Module-----------------#

class CreditCard:
    def __init__(self, card_number: str, customer_id: str, credit_limit: float, expiry_date: str):
        self._card_number = card_number
        self._customer_id = customer_id
        self._credit_limit = credit_limit
        self._available_credit = credit_limit
        self._expiry_date = expiry_date
        self._transactions: List[Transaction] = []

    def make_purchase(self, amount: float) -> bool:
        if amount > 0 and self._avaliable_credit >= amount:
            self._available_credit -= amount
            transaction = Transaction(amount, "Purchase", self._card_number)
            self._transactions.append(transaction)
            return True
        return False
    
    def make_payment(self, amount:float) -> bool:
        if amount > 0:
            self._available_credit += amount
            transaction = Transaction(amount, "Payment", self._card_number)
            self._transactions.append(transaction)
            return True
        return False
    
#------------------13. Bill Payment Moduel------------------#
class BillPayment:
    def __init__(self, payment_id:str,account_number:str,payee:str,amountfloat):
        self._payment_id = payment_id
        self._account_number = account_number
        self._payee = payee
        self._amount = amount
        self._payment_date = datetime.now()
        self._status = "Pending"

    def process_payment(self, bank:'Bank') -> bool:
        account = bank.get_account(self._account_number)
        if account and account.withdraw(self._amount):
            self._status = "Completed"
            return True
        self._status = "Failed"
        return False
    
#------------------14. Forgeign Exchange Module------------------#
class ForexSerivce:
     _exchange_rates = {
        'USD': {'EUR': 0.85, 'GBP': 0.73, 'JPY': 110.0},
        'EUR': {'USD': 1.18, 'GBP': 0.86, 'JPY': 129.5},
        'GBP': {'USD': 1.37, 'EUR': 1.16, 'JPY': 150.8},
        'JPY': {'USD': 0.0091, 'EUR': 0.0077, 'GBP': 0.0066}
    }
     @staticmethod
     def convert(amount:float,from_currency:str,to_currency:str) ->float:
         if from_currency == to_currency:
             return amount
         try:
             rate = ForexService._exchange_rates[from_currency][to_currency]
             return amount * rate
         except KeyError:
             return None
         
#------------------15. Bank Branch Management Module------------------#
class BankBranch:
    def __init__(self, branch_id: str, location: str, manager:str):
        self._branch_id = branch_id
        self._location = location
        self._manager = manager
        self._employees: List['Employee'] = []
        self._atms: List[ATM] = []

    def add_employee(self, employee: 'Employee') -> bool:
        if employee not in self._employees:
            self._employees.append(employee)
            return True
        return False
    
    def add_atm(self, atm: ATM) -> bool:
        if atm not in self._atms:
            self._atms.append(atm)
            return True
        return False
    
#---------------16. Employee Management Module------------------#
class Employee:
    def __init__(self,employee_id: str, name: str, position: str, branch: BankBranch):
        self._employee_id = employee_id
        self._name = name
        self._position = position
        self._branch = branch
        self._hire_date = datetime.now()
    
    def __str__(self) -> str:
        return f"Employee {self._employee_id}: {self._name}, {self._position} at {self._branch._location}"

# -------------------- 17. Audit Trail Module --------------------
class AuditTrail:
    def __init__(self):
        self._logs: List[Dict] = []
    
    def log_event(self, event_type: str, description: str, user_id: str) -> None:
        log_entry = {
            'timestamp': datetime.now(),
            'event_type': event_type,
            'description': description,
            'user_id': user_id
        }
        self._logs.append(log_entry)
    
    def get_logs(self) -> List[Dict]:
        return self._logs

# -------------------- 18. Risk Assessment Module --------------------
class RiskAssessor:
    @staticmethod
    def assess_credit_risk(customer: Customer, loan_amount: float) -> str:
        # Simplified risk assessment
        total_balance = sum(acc.balance for acc in customer.get_all_accounts().values())
        if loan_amount < total_balance * 0.5:
            return "Low"
        elif loan_amount < total_balance:
            return "Medium"
        return "High"

# -------------------- 19. Compliance Check Module --------------------
class ComplianceChecker:
    @staticmethod
    def check_kyc(customer: Customer) -> bool:
        # Simplified KYC check
        required_fields = ['_name', '_email', '_phone']
        return all(getattr(customer, field, None) is not None for field in required_fields)
    
    @staticmethod
    def check_aml(transaction: Transaction) -> bool:
        # Simplified AML check
        return transaction._amount <= 10000  # Flag transactions over $10,000

# -------------------- 20. API Integration Module --------------------
class ThirdPartyAPI:
    @staticmethod
    def verify_identity(name: str, id_number: str) -> bool:
        # Simulate API call to identity verification service
        return len(name) > 2 and len(id_number) > 5
    
    @staticmethod
    def check_credit_score(customer_id: str) -> int:
        # Simulate API call to credit bureau
        return random.randint(300, 850)

# -------------------- Main Bank Class --------------------
class Bank:
    def __init__(self, name: str):
        self._name = name
        self._customers: Dict[str, Customer] = {}
        self._accounts: Dict[str, Account] = {}
        self._loans: Dict[str, Loan] = {}
        self._credit_cards: Dict[str, CreditCard] = {}
        self._investments: Dict[str, Investment] = {}
        self._branches: Dict[str, BankBranch] = {}
        self._audit_trail = AuditTrail()
        self._online_banking = OnlineBanking(self)
    
    def add_customer(self, customer: Customer) -> bool:
        if customer._customer_id not in self._customers:
            self._customers[customer._customer_id] = customer
            self._audit_trail.log_event("Customer", "New customer added", customer._customer_id)
            return True
        return False
    
    def create_account(self, customer_id: str, account_type: str, initial_balance: float = 0.0) -> Optional[Account]:
        if customer_id not in self._customers:
            return None
        
        account_number = f"ACCT{random.randint(100000, 999999)}"
        
        if account_type == "savings":
            account = SavingsAccount(account_number, customer_id, initial_balance)
        elif account_type == "current":
            account = CurrentAccount(account_number, customer_id, initial_balance)
        else:
            return None
        
        self._accounts[account_number] = account
        self._customers[customer_id].add_account(account)
        self._audit_trail.log_event("Account", f"New {account_type} account created", customer_id)
        return account
    
    def get_account(self, account_number: str) -> Optional[Account]:
        return self._accounts.get(account_number)
    
    def transfer(self, from_account: str, to_account: str, amount: float) -> bool:
        source = self.get_account(from_account)
        destination = self.get_account(to_account)
        
        if source and destination and source.withdraw(amount):
            if destination.deposit(amount):
                self._audit_trail.log_event("Transfer", f"Transfer of {amount} from {from_account} to {to_account}", "System")
                return True
            else:
                # Rollback if deposit fails
                source.deposit(amount)
        return False
    
    def __str__(self) -> str:
        return f"Bank: {self._name}, Customers: {len(self._customers)}, Accounts: {len(self._accounts)}"

# -------------------- Demonstration --------------------
if __name__ == "__main__":
    # Create a bank
    my_bank = Bank("Python Savings Bank")
    
    # Create customers
    customer1 = Customer("CUST1001", "John Doe", "john@example.com", "555-1234")
    customer2 = Customer("CUST1002", "Jane Smith", "jane@example.com", "555-5678")
    
    my_bank.add_customer(customer1)
    my_bank.add_customer(customer2)
    
    # Create accounts
    john_savings = my_bank.create_account("CUST1001", "savings", 1000.0)
    john_current = my_bank.create_account("CUST1001", "current", 500.0)
    jane_savings = my_bank.create_account("CUST1002", "savings", 1500.0)
    
    # Perform transactions
    john_savings.deposit(200.0)
    john_current.withdraw(100.0)
    my_bank.transfer(john_savings.account_number, jane_savings.account_number, 300.0)
    
    # Create a loan
    john_loan = Loan("LOAN2001", "CUST1001", 5000.0, 0.05, 12)
    my_bank._loans[john_loan._loan_id] = john_loan
    
    # Create a credit card
    john_cc = CreditCard("4111111111111111", "CUST1001", 5000.0, "12/25")
    my_bank._credit_cards[john_cc._card_number] = john_cc
    
    # Demonstrate polymorphism
    accounts: List[Account] = [john_savings, john_current, jane_savings]
    for account in accounts:
        print(f"Withdrawing from {type(account).__name__}:")
        account.withdraw(100.0)
        print(f"New balance: {account.balance}\n")
    
    # Generate a report
    print(ReportGenerator.generate_account_statement(john_savings))
    
    # Check compliance
    print(f"KYC check for John: {ComplianceChecker.check_kyc(customer1)}")
    
    # Show bank status
    print(my_bank)
