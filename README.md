# PySyun Etherscan Transactions Source

## Overview
PySyun Etherscan Transactions Source is a Python module designed to interact with the Etherscan API for retrieving, filtering, and processing Ethereum transactions. This library automatically handles the installation of its required components, allowing seamless integration.

## Features
- **Retrieve Transactions**: Connect to the Etherscan API to fetch transactions for a specified Ethereum address.
- **Filter Transfers**: Isolate transactions that involve the `transfer` and `transferFrom` methods.
- **Decode Transaction Data**: Use the `eth_abi` and `eth_utils` libraries to decode transaction input data and extract meaningful transfer details.
- **Generate Timeline**: Process the decoded data into a sorted timeline for better visualization of transfer events.

## Usage
Below is an example of how to use the module:

```python
from etherscan_transaction import EtherscanTransactionProcessor, TransferFilterProcessor, TransferDataProcessor

# Initialize the Etherscan transaction processor with your API key and Ethereum address
api_key = "YOUR_ETHERSCAN_API_KEY"
address = "YOUR_ETHEREUM_ADDRESS"
transaction_processor = EtherscanTransactionProcessor(api_key, address)

# Retrieve the latest transactions
transactions = transaction_processor.process(None)

# Filter transactions to extract only transfer-related operations
filter_processor = TransferFilterProcessor()
transfer_transactions = filter_processor.process(transactions)

# Decode transfer data and generate a sorted timeline of transfers
data_processor = TransferDataProcessor()
timeline = data_processor.process(transfer_transactions)

# Output the timeline of transfers
print(timeline)
```

## Pipeline Example using PySyun Chain
You can also combine processors into a linear pipeline using PySyun Chain. This approach allows you to chain multiple processing steps into a single, seamless workflow. Below is an example that creates a pipeline to filter transfer transactions and then convert them into a timeline:

```python
from etherscan_transaction import EtherscanTransactionProcessor, TransferFilterProcessor, TransferDataProcessor
from pysyun_chain import Chainable

# Initialize the Etherscan transaction processor with your API key and Ethereum address
api_key = "YOUR_ETHERSCAN_API_KEY"
address = "YOUR_ETHEREUM_ADDRESS"
tx_processor = EtherscanTransactionProcessor(api_key, address)

# Retrieve the latest transactions
transactions = tx_processor.process(None)

# Create a pipeline that first filters transfer transactions and then processes them into a timeline
pipeline = Chainable(TransferFilterProcessor()) | Chainable(TransferDataProcessor())

# Process the transactions through the pipeline
timeline = pipeline.process(transactions)

# Output the timeline of transfers
print(timeline)
```

## Configuration
- **API Key**: Replace `"YOUR_ETHERSCAN_API_KEY"` with your actual Etherscan API key.
- **Ethereum Address**: Specify the Ethereum address from which you wish to retrieve transactions.
- **Pagination**: Use the `limit` and `offset` parameters in the `EtherscanTransactionProcessor` to control the number of transactions fetched and handle pagination.
- **Rate Limiting**: A built-in delay helps manage API rate limits when making consecutive requests.

## Code Structure
- **EtherscanTransactionProcessor**: Manages the API requests to Etherscan and retrieves transaction data.
- **TransferFilterProcessor**: Filters transactions to keep only those involving the `transfer` or `transferFrom` method signatures.
- **TransferDataProcessor**: Decodes the transaction input data and converts the transfer details into a timeline format sorted by timestamp.

## Contributing
Contributions are welcome! Feel free to fork this repository and submit pull requests for improvements, bug fixes, or new features.