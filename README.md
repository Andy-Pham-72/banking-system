# Banking-system
Python OOP - Banking System Case Study in Python.

<img width="919" alt="Screen Shot 2021-09-02 at 5 13 06 PM" src="https://user-images.githubusercontent.com/70767722/131917196-200d6e84-ef4d-4eac-b4d6-c268dd6a9054.png">

In this project, I created a simple version of a banking system which I incorporate some **Python fundamental skills**: inheritance, exception handling, logging, getter and setter methods along with **SQL database** that associates with the Python script in order to produce the csv as a type of data storage.

We can easily run the .py file in the command line in order to experience the app locally.

All the classes, methods, and functions are documented with docstring comments.

The project consists of 3 main files and 1 log file:
* 1. **[banking_system.py](https://github.com/Andy-Pham-72/banking-system/blob/master/banking_system_application/banking_system.py)** - source code to run the application
* 2. **[banking_system.sql](https://github.com/Andy-Pham-72/banking-system/blob/master/banking_system_application/bankproject.sql)** - MySql database script
* 3. **[config.json](https://github.com/Andy-Pham-72/banking-system/blob/master/banking_system_application/config.json)** - MySql configuration json file
* 4. **[unknown_bank_management.log](https://github.com/Andy-Pham-72/banking-system/blob/master/data/unknown_bank_management.log)** - an example of logging

**The classes UML diagram**

![classes banking_system](https://user-images.githubusercontent.com/70767722/131917227-81c795f1-1713-4401-9c72-943c8e1e7577.png)

**The EER Diagram of the `bankingsys` schema**

![Screen Shot 2021-09-05 at 11 54 21 AM](https://user-images.githubusercontent.com/70767722/132133235-fbaa7328-bb50-4b71-b4b5-95363bb64233.png)

**The User interface in the command line:**

**Main Menu**

![Screen Shot 2021-09-02 at 4 53 43 PM](https://user-images.githubusercontent.com/70767722/131917265-51c81e77-0382-4a8f-b7f0-c9f509202e90.png)

**Transaction Menu**

![Screen Shot 2021-09-02 at 4 52 29 PM](https://user-images.githubusercontent.com/70767722/131917246-5dd64f80-4d24-476a-bd2d-9076a2c7e443.png)

**Account Information example**

![Screen Shot 2021-09-02 at 4 52 09 PM](https://user-images.githubusercontent.com/70767722/131917278-0e5e089f-8f0c-4398-b6cb-1f0c81fe85ba.png)

## Requirements:
I used MySQL as the database management system and you also need to install `mysql_connector_repackage` in order to use Python script to connect with the MySql server. Please check this [link for the installing instruction](https://dev.mysql.com/doc/connector-python/en/connector-python-installation-binary.html)

For Mac user:

```
shell> pip install mysql-connector-python
```

For Windows user:

```
shell> msiexec /i mysql-connector-python-VER-pyPYVER.msi
```

## Future works:
* The `banking_system.py` script still has some flaws in terms of the syntax, exception handling and logical issue that will be updated and fixed along the way. Any comments and suggestions are very appreciated! I am still learning, Thanks All!

* I want to add more features for the banking system; for example: 
    - `Search Menu` (using account number, email, phone number, first name, or last name to list the corresponding customer information),
    - `Daily and Monthly Reports` to show the updated account information, 
    - `Account Adjustment` to change or update account information by using the account number.
    - `Payment Method` to save the transaction payment record with different types of payment (Visa, Master, Paypal). 

## Any code comments and contributions are very welcome!
If you have any question please reach me out through my personal email: [aqpham02@gmail.com]

Cheers!
