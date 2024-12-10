# InvestAssistant

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
* The **Profile** is the central entity, linked to many other entities like **Transactions**, **Investments**, and *
  *CashTransactions**.

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