// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/hevm/ERC20hevm.t.sol";

contract ERC20_OpenZeppelin_Hevm is ERC20SymbolicProperties {
    function _deployToken() internal override returns (address) { return address(new OpenZeppelinERC20()); }
}
