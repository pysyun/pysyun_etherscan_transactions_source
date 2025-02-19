from eth_abi import decode
from eth_utils import remove_0x_prefix
import requests
import time


class EtherscanTransactionProcessor:
    def __init__(
            self,
            api_key,
            address: str,
            limit: int = 100,
            offset: int = 0,
            base_url: str = "https://api.etherscan.io/api"
    ):
        """
        Initializes the Etherscan transaction processor.

        Args:
            api_key: Etherscan api_key
            address: Ethereum address
            limit: Number of transactions (default 100)
            offset: Number of transactions to skip (for pagination)
            base_url: Base URL for Etherscan API
        """
        self.api_key = api_key
        self.address = address
        self.limit = limit
        self.offset = offset
        self.base_url = base_url

    def process(self, _):
        """
        Gets latest transactions for specified Ethereum address.

        Args:
            _: Dummy parameter for interface compatibility

        Returns:
            array: List of transactions
        """
        params = {
            "module": "account",
            "action": "txlist",
            "address": self.address,
            "startblock": 0,
            "endblock": 99999999,
            "page": 1,
            "offset": self.limit,
            "sort": "desc",
            "apikey": self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()

            data = response.json()

            if data["status"] == "1" and data["message"] == "OK":
                return data["result"]
            else:
                print(f"API returned error: {data['message']}")
                return []

        except requests.exceptions.RequestException as e:
            print(f"Error making API request: {e}")
            return []

        finally:
            # Add delay to avoid API rate limit
            time.sleep(0.2)


class TransferFilterProcessor:
    """
    Processor for filtering transfer and transferFrom transactions
    """

    def __init__(self):
        self.transfer_signature = "0xa9059cbb"
        self.transfer_from_signature = "0x23b872dd"

    def process(self, transactions):
        """
        Filters transactions that call transfer or transferFrom methods.

        Args:
            transactions: List of Ethereum transactions

        Returns:
            List: Filtered list containing only transfer and transferFrom transactions
        """
        return [
            tx for tx in transactions
            if tx.get('input', '').startswith(self.transfer_signature) or
               tx.get('input', '').startswith(self.transfer_from_signature)
        ]


class TransferDataProcessor:
    """
    Processor for extracting transfer data and converting it to timeline format
    """
    @staticmethod
    def decode_transfer_input(input_data):
        """
        Decodes transfer or transferFrom method input data.

        Args:
            input_data: Transaction input data

        Returns:
            dict: Decoded transfer parameters
        """
        clean_input = remove_0x_prefix(input_data)
        method_signature = clean_input[:8]
        params_data = clean_input[8:]

        try:
            if method_signature == "a9059cbb":  # transfer
                decoded = decode(['address', 'uint256'], bytes.fromhex(params_data))
                return {
                    'method': 'transfer',
                    'from': None,
                    'to': decoded[0],
                    'amount': decoded[1]
                }
            elif method_signature == "23b872dd":  # transferFrom
                decoded = decode(['address', 'address', 'uint256'], bytes.fromhex(params_data))
                return {
                    'method': 'transferFrom',
                    'from': decoded[0],
                    'to': decoded[1],
                    'amount': decoded[2]
                }
            return None
        except Exception as e:
            print(f"Error decoding input data: {e}")
            return None

    def process(self, transactions):
        """
        Processes transfer transactions and converts them to timeline format.

        Args:
            transactions: List of transfer transactions

        Returns:
            List: Timeline of transfers [{"time": timestamp, "value": transfer_data}, ...]
        """
        timeline = []

        for tx in transactions:
            decoded_data = self.decode_transfer_input(tx['input'])
            if decoded_data:
                timestamp = int(tx['timeStamp'])

                if decoded_data['method'] == 'transfer':
                    transfer_data = {
                        'from': tx['from'],
                        'to': decoded_data['to'],
                        'amount': decoded_data['amount']
                    }
                else:  # transferFrom
                    transfer_data = {
                        'from': decoded_data['from'],
                        'to': decoded_data['to'],
                        'amount': decoded_data['amount']
                    }

                timeline.append({
                    "time": timestamp,
                    "value": transfer_data
                })

        return sorted(timeline, key=lambda x: x['time'])
