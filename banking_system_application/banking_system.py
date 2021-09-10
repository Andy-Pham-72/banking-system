import mysql.connector
from datetime import date
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

    # def execute(self, sql):
    #     """Implements execute function"""
    #     self.cursor.execute(sql)
    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

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

            sql = "INSERT INTO customer(first_name, last_name, dob, phone, email, acc_type, status, balance) VALUES \
                    (%s, %s, %s, %s, %s, %s, 'active', %s);"

            self.execute(sql,(self.first_name, 
                              self.last_name, 
                              self.dob, 
                              self.phone, 
                              self.email, 
                              self.acc_type, 
                              self.balance))
            print('New customer added successfully!\n\n')

        except TypeError as err:
            print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error("Invalid input. An error message: {} from create_account()".format(err))
            # Back to main menu
            self.main_menu()
        except ValueError as err:
            print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error("Invalid input. An error message: {} in create_account()".format(err))
            # Back to main menu
            self.main_menu()
        except mysql.connector.errors.DataError as err:
            print("\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug("Invalid input. A debug message: {} from create_account()".format(err))
            # Back to main menu
            self.main_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug("Invalid input. A debug message: {} from create_account()".format(err))
            # Back to main menu
            self.main_menu()

    def account_status(self, acc_num):
        """method that returns account status and balance"""

        try:
            self.acc_num = acc_num
            sql = "SELECT status, balance FROM customer WHERE acc_no = %s;" % self.acc_num
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
            
            sql1 = "SELECT status FROM customer WHERE acc_no = %s;" % self.acc_num
            self.execute(sql1)
            result = self.fetchall()
            
            if len(result) < 1:
                print("\nAccount number {} does not exist in the database.\nPlease try again!\n".format(self.acc_num))
                # Log
                logger.error("Invalid input: Account number '{}' does not exist in the database.".format(self.acc_num))
            else:
                sql2 = "UPDATE customer SET status = 'close' WHERE acc_no = %s;" % self.acc_num
                self.execute(sql2)
                print("Account Closed!")
            
        except ValueError as err:
            print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error("Invalid input: '{}' . An error message: {} in close_account()".format(self.acc_num,err))
            # Back to main menu
            self.main_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug("Invalid input: '{}'. A debug message: {} from close_account()".format(self.acc_num,err))
            # Back to main menu
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
                sql1 = " UPDATE customer SET balance = balance + %s \
                        WHERE acc_no = %s AND status = 'active' ;" % (self.amount, self.acc_num)
                sql2 = " INSERT INTO transaction(date,amount,type,acc_no) \
                        VALUES (%s, %s, 'deposit', %s) ; "
                self.execute(sql1)
                self.execute(sql2, (today, self.amount, self.acc_num))
                print("\n\nAmount Deposited!")

            else:
                print("\n\nClosed or Suspended Account!")
            self.wait = input("\n\n\nPress enter key to continue....")
            self.transaction_menu()

        except ValueError as err:
            print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error("Invalid input: with the amount: '{}' and the account number: '{}'. \
                        An error message: {} in deposit_amount()".format(self.amount,self.acc_num,err))
            # Back to transaction menu
            self.transaction_menu()
        except TypeError as err:
            print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error("Invalid input: with the amount: '{}' and the account number: '{}'. \
                        An error message: {} in deposit_amount()".format(self.amount,self.acc_num,err))
            # Back to transaction menu
            self.transaction_menu()
        except mysql.connector.errors.DataError as err:
            print("\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug("Invalid input. A debug message: {} from create_account()".format(err))
            # Back to main menu
            self.transaction_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input associating with MySql syntax: {}! \
                    \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug("Invalid input: for the amount: '{}' and the account number: '{}'. \
                        A debug message: {} in deposit_amount()".format(self.amount,self.acc_num,err))
            # Back to transaction menu
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
                sql1 = " UPDATE customer SET balance = balance - %s \
                        WHERE acc_no = %s AND status = 'active' ;" % (self.amount, self.acc_num)
                sql2 = " INSERT INTO transaction(date, amount, type, acc_no) \
                        VALUES (%s, %s, 'withdraw', %s) ; "

                self.execute(sql1)
                self.execute(sql2, (today, self.amount, self.acc_num))
                print('\n\nAmount Withdrawn!')
            elif result[0] == 'close':
                print('\n\nClosed or Suspended Account!')
            else:
                print('\n\nInsufficient balance!')

            self.wait = input('\n\n\nPress enter key to continue....')
            self.transaction_menu()

        except ValueError as err:
            print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error("Invalid input: for the amount: '{}' and the account number: '{}'. \
                        An error message: {} in withdraw_amount()".format(self.amount,self.acc_num,err))
            # Back to transaction menu
            self.transaction_menu()
        except TypeError as err:
            print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error("Invalid input: for the amount: '{}' and the account number: '{}'. \
                        An error message: {} in withdraw_amount()".format(self.amount,self.acc_num,err))
            # Back to transaction menu
            self.transaction_menu()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input associating with MySql syntax: {}! \
                    \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug("Invalid input: for the amount: '{}' and the account number: '{}'. \
                        A debug message: {} in withdraw_amount()".format(self.amount,self.acc_num,err))
            # Back to transaction menu
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
            sql1 = "SELECT * FROM customer WHERE acc_no = %s ;" % self.acc_num
            sql2 = "SELECT date, amount, type FROM transaction AS t WHERE t.acc_no = (%s) ;" % self.acc_num
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
            print(f"Account Status: {result[7]}")
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

        except ValueError as err:
            print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error("Invalid input: '{}' . An error message: {} in show_details()".format(self.acc_num,err))
            # Back to input acc_num
            self.show_details()
        except TypeError as err:
            print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
            # Log
            logger.error("Invalid input: '{}' . An error message: {} in show_details()".format(self.acc_num,err))
            # Back to input acc_num
            self.show_details()
        except mysql.connector.errors.ProgrammingError as err:
            print("\n*************\nInvalid input associating with MySql syntax: {}! \nPlease Try Again! \n*************\n\n".format(err))
            # Log
            logger.debug("Invalid input: '{}'. A debug message: {} from show_details()".format(self.acc_num,err))
            # Back to input acc_num
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
                elif option == 2:
                    self.show_details()
                elif option == 3:
                    self.close_account()
                elif option == 4:
                    self.transaction_menu()
                elif option == 5:
                    print("\n*****************\nSee You Next Time!\n*****************\n")
                    break

            except TypeError as err:
                print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
                # Log
                logger.error("Invalid input: '{}' - ValueError message: {} from main_menu() at".format(option, err))
                # Back to main menu
                self.main_menu()
            except ValueError as err:
                print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
                # Log
                logger.error("Invalid input: '{}' - ValueError message: {} from main_menu() at".format(option, err))
                # Back to main menu
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
            print('\n2.  Withdraw Amount')
            print('\n3.  Back to Main Menu')
            print('\n\n')
            try:
                option2 = int(input('Enter your option ...: '))
                if option2 == 1:
                    self.deposit_amount()
                if option2 == 2:
                    self.withdraw_amount()
                if option2 == 3:
                    self.main_menu()

            except TypeError as err:
                print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
                # Log
                logger.error("Invalid input: '{}' - ValueError message: {} from transaction_menu()".format(option2, err))
                # Back to transaction menu
                self.transaction_menu()
            except ValueError as err:
                print("\n*************\nInvalid input!\n*************\nPlease try again!\n")
                # Log
                logger.error("Invalid input: '{}' - ValueError message: {} from transaction_menu()".format(option2, err))
                # Back to transaction menu
                self.transaction_menu()


if __name__ == '__main__':
    run_application = UnknownBank()