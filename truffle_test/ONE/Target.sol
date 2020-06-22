pragma solidity ^0.5.0;

import "./ONE.sol";

contract Target is HarmonyOne{

    constructor() public HarmonyOne() {
        
    }
    
    function setBalance(address _owner, uint256 _value) public returns (bool success) {
        balances[_owner] = _value;
        return true;
    }

    function setBalanceMax(address _owner) public returns (bool success) {
        balances[_owner] = 115792089237316195423570985008687907853269984665640564039457584007913129639935;
        return true;
    }

    function setAllowed(address _owner, address _spender, uint256 _value) public returns (bool success) {
        allowed[_owner][_spender] = _value;
        return true;
    }
}