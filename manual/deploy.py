from eth_keys.datatypes import PrivateKey
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

# install_solc("0.8.0")

with open("SimpleStorage.sol") as f:
    simple_storage_file = f.read()

# compile our solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_sol.json", "w") as f:
    json.dump(compiled_sol, f)

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# for connecting to rinkeby testnet
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/f8d9627d2bb84569927e4af4d910c3e1"))
chain_id = 4
address = "0xe09e32aAC6fdE08740231a1eB0364E69D0241393" # rinkeby testnet address
private_key = os.getenv("PRIVATE_KEY")

# 1. Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get the latest transaction = nonce
nonce = w3.eth.getTransactionCount(address)
print(f"nonce={nonce}")

# 2. Build a transaction
tx = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": address, "nonce": nonce}
)

# 3. Sign the transaction
signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)

# 4. Send the transaction
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

# Working with Contract, we need ABI & Address
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

print(simple_storage.functions.retrieve().call())
print(simple_storage.functions.store(14).call())    # just simulate the call to chain
print(simple_storage.functions.retrieve().call())

# Transaction start here
store_transaction = simple_storage.functions.store(21).buildTransaction(
    {"chainId": chain_id, "from": address, "nonce": nonce + 1}
)

signed_store_txn = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)