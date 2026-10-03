// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/halmos/ERC1155halmos.t.sol";

contract ERC1155_Solmate_Halmos is ERC1155ymbolicPropertieshalmos {
    function _deployToken() internal override returns (address) { return address(new SolmateERC1155Mock()); }
}
