from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVS, get_account, fund_with_link
from scripts.deployLottery import deploy_lottery
from brownie import network
import pytest
import time

def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from":account})
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
