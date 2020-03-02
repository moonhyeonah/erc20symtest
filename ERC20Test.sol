pragma solidity ^0.4.24;

contract StandardToken {
    mapping (address => uint256) balances;
    mapping (address => mapping (address => uint256)) allowed;
    uint256 public totalSupply;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    
    constructor (uint _totalSupply) public {
        totalSupply = _totalSupply;
        balances[msg.sender] = _totalSupply;
        emit Transfer(0x0, msg.sender, _totalSupply);
    }

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

    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success) {
        if (balances[_from] >= _value && allowed[_from][msg.sender] >= _value && _value > 0) {
            balances[_to] += _value;
            balances[_from] -= _value;
            allowed[_from][msg.sender] -= _value;
            emit Transfer(_from, _to, _value);
            return true;
        }
        else {
            return false;
        }
    }

    function balanceOf(address _owner) public constant returns (uint256 balance) {
        return balances[_owner];
    }

    function approve(address _spender, uint256 _value) public returns (bool success) {
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function allowance(address _owner, address _spender) public constant returns (uint256 remaining) {
      return allowed[_owner][_spender];
    }
}

contract ERC20Token {
    function totalSupply() public pure returns (uint256) {}
    function balanceOf(address _owner) public view returns (uint256 balance);
    function transfer(address _to, uint256 _value) public returns (bool success);
    function transferFrom(address _from, address _to, uint256 _value) public returns (bool success);
    function approve(address _spender, uint256 _value) public returns (bool success);
    function allowance(address _owner, address _spender) public view returns (uint256 remaining);

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract ERC20Test {
    
    ERC20Token targetToken;
    uint256 constant MAX = 2 ** 256 - 1;
    
    constructor (address _targetToken) public {
        targetToken = ERC20Token(_targetToken);
    }
    
    function testBA1(address _owner, uint256 _balance) public view returns (bool success) {
        if (targetToken.balanceOf(_owner) == _balance) {
            return true;
        }
        return false;
    }
    
/*    function testBA2(address _owner, uint256 _balance) public view returns (bool success) {
        return false;
    }
*/    
    function testTS1(uint256 _totalSupply) public view returns (bool success) {
        if (targetToken.totalSupply() == _totalSupply) {
            return true;
        }
        return false;
    }

    function testAL1(address _owner, address _spender, uint256 _remaining) public view returns (bool success) {
        if (targetToken.allowance(_owner, _spender) == _remaining) {
            return true;
        }
        return false;
    }
    
    function testAP(address _spender, uint256 _value) public returns (bool success) {
        address msgSender = address(this);
        uint256 fromBal = targetToken.balanceOf(msgSender);
        if (fromBal >= _value) {
            if (targetToken.approve(_spender, _value) == true) {
                if (targetToken.allowance(msgSender, _spender) == _value) {
                    return true;
                }
            }
        }
        else {
            uint256 remaining = targetToken.allowance(msgSender, _spender);
            if (targetToken.approve(_spender, _value) == false) {
                if (targetToken.allowance(msgSender, _spender) == remaining) {
                    return true;
                }
            }
        }
        return false;
    }    
    
    function testTF(address _from, address _to, uint256 _value) public returns (bool success) {
        address msgSender = address(this);
        uint256 fromBal = targetToken.balanceOf(_from);
        uint256 toBal = targetToken.balanceOf(_to);
        uint256 remaining = targetToken.allowance(_from, msgSender);
        
        if (fromBal >= _value) {
            if ((toBal + _value) <= MAX) {
                if (remaining >= _value) {
                    if (targetToken.transferFrom(_from, _to, _value) == true) {
                        if ( (targetToken.balanceOf(_from) == (fromBal - _value)) &&
                             (targetToken.balanceOf(_to) == (toBal + _value)) &&
                             (targetToken.allowance(_from, msgSender) == (remaining - _value)) ) {
                             return true;
                         }
                    }
                }
                else {
                    targetToken.transferFrom(_from, _to, _value);
                    // throw check
                }
            }
            else {
                if (targetToken.transferFrom(_from, _to, _value) == false) {
                    if ( (targetToken.balanceOf(_from) == fromBal) &&
                         (targetToken.balanceOf(_to) == toBal) &&
                         (targetToken.allowance(_from, msgSender) == remaining) )
                         return true;
                }
            }    
        }
        else {
            if (targetToken.transferFrom(_from, _to, _value) == false) {
                    if ( (targetToken.balanceOf(_from) == fromBal) &&
                         (targetToken.balanceOf(_to) == toBal) &&
                         (targetToken.allowance(_from, msgSender) == remaining) )
                         return true;
            }
        }
        
        return false;
    }

    function testTR(address _to, uint256 _value) public returns (bool success) {
        address msgSender = address(this);
        uint256 fromBal = targetToken.balanceOf(msgSender);
        uint256 toBal = targetToken.balanceOf(_to);
        if (fromBal >= _value) {
            if ((toBal + _value) <= MAX) {
                if (targetToken.transfer(_to, _value) == true) {
                    if ( (targetToken.balanceOf(msgSender) == (fromBal - _value)) &&
                         (targetToken.balanceOf(_to) == (toBal + _value)) )
                         return true;
                }
            }
            else {
                if (targetToken.transfer(_to, _value) == false) {
                    if ( (targetToken.balanceOf(msgSender) == fromBal) &&
                         (targetToken.balanceOf(_to) == toBal) )
                         return true;
                }
            }    
        }
        else {
            targetToken.transfer(_to, _value);
            // throw 확인
        }
        
        return false;
    }

}