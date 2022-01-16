from brownie import BrownieStorage, accounts

def test_deploy():
    # Arrange
    account = accounts[0]
    # Act
    brownie_storage = BrownieStorage.deploy({"from": account})
    starting_value = brownie_storage.retrieve()
    expected = 0
    # Assert
    assert starting_value == expected

def test_update_val():
    # Arrange
    account = accounts[0]
    brownie_storage = BrownieStorage.deploy({"from": account})
    # Act
    expected = 15
    brownie_storage.store(expected, {"from": account})
    # Assert
    assert brownie_storage.retrieve() == expected
