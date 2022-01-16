# 0.01329 ở giá $3600/eth
from brownie import Lottery, accounts, network, config, exceptions
from scripts.deployLottery import deploy_lottery
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVS, fund_with_link, get_contract
from web3 import Web3
import pytest

def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    # Act
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    # Assert
    assert lottery.getEntranceFee() == expected_entrance_fee

def test_cant_enter_unless_starter():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter()

def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account() 
    lottery.startLottery()  # according to doc https://eth-brownie.readthedocs.io/en/stable/core-contracts.html {"from":account} is optional
    lottery.enter({"value": lottery.getEntranceFee()})
    assert(lottery.players(0) == account)

def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery()
    lottery.enter({"from":account, "value": lottery.getEntranceFee()})  # can't skip the account this time, maybe because of funding
    fund_with_link(lottery)
    lottery.endLottery({"from":account})
    assert lottery.lottery_state() == 2

def test_fulfill_randomness():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    account = get_account()
    winner_account = get_account(index=1)
    lottery.startLottery()
    lottery.enter({"from":account, "value": lottery.getEntranceFee()}) 
    lottery.enter({"from":winner_account, "value": lottery.getEntranceFee()})
    lottery.enter({"from":get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    tx = lottery.endLottery({"from":account})
    request_id = tx.events["RequestedRandomness"]["requestId"]

    STATIC_RNG = 778
    get_contract("vrf_coordinator").callBackWithRandomness(request_id, STATIC_RNG, lottery.address, {"from":account})
    start_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()

    assert lottery.recentWinner() == winner_account    # because 777 % 3 == 0
    assert lottery.balance() == 0
    assert account.balance() == start_balance_of_account + balance_of_lottery

