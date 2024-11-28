# InvestAssistant

# WIP

# Database

## Key Entities and Relationships

**Instrument**:
Represents the financial product being traded (e.g., stock, ETF, crypto). Each instrument has a ticker and a current price.

**Profile** (or User):
Represents a user or investor, who can make multiple transactions and hold multiple investments.

**Transaction**:
Represents an individual buy/sell action by the user for a particular instrument. It records details such as the quantity, price per unit, and transaction type (buy or sell).

**Investment**:
Represents the user's aggregated position in a specific instrument, including fields like total position, average price, and market value.

## Database Schema

Profile/User
   └──> has many Transactions
   └──> has many Investments

Instrument
   └──> has many Transactions
   └──> has many Investments

Transaction
   └──> belongs to one Profile
   └──> belongs to one Instrument

Investment
   └──> belongs to one Profile
   └──> belongs to one Instrument


## How It Works Together

Instrument:
Holds information like ticker and current_price.

Profile:
Represents the user and is linked to Django's User model.

Transaction:
Tracks every individual buy/sell for a user in an instrument.

Investment:
Tracks the user's current position in an instrument and updates when a new transaction is made.
