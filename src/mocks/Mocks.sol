// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Thin wrappers that expose the internal mint/burn functions of each
// implementation under test, so that every subject has the same external API.
// The token logic itself is the unmodified upstream code.

import {ERC20Mock as OZERC20Mock} from "lib/openzeppelin-contracts/contracts/mocks/token/ERC20Mock.sol";
import {ERC4626Mock as OZERC4626Mock} from "lib/openzeppelin-contracts/contracts/mocks/token/ERC4626Mock.sol";
import {ERC721 as OZERC721} from "lib/openzeppelin-contracts/contracts/token/ERC721/ERC721.sol";
import {ERC1155 as OZERC1155} from "lib/openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol";

import {ERC20 as SolmateERC20} from "lib/solmate/src/tokens/ERC20.sol";
import {ERC721 as SolmateERC721} from "lib/solmate/src/tokens/ERC721.sol";
import {ERC1155 as SolmateERC1155} from "lib/solmate/src/tokens/ERC1155.sol";
import {ERC4626 as SolmateERC4626} from "lib/solmate/src/tokens/ERC4626.sol";

// ----------------------------------------------------------------- ERC-20

contract OpenZeppelinERC20 is OZERC20Mock {}

contract SolmateERC20Mock is SolmateERC20 {
    constructor() SolmateERC20("ERC20Mock", "E20M", 18) {}

    function mint(address account, uint256 amount) external {
        _mint(account, amount);
    }

    function burn(address account, uint256 amount) external {
        _burn(account, amount);
    }
}

// ---------------------------------------------------------------- ERC-721

contract OpenZeppelinERC721 is OZERC721 {
    constructor() OZERC721("ERC721Mock", "E721M") {}

    function mint(address to, uint256 id) public {
        _mint(to, id);
    }

    function burn(uint256 id) public {
        _burn(id);
    }
}

contract SolmateERC721Mock is SolmateERC721 {
    constructor() SolmateERC721("ERC721Mock", "E721M") {}

    function tokenURI(uint256) public pure override returns (string memory) {
        return "";
    }

    function mint(address to, uint256 id) public {
        _mint(to, id);
    }

    function burn(uint256 id) public {
        _burn(id);
    }
}

// --------------------------------------------------------------- ERC-1155

contract OpenZeppelinERC1155 is OZERC1155 {
    constructor() OZERC1155("ERC1155") {}

    function mint(address to, uint256 id, uint256 value, bytes memory data) public {
        _mint(to, id, value, data);
    }

    function burn(address from, uint256 id, uint256 value) public {
        _burn(from, id, value);
    }
}

contract SolmateERC1155Mock is SolmateERC1155 {
    function uri(uint256) public pure override returns (string memory) {
        return "ERC1155";
    }

    function mint(address to, uint256 id, uint256 value, bytes memory data) public {
        _mint(to, id, value, data);
    }

    function burn(address from, uint256 id, uint256 value) public {
        _burn(from, id, value);
    }
}

// --------------------------------------------------------------- ERC-4626

contract OpenZeppelinERC4626 is OZERC4626Mock {
    constructor(address underlying) OZERC4626Mock(underlying) {}
}

contract SolmateERC4626Mock is SolmateERC4626 {
    constructor(SolmateERC20 underlying) SolmateERC4626(underlying, "ERC4626Mock", "E4626M") {}

    function totalAssets() public view override returns (uint256) {
        return asset.balanceOf(address(this));
    }

    function mint(address account, uint256 amount) external {
        _mint(account, amount);
    }

    function burn(address account, uint256 amount) external {
        _burn(account, amount);
    }
}
