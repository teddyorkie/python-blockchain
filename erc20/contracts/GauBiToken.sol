// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./IERC20.sol";
import "@chainlink/contracts/src/v0.8/vendor/SafeMathChainlink.sol";

contract GauBiToken is IERC20 {
    address payable[] public holders;
    mapping(address => uint256) private addrToBalance;
    mapping (address => mapping (address => uint256)) public allowed;
    string _name;
    string _symbol;
    uint8 _decimals;
    uint256 _totalSupply;
    event Transfer(address indexed _from, address indexed _to, uint256 _value);
    event Approval(address indexed _owner, address indexed _spender, uint256 _value);

    constructor() {
        _name = "GauBiToken";
        _symbol = "GBT";
        _decimals = 8;
        _totalSupply = 1_000_000_000;
    }

    function name() public view returns (string memory) {
        return _name;
    }

    function symbol() public view returns (string memory) {
        return _symbol;
    }

    function decimals() public view returns (uint8) {
        return _decimals;
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    /**
    * @dev Gets the balance of the specified address.
    * @param owner The address to query the balance of.
    * @return An uint256 representing the amount owned by the passed address.
    */
    function balanceOf(address _owner) public view returns (uint256) {
        return addrToBalance[_owner];
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(addrToBalance[msg.sender] >= value);
        addrToBalance[msg.sender] -= value;
        addrToBalance[_to] += value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        require(addrToBalance[_from] >= value);
        addrToBalance[_from] -= value;
        addrToBalance[_to] += value;
        emit Transfer(_from, _to, _value);
        return true;
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        require(_spender != address(0));
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public view returns (uint256 remaining) {
        return allowed[_owner][_spender];
    }

}
