// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/hevm/ERC721hevm.t.sol";

contract ERC721_OpenZeppelin_Hevm is ERC721SymbolicPropertieshevm {
    function _deployToken() internal override returns (address) { return address(new OpenZeppelinERC721()); }
}
