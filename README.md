# InvestAssistant

InvestAssistant is a Django-based financial tracking platform built on the Model-View-Template (MVT) architecture. It enables users to manage investments across various instruments like stocks, ETFs, and cryptocurrencies. The application provides comprehensive portfolio management with features for tracking holdings, transaction history, and unrealized profits or losses.

## Features

- **User Management**: Create profiles and manage account information
- **Investment Tracking**: Monitor holdings across multiple investment instruments
- **Transaction Management**: Record buy/sell transactions with automatic portfolio updates
- **Cash Management**: Track deposits and withdrawals with accurate balance calculations
- **Portfolio Analytics**: View cost basis, market value, and return on investment metrics

## Technology Stack

- **Framework**: Django (MVT architecture)
- **Database**: SQLite (development) / PostgreSQL (production-ready)
- **Frontend**: Django Templates with Bootstrap
- **Authentication**: Django's built-in authentication system

## Setup

1. Clone this repository
   ```
   git clone https://github.com/kaweeo/InvestAssistant
   ```

2. Create and activate virtual environment
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies
   ```
   pip install -r requirements.txt
   ```

4. Run migrations
   ```
   python manage.py migrate
   ```

5. Start the development server
   ```
   python manage.py runserver
   ```

6. Access the application at http://127.0.0.1:8000/

## Architecture

### Model-View-Template (MVT) Pattern

InvestAssistant follows Django's MVT architectural pattern:

- **Models**: Define data structure and business logic
- **Views**: Process user requests and return responses
- **Templates**: Render data in HTML format for the client

### Database Schema

- **Profile/User** → has many Transactions → has many Investments
- **Instrument** → has many Transactions → has many Investments
- **Transaction** → belongs to one Profile → belongs to one Instrument
- **Investment** → belongs to one Profile → belongs to one Instrument
- **CashTransaction** → belongs to one Profile

## System Components

### 1. User and Profile

- A **User** creates a **Profile** with personal details and account balance
- The **Profile** serves as the central entity linked to transactions and investments

### 2. Transactions (Buy/Sell)

- **Buy Transaction**:
  - Reduces the user's balance by the transaction value
  - Creates or updates an Investment record
- **Sell Transaction**:
  - Increases the user's balance by the transaction value
  - Updates the Investment record to reflect reduced holdings

### 3. Investment

- Represents a user's holdings in a specific instrument
- Tracks total quantity and average acquisition price
- Provides methods for calculating current value and performance metrics

### 4. Portfolio

- Consolidates all investments for a comprehensive view
- Calculates performance metrics including:
  - Total market value
  - Cost basis
  - Unrealized profit/loss
  - Return on investment

### 5. Cash Transactions

- Manages deposits and withdrawals
- Updates the user's balance accordingly
- Maintains a history of all cash movements

## Screenshots

### User Registration
![create-user](https://github.com/kaweeo/InvestAssistant/blob/main/description/not-logged-in.png)

### Portfolio Overview
![portfolio](https://github.com/kaweeo/InvestAssistant/blob/main/description/portfolio.png)

### Transaction History
![transaction](https://github.com/kaweeo/InvestAssistant/blob/main/description/transactions.png)
