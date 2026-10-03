// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/hevm/ERC20hevm.t.sol";

contract ERC20_Solmate_Hevm is ERC20SymbolicProperties {
    function _deployToken() internal override returns (address) { return address(new SolmateERC20Mock()); }
}
