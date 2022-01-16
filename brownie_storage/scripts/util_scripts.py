from brownie import network, config, accounts, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 200_000_000_000

FORKED_LOCAL_ENV = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVS = ['development', 'ganache-local']

def get_account():
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVS 
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]  # auto assign to accounts generated by ganache-cli
        # rinkeby_account = accounts.load('rinkeby-account')  # securely store the private key
    else:
        return accounts.add(config["wallets"]["from-key"])

def deploy_mocks():
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")

    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print("Mocks Deployed!")
