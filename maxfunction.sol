pragma solidity ^0.4.24;

contract MaxFunction {
    
    uint max;
    mapping (uint256 => uint256) list;

    constructor () public {
        list[1] = 10;
        list[2] = 20;
        list[3] = 30;
    }

    function maxOfList(uint x, uint y, uint z) public returns (uint256 result, uint, uint, uint) {
        if ( list[x] >= list[y] ) {
            if ( list[x] >= list[z] ) {
                max = list[x];
            }
            else {
                max = list[z];
            }
        }
        else {
            if ( list[y] >= list[z] ) {
                max = list[y];
            }
            else {
                max = list[z];
            }
        }
        return (max, list[x], list[y], list[z]);
    }
    
    function maxOf(uint x, uint y, uint z) public returns (uint256 result) {
        if ( x >= y ) {
            if ( x >= z ) {
                max = x;
            }
            else {
                max = z;
            }
        }
        else {
            if ( y >= z ) {
                max = y;
            }
            else {
                max = z;
            }
        }
        return max;
    }
}
