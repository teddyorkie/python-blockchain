from brownie import BrownieStorage, accounts, config

def read_contract():
    value_stored = BrownieStorage[-1]       # <-- this is the most recent deployment
    print(value_stored.retrieve())

def main():
    read_contract()