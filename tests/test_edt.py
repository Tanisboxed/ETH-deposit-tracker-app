import unittest 
from unittest.mock import patch, MagicMock
from src.EthereumDepositTracker import EthereumDepositTracker

class TestEthereumDepositTracker(unittest.TestCase):
    @patch('ethereum_deposit_tracker.w3')
    def setUp(self, mock_w3):
        mock_w3.isConnected.return_value= True
        mock_w3.eth.chain_id = 1
        self.tracker = EthereumDepositTracker()

    @patch('ethereum_deposit_tracker.w3')
    def test_conn(self,mock_w3):
        mock_w3.isConnected.return_value = True
        self.assertTrue(self.tracker.deposit_contract is not None)
    
    @patch('ethereum_deposit_tracker.w3')
    def test_track_deposits(self, mock_w3):
        mock_filter = MagicMock()
        mock_filter.get_new_entries.return_value= []

        self.tracker.deposit_contract.events.DepositEvent.create_filter.return_value = mock_filter
        with patch('time.sleep',return_value=None):
            self.tracker.track_deposits()
            mock_filter.get_new_entries.assert_called()
        
    @patch('ethereum_deposit_tracker.w3')
    def test_process_deposits(self,mock_w3):
        mock_event={
            'blockNumber': 123,
            'transactionHash': b'\x12\x34',
            'args':{
                'pubkey': b'\x12' * 48,
            }
        }
        mock_w3.eth.get_block.return_value = {'timestamp' : 1609459200}
        mock_w3.eth.get_transaction.return_value = {'gasPrice':1000000000}
        mock_w3.eth.get_transaction_receipt.return_value = {'gasUsed' :21000}

        with patch.object(self.tracker, 'save_deposit') as mock_save_deposit:
            self.tracker.process_deposits(mock_event)
            mock_save_deposit.assert_called_once()
            saved_deposit = mock_save_deposit.call_args[0][0]
            self.assertEqual(saved_deposit['fee'],0.021)
    
    @patch('ethereum_deposit_tracker.psycopg2.connect')
    def test_save_deposit(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value= mock_conn
        mock_conn.cursor.return_value = mock_cursor
        self.tracker.conn = mock_conn 
        self.tracker.cur = mock_cursor
        deposit = {
            'blockNumber':123,
            'blockTimestamp': 1609459200,
            'hash':'0x1234',
            'pubkey': '0x' + '12' * 48,
            'fee':0.021
        }
        self.tracker.save_deposit(deposit)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

if __name__ == '__main__':
    unittest.main()
