#Project:4/////////////////////////////////////////////////////////////////////////////////////////////
#ATM

import os
os.system('cls')

from datetime import datetime
accounts=[]    
class Account():
    def __init__(self,acc_no,acc_holder_name,pin,balance):
        self.acc_no=acc_no
        self.acc_holder_name=acc_holder_name
        self.pin=pin
        self.balance=balance
        self.history=[]
    
    def check_your_account_detail(self):
        print(f"Account No:{self.acc_no}")
        print(f"Account Holder Name:{self.acc_holder_name}")
        print(f"Your balance:{self.balance}\n")

    def check_balance(self):
        print(f"Your current balance :{self.balance}\n")

    def deposit(self,amount):
        if(amount<=0):
            print("Invalid amount\n")
        else:
            self.balance+=amount
            self.history.append(f"{datetime.now()}:Deposited amount: {amount}")
            print(f"Your {amount} deposit successfully \n")

    def with_draw(self,amount):
        if(amount>self.balance):
            print("Your current balance is low=",self.balance)
        else:
            self.balance-=amount
            print(f"your remaining balance:{self.balance}\n")
            self.history.append(f"{datetime.now()}:Withdraw: {amount}")

    def change_pin(self):
        attempt=3
        while attempt>0:
            
            old_pin=int(input("enter old pin: "))
            if self.pin==old_pin:
                new_pin=int(input("enter new pin: "))
                self.pin=new_pin
                self.history.append(f"{datetime.now()}:Pin Changed")
                print("your account passoward is change successfully\n")
                return
            else:
                attempt-=1
                print(f"you have left{attempt}\n")
        print("Pin change failed\n")

    def show_history(self,all=False):
        if(len(self.history)==0):
            print("No Transaction yet\n")
        else:
            print("....Last Transaction....")
            data=self.history if all else self.history[-5:]
            for h in data:
                print("-",h)
                print()

    def transfer_money(self,receipt_acc_no,amount):
        
        receipt=None

        for a in accounts:
            if a.acc_no==receipt_acc_no:
                receipt=a
                
                break
       
        if receipt==None:
            print("Account Not Find\n")
            return
        
        if receipt.acc_no==self.acc_no:
            print("Amount cannot tranfer to your account\n")
            return
        
        if amount<=0:
            print("Invalid amount enter\n")
            return 
        
        if isinstance(self,saving_account) and (self.balance-amount<1000):
            print("INsufficient balance:Minimum balance required 1000\n")
            return
        elif isinstance(self,current_account) and (self.balance-amount<-5000):
            print("Insufficient balance:Overdraft limit exceeded\n")
            return 
        
        self.balance-=amount
        receipt.balance+=amount

        self.history.append(f"{datetime.now()}:Transferred {amount} to {receipt.acc_holder_name}")
        receipt.history.append(f"{datetime.now()}: Received {amount} from {self.acc_holder_name}")

        save_account(accounts)

        print(f"Successfully transferred {amount} to {receipt.acc_holder_name}\n")       
#Saving Account
class saving_account(Account):
    def with_draw(self,amount):
        if self.balance -amount < 1000:
            print("Minimum balance requires 1000\n")
        else:
            self.balance-=amount
            self.history.append(f"{datetime.now()}:withdraw amount:{amount}")
            print("Amount withdraw successfully\n")

#For Current Account
class current_account(Account):
    def with_draw(self, amount):
       if self.balance-amount<-5000:
           print("Overdraft limit exceed\n")
       else:
           self.balance-=amount
           self.history.append(f"{datetime.now()}:Withdraw amount:{amount}")

#Create New Account
def create_new_account():

    print("1.For saving account")
    print("2.For current account")

    acc_type=int(input("enter account type: "))

    x=int(input("enter how much account you want to create: "))

    for i in range(1,x+1):
        print(f"Account no {i} info")
        acc_no=int(input("enter account no: "))
        acc_holder_name=input("enter name: ")
        pin=int(input("enter pin: "))
        balance=int(input("enter balance: "))

        if(acc_type==1):
            a = saving_account(acc_no, acc_holder_name, pin, balance)
        else:
            a = current_account(acc_no, acc_holder_name, pin, balance)

        accounts.append(a)

    save_account(accounts)

    print("Your account is created successfully\n")

#Write Account To File
def save_account(accounts):
    with open("ATM Project File.txt","w") as f:
        for a in accounts:
            if isinstance(a,saving_account):
                acc_type="saving account"
            else:
                acc_type="current account"

            history_str="|".join(a.history)

            f.write(f"{a.acc_no},{a.acc_holder_name},{a.pin},{a.balance},{acc_type},{history_str}\n") 

