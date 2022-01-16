from brownie import FundMe
import scripts.util_scripts as utils

def fund():
    fund_me = FundMe[-1]
    account = utils.get_account()
    entrance_fee = fund_me.getEntranceFee()
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    fund_me.fund({"from": account, "value":entrance_fee})

def withdraw():
    fund_me = FundMe[-1]
    account = utils.get_account()
    fund_me.withdraw({"from": account})

def main():
    fund()
    withdraw()