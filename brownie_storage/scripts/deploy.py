from brownie import accounts, config, BrownieStorage
import scripts.util_scripts as utils

def deploy_brownie_storage():
    account = utils.get_account()   
    brownie_storage = BrownieStorage.deploy({"from": account})
    stored_value = brownie_storage.retrieve()
    print(stored_value)
    transaction = brownie_storage.store(25, {"from": account})
    transaction.wait(1)
    updated_stored_value = brownie_storage.retrieve()
    print(updated_stored_value)

def main():
    deploy_brownie_storage()