pragma solidity ^0.4.24;


/// @title Standard token contract
/// @author Stefan George - <stefan.george@consensys.net>
contract StandardToken {
    /*
     *  Data structures
     */
    mapping (address => uint256) balances;
    uint256 public totalSupply;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor (uint _totalSupply) public {
        /// uint _totalSupply = 200;
        totalSupply = _totalSupply;
        balances[msg.sender] = _totalSupply;
        emit Transfer(0x0, msg.sender, _totalSupply);
    }

    /*
     *  Read and write storage functions
     */
    /// @dev Transfers sender's tokens to a given address. Returns success.
    /// @param _to Address of token receiver.
    /// @param _value Number of tokens to transfer.
    function transfer(address _to, uint256 _value) public returns (bool success) {
        if (balances[msg.sender] >= _value && _value > 0) {
            balances[msg.sender] -= _value;
            balances[_to] += _value;
            emit Transfer(msg.sender, _to, _value);
            return true;
        }
        else {
            return false;
        }
    }


    /// @dev Returns number of tokens owned by given address.
    /// @param _owner Address of token owner.
    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balances[_owner];
    }

}