#Load Account At the Start From File In accounts List 
def load_accounts():
    accounts.clear()
    try:
        with open("ATM Project File.txt","r") as f:
            for line in f:
                line = line.strip()

                if line == "":
                    continue   

                parts = line.split(",")

                if len(parts) < 5:
                    continue   

                acc_no, name, pin, balance,acc_type= parts[:5]

                history_str=",".join(parts[5:])
                history_list=history_str.split("|") if history_str else[]

                if(acc_type=="saving account"):

                    acc = saving_account(int(acc_no), name, int(pin), int(balance))
                else:
                    acc=current_account(int(acc_no), name, int(pin), int(balance))

                acc.history=history_list

                accounts.append(acc)

    except FileNotFoundError:
        pass

load_accounts()       
   
#Login Logic
def login():
    
    acc_no=int(input("enter account No: "))
    for a in accounts:
        if a.acc_no==acc_no:
            attempt=3
            while attempt >0:
                pin=int(input("enter pin: "))
                if a.pin==pin:
                    user_menu(a)
                    return
                else:
                    attempt-=1
                    print(f"Wrong Pin:Try Left:{attempt} ")
            print("Account Looked due to wrong pin\n") 
            return
    print("Account not found\n") 

#Usermenu
def user_menu(a):
    while True:
                    
        print("1.Check Balance")
        print("2.For Withdraw")
        print("3.For Deposit")
        print("4.For Change Pin")
        print("5.For check your account detailed")
        print("6.To check history")
        print("7.For transfer money")
        print("8.For Logout\n")

        ch=int(input("enter your choice: "))

        if(ch==1):
            a.check_balance()
        elif(ch==2):
            amount=int(input("enter amount to withdraw: "))
            a.with_draw(amount)
            save_account(accounts)
        elif(ch==3):
            amount=int(input("enter amount to deposit: "))
            a.deposit(amount)
            save_account(accounts)
        elif(ch==4):
            a.change_pin()
            save_account(accounts)
        elif(ch==5):
            a.check_your_account_detail()
        elif(ch==6):
            show_all=input("Show full history?(Y/N):").lower()=='y'
            a.show_history(all=show_all)
        elif(ch==7):
            receipt_acc_no=int(input("enter receipt number: "))
            amount=int(input("enter amount to transfer: "))
            a.transfer_money(receipt_acc_no,amount)
        elif(ch==8):
            print("Logged out\n")
            break
        else:
            print("Invalid choice\n")

#Admin TO View Account
def view_account(accounts):
    if len(accounts)==0:
        print("No Account Found")
    else:
        print("Account_No|Name|Balance|History")
        for a in accounts:
            print(f"{a.acc_no},{a.acc_holder_name},{a.balance},{a.history[-1:]}")

#Delete Account
def delete_acoount():
    if(len(accounts)==0):
        print("No Account Find")
        return
    
    acc_no=int(input("enter account no:(To delete it): "))
    for a in accounts:
        if a.acc_no==acc_no:
            accounts.remove(a)
            save_account(accounts)
            print("Account Deleted Successfully")
            break
        else:
            print("Account not found")

#Admin Mainmenu
adminpassword=123
def admin_panel_menu():
    global adminpassword
    
    print("....Welcome To Admin Panel.....\n")
    while True:
        
        print("1.For View All account")
        print("2.Create New Account")
        print("3.For Change Admin Password")
        print("4.Delete Account")
        print("5.To Logout\n")

        ch=int(input("enter your choice: "))
        if(ch==1):
            view_account(accounts)
        elif(ch==2):
            create_new_account()
        elif(ch==3):
            old_pin=int(input("enter old pin: "))
            new_pin=int(input("enter new pin: "))
            if adminpassword==old_pin:
                adminpassword=new_pin
                print("Admin Password Change Successfully\n")
            else:
                print("Invalid old passward\n")
        elif(ch==4):
            delete_acoount()
        elif(ch==5):
            return
        else:
            print("invalid choice\n")

#Program Start
while True:
        
    print("1.For User")
    print("2.For Admin Panel")
    print("3.For Exit\n")

    ch=int(input("enter your choice: "))

    if(ch==1):
        login()     
    elif(ch==2):
            attempt=3
            while attempt>0:
                pin=int(input("enter (Admin)pin:"))
                if(pin==adminpassword):
                    admin_panel_menu()
                    break
                else:
                    attempt-=1
                    print("Wrong! Pin")
                    print(f"You have left {attempt} attempt\n")
            print("Invalid pin\n")
            continue
    elif(ch==3):
        print("Thank you\n")
        break
    else:
        print("Invalid choice\n")         