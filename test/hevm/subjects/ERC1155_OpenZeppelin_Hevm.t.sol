// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/hevm/ERC1155hevm.t.sol";

contract ERC1155_OpenZeppelin_Hevm is ERC1155ymbolicProperties {
    function _deployToken() internal override returns (address) { return address(new OpenZeppelinERC1155()); }
}
