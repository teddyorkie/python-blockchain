from brownie import network, accounts, config
from brownie import FundMe, MockV3Aggregator
import scripts.util_scripts as utils

def deploy_fund_me():
    account = utils.get_account()

    # pass the price feed address to our fundme contract

    if network.show_active() not in utils.LOCAL_BLOCKCHAIN_ENVS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        utils.deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    fund_me = FundMe.deploy(
        price_feed_address, 
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"Contract deployed to {fund_me.address}")
    return fund_me

def main():
    deploy_fund_me()