// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/halmos/ERC721halmos.t.sol";

contract ERC721_OpenZeppelin_Halmos is ERC721SymbolicPropertieshalmos {
    function _deployToken() internal override returns (address) { return address(new OpenZeppelinERC721()); }
}
