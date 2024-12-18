# InvestAssistant

InvestAssistant is a financial tracking platform that allows users to manage their investments in various instruments
like stocks and bonds. Users can create profiles, perform buy and sell transactions, and track their portfolio, which
includes holdings, transaction history, and unrealized profits or losses. The platform also manages cash deposits and
withdrawals, ensuring users have accurate balances for trading. InvestAssistant provides a complete solution for
investment management and financial tracking.

## Set up

1. Clone this repository
   `git clone https://github.com/kaweeo/InvestAssistant`
2. Open the project
3. Create venv
   `python -m venv venv`
4. Install dependencies
   `pip install -r requirements.txt`
5. Set up the database
6. Run the migrations
   `python manage.py migrate`
7. Run the project

python manage.py runserver

## Database Schema

Profile/User └──> has many Transactions └──> has many Investments

Instrument └──> has many Transactions └──> has many Investments

Transaction └──> belongs to one Profile └──> belongs to one Instrument

Investment └──> belongs to one Profile └──> belongs to one Instrument

CashTransaction └──> belongs to one Profile

---

## How It Works Together

### 1. User and Profile

* A **User** creates a **Profile** that holds additional details like name, phone number, and balance.
* The **Profile** is the central entity, linked to many other entities like **Transactions**, **Investments**, and **CashTransactions**.

### 2. Transactions (Buy/Sell)

* When a user buys or sells an instrument, a **Transaction** is created.
    * **Buy Transaction:**
        - The user's **Profile** balance is reduced by the total transaction value (quantity * price per unit).
        - An **Investment** record is created or updated to track the user's holdings in the instrument.
    * **Sell Transaction:**
        - The user's **Profile** balance is increased by the transaction value.
        - The **Investment** record is updated to reflect the reduced quantity.

### 3. Investment

* An **Investment** record represents the user's holdings in a specific instrument.
* It tracks the **total_quantity** of the instrument owned and the **avg_price** at which the instrument was acquired.
* Each **Investment** is associated with a **Profile**.
* The **Investment** is updated with each buy or sell transaction to maintain accurate information about the user's
  holdings.

### 4. Portfolio

* The **Portfolio** provides a consolidated view of a user's investments.
* It aggregates all **Transactions** and **Investments** to calculate the current holdings.
* For each instrument, it calculates the net position, average acquisition price, and unrealized profit/loss.
* The portfolio is updated dynamically as new transactions occur.

By effectively managing these entities, the system ensures accurate tracking of user investments, provides valuable
insights into portfolio performance, and facilitates smooth execution of buy and sell transactions.

### 5. CashTransactions

* CashTransactions handle the movement of funds in and out of a user’s account.
* Deposit: When a user deposits funds, a CashTransaction of type "Deposit" is created. This increases the Profile
  balance.
* Withdrawal: When a user withdraws funds, a CashTransaction of type "Withdrawal" is created. This decreases the Profile
  balance.
  
###
![create-user](https://github.com/kaweeo/InvestAssistant/blob/main/description/not-logged-in.png)

###
![portfolio](https://github.com/kaweeo/InvestAssistant/blob/main/description/portfolio.png)

###
![transaction](https://github.com/kaweeo/InvestAssistant/blob/main/description/transactions.png)
