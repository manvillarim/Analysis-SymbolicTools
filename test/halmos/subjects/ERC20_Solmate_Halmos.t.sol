// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/halmos/ERC20halmos.t.sol";

contract ERC20_Solmate_Halmos is ERC20SymbolicProperties {
    function _deployToken() internal override returns (address) { return address(new SolmateERC20Mock()); }
}
