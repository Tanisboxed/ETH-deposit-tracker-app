# ETH-deposit-tracker-app
Ethereum Deposit Tracker is a tool designed to track deposists to Ethereum 2.0 Breacon Chain's deposit contract. It leverages Web3.py to connect to an Ethereum node via WebSocket, monitor new deposit events and save them to a PostgreSQL database for further analysis and reporting. Utilizing geth.

## Table of Contents
- Project Structure
- Features
- Prerequisites
- Setup
- Environment Variables
- Usage
- Docker Setup
- Troubleshooting
- Contributing
- License

### Project Structure

EthereumDepositTracker/
│
├── src/

│   └── ethereum_deposit_tracker.py    # Main Ethereum Deposit Tracker code

├── tests/

│   └── test_edt.py # Unit tests

├── docker/

│   ├── Dockerfile                     # Docker build instructions

│   └── docker-compose.yml              # Docker Compose for multi-container setup

├── geth-data/                         # Folder to store Ethereum node data (for Docker)

├── .env                               # Environment variables

├── requirements.txt                    # Python dependencies

├── README.md                          # Project documentation

├── .gitignore                          # Ignored files in Git


### Features:
- Tracks deposits made to the Ethereum 2.0 Beacon Deposit contract.
- Saves deposit information (pubkey, fee, etc.) to a PostgreSQL database.
- Runs in a Dockerized environment with an Ethereum Geth node.

### Prerequisites:
- Python 3.9+
- PostgreSQL
- Docker and Docker Compose
- Web3.py and associated dependencies

### Setup:
1. Clone the repo:
```
git clone https://github.com/Tanisboxed/ETH-deposit-tracker-app.git
cd EthereumDepositTracker
```

3. Create virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

4. Install dependences:
```
pip install -r requirement.txt
```

5. Configure environment variables:
   configure the following environment variables:
```
GETH_WS_URL=ws://localhost:8546
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=eth_deposits
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
TELEGRAM_BOT_TOKEN=7519483853:AAFQKVvOg6UhzOuLcdyzkLqqrH8si8XkBJ
```

#### PostGREsql Structure: 
![image](https://github.com/user-attachments/assets/71eede92-62f2-4bbf-95c0-76916d230b1b)

#### Telegram BOT TOKEN AQUIRED:
![image](https://github.com/user-attachments/assets/d43d31be-bb8c-4f51-81df-e42fbd23a093)

### Usage:
1. Running the Ethereum Deposit Tracker: pythono src/ethereum_deposit_tracker.py
2. Build and start the Docket container: docker-compose up --build
3. Running Tests: unittest tests/test_edt.py

### Troubleshooting
1. WebSocket URL Issue: Ensure WebSocket URL (GETH_WS_URL) is correct.
2. PostgreSQL Connection: Verify your PostgreSQL credentials and that the database is running

