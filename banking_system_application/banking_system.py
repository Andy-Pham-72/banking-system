import mysql.connector
from datetime import date, datetime
import logging

# Creates a logger
logger = logging.getLogger(__name__)

# set logger level
logger.setLevel(logging.DEBUG)

# define file handler and set formatter
file_handler = logging.FileHandler('unknown_bank_management.log')
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)

# add file handler to logger
logger.addHandler(file_handler)


class SqlFuncs:
    """class SqlFuncs is created to access the essential mysql.connector's functions"""

    def __init__(self):
        self._conn = mysql.connector.connect(host='localhost', user='root', database='bankingsys',
                                             passwd='rootroot')  # use your password here
        self._cursor = self._conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def execute(self, sql):
        """Implements execute function"""
        self.cursor.execute(sql)

    def commit(self):
        """Implements commit function"""
        self.connection.commit()

    def fetchall(self):
        """Implements fetchall function"""
        return self.cursor.fetchall()

    def fetchone(self):
        """Implement fetchone function"""
        return self.cursor.fetchone()

    def close(self, commit=True):
        """Implement close function"""
        if commit:
            self.commit()
        self.connection.close()


class UnknownBank(SqlFuncs):
    """
    UnknownBank is a basic Banking system application that consists of some essential banking transactions
    1. Create Banking Account
    2. Deposit Amount
    3. Withdraw Amount
    4. Close Account
    5. Account Details (Customer information, Balance and Account type)
    """

    global logger

    def __init__(self):
        super().__init__()
        self.main_menu()

    def create_account(self):
        """
        method that creates a new account.

        *************
        Input example
        *************

        first_name = str()
        last_name = str()
        dob = yyyy-mm-dd
        phone = ***-***-**** (eg: 123-456-7890)    
        email = str()
        acc_type = saving / checking
        balance = int()
        """

        try:
            self.first_name = input("Enter the account holder first name : ")
            self.last_name = input("Enter the account holder last name : ")
            self.dob = input("Enter the account holder date of birth : ")
            self.phone = input("Enter the account holder phone number: ")
            self.email = input("Enter the account holder email: ")
            self.acc_type = input("Account type (saving/checking): ")
            self.balance = input("Enter opening balance: ")

            sql = f""" INSERT INTO customer(first_name, last_name, dob, phone, email, acc_type, status, balance) VALUES 
                    ('{self.first_name}','{self.last_name}','{self.dob}','{self.phone}','{self.email}','{self.acc_type}',
                    'active',{self.balance}
                     );"""

            self.execute(sql)
            print('New customer added successfully!\n\n')
        except SyntaxError:
            print("\n*************\nInvalid input! \nPlease Try Again!\n*************\n\n")
            # Log
            logger.error(f'An error message: SyntaxError in create_account()')
            self.main_menu()
        except ValueError:
            print("\n*************\nInvalid input! \nPlease Try Again! \n*************\n\n")
            # Log
            logger.error(f'An error message: ValueError in create_account()')
            self.main_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug(f'A debug message: {err} from create_account()')
            self.main_menu()

    def account_status(self, acc_num):
        """method that returns account status and balance"""

        try:
            self.acc_num = acc_num
            sql = f"""SELECT status, balance FROM customer WHERE acc_no = {self.acc_num};"""
            self.execute(sql)
            self._result = self.fetchone()
            return self._result
        except SyntaxError:
            print("\n*************\nInvalid input! \nPlease Try Again!\n*************\n\n")
            # Log
            logger.error(f'An error message: SyntaxError in account_status()')
            self.main_menu()
        except ValueError:
            print("\n*************\nInvalid input! \nPlease Try Again! \n*************\n\n")
            # Log
            logger.error(f'An error message: ValueError in account_status()')
            self.main_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug(f'A debug message: {err} from account_status()')
            self.main_menu()

    def close_account(self):
        """
        method that closes a customer account
        *************
        Input example
        *************

        acc_num = int()

        """

        try:
            self.acc_num = input("Enter Account Number: ")
            sql = f"""UPDATE customer SET status = "close" WHERE acc_no = {self.acc_num} ;"""
            self.execute(sql)
            print("Account Closed!")
        except SyntaxError:
            print("\n*************\nInvalid input! \nPlease Try Again!\n*************\n\n")
            # Log
            logger.error(f'A error message: SyntaxError in close_account()')
            self.main_menu()
        except ValueError:
            print("\n*************\nInvalid input! \nPlease Try Again! \n*************\n\n")
            # Log
            logger.error(f'A error message: ValueError in close_account()')
            self.main_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug(f'A debug message: {err} from close_account()')
            self.main_menu()

    def deposit_amount(self):
        """
        method that makes a deposit into an account
        """

        try:
            self.acc_num = input("Enter Account Number: ")
            self.amount = input("Enter Amount: ")
            today = date.today()
            result = self.account_status(self.acc_num)

            if result[0] == 'active':
                sql1 = f""" UPDATE customer SET balance = balance + {self.amount}
                       WHERE acc_no = {self.acc_num} AND status = "active" ; """
                sql2 = f""" INSERT INTO transaction(date,amount,type,acc_no) VALUES 
                        ("{today}", {self.amount}, "deposit", {self.acc_num}) ; """
                self.execute(sql1)
                self.execute(sql2)
                print("\n\nAmount Deposited!")

            else:
                print("\n\nClosed or Suspended Account!")
            self.wait = input("\n\n\nPress enter key to continue....")

        except SyntaxError:
            print("\n*************\nInvalid input! \nPlease Try Again!\n*************\n\n")
            # Log
            logger.error(f'An error message: SyntaxError in deposit_amount()')
            self.transaction_menu()
        except ValueError:
            print("\n*************\nInvalid input! \nPlease Try Again! \n*************\n\n")
            # Log
            logger.error(f'An error message: ValueError in deposit_amount()')
            self.transaction_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug(f'A debug message: {err} from deposit_amount()')
            self.transaction_menu()

    def withdraw_amount(self):
        """
        method that withdraws an amount from customer account by their account number
        *************
        Input example
        *************

        acc_num = int()
        amount = int()
        """

        try:
            self.acc_num = input("Enter Account Number: ")
            self.amount = input("Enter Amount: ")
            today = date.today()
            result = self.account_status(self.acc_num)

            if result[0] == 'active' and int(result[1]) >= int(self.amount):
                sql1 = f""" UPDATE customer SET balance = balance - {self.amount} 
                        WHERE acc_no = {self.acc_num} AND status = "active" ;"""
                sql2 = f""" INSERT INTO transaction(date, amount, type, acc_no)
                        VALUES ( "{today}", {self.amount} , "withdraw" , {self.acc_num} ); """

                self.execute(sql1)
                self.execute(sql2)
                print('\n\nAmount Withdrawn!')
            elif result[0] == 'close':
                print('\n\nClosed or Suspended Account!')
            else:
                print('\n\nClosed or Suspended Account.Or Insufficient amount!')

            self.wait = input('\n\n\nPress enter key to continue....')

        except SyntaxError:
            print("\n*************\nInvalid input! \nPlease Try Again!\n*************\n\n")
            # Log
            logger.error(f'A error message: SyntaxError in withdraw_amount()')
            self.transaction_menu()
        except ValueError:
            print("\n*************\nInvalid input! \nPlease Try Again! \n*************\n\n")
            # Log
            logger.error(f'An error message: ValueError in withdraw_amount()')
            self.transaction_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug(f'A debug message: {err} from withdraw_amount()')
            self.transaction_menu()

    def show_details(self):
        """
        method that shows the customer account information
        *************
        Input example
        *************

        acc_num = int()
        """

        try:
            self.acc_num = input("Enter Account Number: ")
            sql1 = f"""SELECT * FROM customer WHERE acc_no = {self.acc_num} ;"""
            sql2 = f"""SELECT date, amount, type FROM transaction AS t WHERE t.acc_no = {self.acc_num} ;"""
            self.execute(sql1)
            result = self.fetchone()
            print("\n")
            print("Account Information")
            print("*" * 50)
            print(f"Account Number: {str(result[0])}")
            print(f"Customer Name: {result[1]} {result[2]}")
            print(f"Date of Birth: {str(result[3])}")
            print(f"Contact Number: {result[4]}")
            print(f"Customer Email: {result[5]}")
            print(f"Account Type: {result[6]}")
            print(f"Account Balance: $ {str(result[8])}")
            print("*" * 50)
            print("\n")

            self.execute(sql2)
            results = self.fetchall()
            print("**** Transaction History ****")
            if len(results) < 1:
                print("Customer has not made any transaction yet!")
            else:
                for result in results:
                    print(result[0],"$", result[1], result[2])
            self.wait = input('\n\n\nPress enter key to continue....')

        except SyntaxError:
            print("\n*************\nWrong input!\n*************\n")
            # Log
            logger.error(f'An error message: SyntaxError in show_details()')
            self.show_details()
        except ValueError:
            print("\n*************\nWrong input!\n*************\n")
            # Log
            logger.error(f'An error message: ValueError in show_details()')
            self.show_details()
        except mysql.connector.errors.ProgrammingError as err:
            logger.debug(f'A debug message: {err}')
            print("\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
            self.show_details()

    def main_menu(self):
        """
        method that shows the interface for all the banking options
        *************
        Input example
        *************
        option = 1/2/3/4/5

        """

        while True:
            print("\n----- MAIN MENU ----- ")
            print("\n1.  Create Account")
            print("\n2.  Account Details")
            print('\n3.  Close Account')
            print('\n4.  Transaction Menu')
            print('\n5.  Close application')
            print('\n\n')
            try:
                option = int(input('Enter your option ...: '))
                if option == 1:
                    self.create_account()
                if option == 2:
                    self.show_details()
                if option == 3:
                    self.close_account()
                if option == 4:
                    self.transaction_menu()
                if option == 5:
                    break

            except SyntaxError:
                print("\n*************\nWrong input!\n*************\n")
                # Log
                logger.error(f'An error message: SyntaxError in show_details()')
                self.main_menu()
            except ValueError:
                print("\n*************\nWrong input!\n*************\n")
                # Log
                logger.error(f'An error message: ValueError in show_details() at')
                self.main_menu()

    def transaction_menu(self):
        """
        method that shows all the transactional options
        *************
        Input example
        *************

        option = 1/2/3
        """

        while True:
            print("\n ----- TRANSACTION MENU ----- ")
            print("\n1.  Deposit Amount")
            print('\n2.  WithDraw Amount')
            print('\n3.  Back to Main Menu')
            print('\n\n')
            try:
                option = int(input('Enter your option ...: '))
                if option == 1:
                    self.deposit_amount()
                if option == 2:
                    self.withdraw_amount()
                if option == 3:
                    self.main_menu()

            except SyntaxError:
                print("\n*************\nWrong input!\n*************\n")
                # Log
                logger.debug(f'An error message: SyntaxError in show_details()')
                self.transaction_menu()
            except ValueError:
                print("\n*************\nWrong input!\n*************\n")
                # Log
                logger.debug(f'An error message: ValueError in show_details()')
                self.transaction_menu()


if __name__ == '__main__':
    run_application = UnknownBank()
