pragma solidity ^0.4.18;

import "./POLY.sol";

contract Target is PolyToken{

    function Target() public PolyToken(address(1)) {
        
    }
    
    function setBalance(address _owner, uint256 _value) public returns (bool success) {
        balances[_owner] = _value;
        return true;
    }
    
    function unsetBalance(address _owner) public returns (bool success) {
        delete balances[_owner];
        return true;
    }

    function setAllowed(address _owner, address _spender, uint256 _value) public returns (bool success) {
        allowed[_owner][_spender] = _value;
        return true;
    }

    function unsetAllowed(address _owner, address _spender) public returns (bool success) {
        delete allowed[_owner][_spender];
        return true;
    }
}