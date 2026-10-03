// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/halmos/ERC4626halmos.t.sol";

contract ERC4626_OpenZeppelin_Halmos is ERC4626SymbolicProperties {
    function _deployAsset() internal override returns (address) { return address(new OpenZeppelinERC20()); }
    function _deployVault(address underlying) internal override returns (address) { return address(new OpenZeppelinERC4626(underlying)); }
}
