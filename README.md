# InvestAssistant

## Database

### Key Entities and Relationships

1. **Instrument**:
   - **Description**: Represents the financial product being traded (e.g., stock, ETF, crypto). Each instrument has a ticker and a current price.
   - **Fields**:
     - `ticker`: Unique identifier for the instrument (e.g., AAPL for Apple stock).
     - `current_price`: The current price of the instrument.
   - **Relationships**:
     - One-to-many relationship with `Transaction` (a single instrument can have multiple transactions).
     - One-to-many relationship with `Investment` (a single instrument can be part of many user investments).

2. **Profile** (or User):
   - **Description**: Represents a user or investor who can make multiple transactions and hold multiple investments.
   - **Fields**:
     - `user`: A one-to-one link to the `User` model, which contains the user's personal details.
     - `balance`: The user's available cash balance for transactions.
   - **Relationships**:
     - One-to-many relationship with `Transaction` (a profile can have multiple transactions).
     - One-to-many relationship with `Investment` (a profile can hold many investments).
     - One-to-many relationship with `CashTransaction` (a profile can have many cash transactions).

3. **Transaction**:
   - **Description**: Represents an individual buy or sell action by the user for a particular instrument.
   - **Fields**:
     - `transaction_side`: Whether the transaction is a 'BUY' or 'SELL'.
     - `quantity`: The number of units of the instrument being bought or sold.
     - `price_per_unit`: The price per unit of the instrument at the time of the transaction.
     - `timestamp`: The time the transaction occurred.
   - **Relationships**:
     - Many-to-one relationship with `Profile` (a transaction belongs to a specific user).
     - Many-to-one relationship with `Instrument` (a transaction is for a specific instrument).

4. **Investment**:
   - **Description**: Represents the user's aggregated position in a specific instrument, including the total quantity, average price, and market value of the instrument held by the user.
   - **Fields**:
     - `total_quantity`: The total amount of the instrument held by the user.
     - `avg_price`: The average price at which the instrument was purchased.
   - **Relationships**:
     - Many-to-one relationship with `Profile` (an investment belongs to a specific user).
     - Many-to-one relationship with `Instrument` (an investment is in a specific instrument).

5. **CashTransaction**:
   - **Description**: Represents the cash deposited or withdrawn by the user. This modifies the user's balance.
   - **Fields**:
     - `transaction_flow`: Whether it is a 'DEPOSIT' or 'WITHDRAWAL'.
     - `amount`: The amount of money deposited or withdrawn.
     - `timestamp`: The time the cash transaction occurred.
   - **Relationships**:
     - Many-to-one relationship with `Profile` (a cash transaction is linked to a user).

---

### Database Schema

Profile/User └──> has many Transactions └──> has many Investments └──> has many CashTransactions

Instrument └──> has many Transactions └──> has many Investments

Transaction └──> belongs to one Profile └──> belongs to one Instrument

Investment └──> belongs to one Profile └──> belongs to one Instrument

CashTransaction └──> belongs to one Profile


---

### How It Works Together

1. **User and Profile**:
   - A `User` creates a `Profile` that holds additional details like the user's name, phone number, and balance. The `Profile` has many relationships with other entities like `Transactions`, `Investments`, and `CashTransactions`.

2. **Transactions (Buy/Sell)**:
   - When a user buys or sells an instrument, a `Transaction` is created. If it's a **buy transaction**, the `Profile`'s balance is reduced by the total transaction value (quantity * price per unit). If it's a **sell transaction**, the `Profile`'s balance is increased by the transaction value. The associated `Investment` record is updated or created to reflect the user's new holdings.

3. **Cash Transactions (Deposit/Withdrawal)**:
   - When a user deposits or withdraws cash, a `CashTransaction` record is created. If it's a **deposit**, the `Profile`'s balance increases. If it's a **withdrawal**, the balance decreases, as long as sufficient funds are available. This ensures the balance is correctly tracked and updated.

4. **Investment**:
   - Each time a buy transaction occurs, an associated `Investment` record is created (if one does not already exist). The `Investment` tracks how much of each instrument the user owns and the average price at which the instrument was acquired. The `total_quantity` and `avg_price` are updated on each buy transaction, ensuring the user's position is accurately represented.
