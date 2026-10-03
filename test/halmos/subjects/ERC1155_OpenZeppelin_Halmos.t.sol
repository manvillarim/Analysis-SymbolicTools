// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/halmos/ERC1155halmos.t.sol";

contract ERC1155_OpenZeppelin_Halmos is ERC1155ymbolicPropertieshalmos {
    function _deployToken() internal override returns (address) { return address(new OpenZeppelinERC1155()); }
}
