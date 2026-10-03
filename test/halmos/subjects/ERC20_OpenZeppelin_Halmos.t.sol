// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/halmos/ERC20halmos.t.sol";

contract ERC20_OpenZeppelin_Halmos is ERC20SymbolicProperties {
    function _deployToken() internal override returns (address) { return address(new OpenZeppelinERC20()); }
}
