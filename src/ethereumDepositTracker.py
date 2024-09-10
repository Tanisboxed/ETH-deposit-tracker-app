import time
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
import logging
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

Beacon_Deposit_Contract = "0x00000000219ab540356cBB839Cbe05303d7705Fa"

with open('Beacon_Deposit_Contract.json','r') as abi_file:
    Beacon_Deposit_ABI = json.load(abi_file)

GETH_WS_URL = os.getenv('GETH_WS_URL', 'ws://localhost:8546')
w3= Web3(Web3.WebsocketProvider(GETH_WS_URL)) #connecting to geth node

w3.middleware_onion.inject(geth_poa_middleware, layer=0)

class EthereumDepositTracker:
    def __init__(self):
        if not w3.isConnected():
            raise Exception("Unable to connect to Geth node")
        logger.info(f'Connected to Ethereum node. Chain ID: {w3.eth.chain_id}')
        self.deposit_contract = w3.eth.contract(
            address= Beacon_Deposit_Contract,
            abi=Beacon_Deposit_ABI
        )
        #connecting to PostgreSQL
        self.conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST','localhost'),
            database=os.getenv('POSTGRES_DB','ethereumdb'),
            user=os.getenv('POSTGRES_USER','tanisha'),
            password=os.getenv('POSTGRES_PASSWORD','tanu2004'),
            port=os.getenv('POSTGRES_PORT',5432)
        )
        self.cur=self.conn.cursor()
        logger.info("Connected to PostgreSQL database")

        
    def track_deposits(self):
        logger.info("Tracking deposits..")
        deposit_filter = self.deposit_contract.events.DepositEvent.create_filter(fromBlock='latest')
        while True:
            try:
                for event in deposit_filter.get_new_entries():
                    self.process_deposits(event)
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error in tracking the deposits: {e}")
                time.sleep(5) #time before retrying


    def process_deposits(self, event):
        try:
            transaction=w3.eth.get_transaction(event['transactionHash'])
            receipt=w3.eth.get_transaction_receipt(event['transactionHash'])
            fee= receipt['gasUsed'] * transaction['gasPrice']
            deposit = {
                'blockNumber':event['blockNumber'],
                'blockTimestamp':w3.eth.get_block(event['blockNumber'])['timestamp'],
                'hash' : event['transactionHash'].hex(),
                'pubkey': '0x' + event['args']['pubkey'].hex(),
                'fee': w3.from_wei(fee,'ether')
            }
            self.save_deposit(deposit)
            logger.info(f"New deposit Processed: {deposit}")
        except Exception as e:
            logger.error(f"Error processing deposit event: {e}")
        
    def save_deposit(self, deposit):
        try: 
            insert_query = """
                INSERT INTO deposits (block_number, block_timestamp, fee, hash, pubkey)
                VALUES (%s, to_timestamp(%s), %s, %s, %s)
            """
            self.cur.execute(insert_query, (
                deposit['blockNumber'],
                deposit['blockTimestamp'],
                deposit['fee'],
                deposit['hash'],
                deposit['pubkey']
            ))
            self.conn.commit()
            logger.info(f"Deposit saved : {deposit['hash']}")
        except Exception as e:
            logger.error(f"Error while saving deposit to db: {e}")
            self.conn.rollback()

if __name__ == "__main__":
    tracker = EthereumDepositTracker()
    tracker.track_deposits()
