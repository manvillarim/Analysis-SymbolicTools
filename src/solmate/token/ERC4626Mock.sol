// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import {ERC20} from "./ERC20.sol";
import {ERC4626} from "./ERC4626.sol";

contract ERC4626SMock is ERC4626 {
    constructor(ERC20 asset) ERC4626(asset, "ERC4626Mock", "E4626M") {}

    function mint(address account, uint256 amount) external {
        _mint(account, amount);
    }

    function burn(address account, uint256 amount) external {
        _burn(account, amount);
    }

}
