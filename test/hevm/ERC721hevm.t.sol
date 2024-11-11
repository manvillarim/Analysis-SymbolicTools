// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import {Test, console2} from "forge-std/Test.sol";
import {MockERC721} from "forge-std/mocks/MockERC721.sol";

 contract ERC721 is MockERC721 {
    function mint(address to, uint256 id) public {
         _mint(to, id);
    }

    function burn(uint256 id) public {
        _burn(id);
    }

}

contract ERC721ReveiverTest {
    function onERC721Received() external pure returns(bytes4) {
        // Just to enable safeTransferFrom conditions
        return bytes4(keccak256("onERC721Received(address,address,uint256,bytes)"));
    }
}

contract ERC721SymbolicProperties is Test {

    ERC721 token;
    ERC721ReveiverTest rec;

    function setUp() public {
        token = new ERC721();
        token.initialize("ERC721Token", "ERC721Token");
        rec = new ERC721ReveiverTest();
    }

    // This function verifies the `setApprovalForAll` function of the ERC721 contract. It sets the approval for an operator and checks if the `isApprovedForAll` function returns the correct value.
    function prove_setApprovalForAll(address operator, bool approved) public {
        vm.prank(msg.sender);
        token.setApprovalForAll(operator, approved);
        assert(token.isApprovedForAll(msg.sender, operator) == approved);
    }

    // This function verifies the `approve` function when the owner of the token is the same as the message sender. It mints a token for the message sender, approves a spender, and checks if the `getApproved` function returns the correct spender address.
    function prove_ApproveWhenOwnerEqualsMSGSender(address spender, uint256 id) public { // OK hevm and halmos
        require(msg.sender != address(0));
        try token.mint(msg.sender, id) {} catch {assert(false);}
        address owner = token.ownerOf(id);
        require(msg.sender == owner);
        vm.prank(msg.sender);
        try token.approve(spender, id) {} catch { assert(false); }
        assert(token.getApproved(id) ==  spender);
    }

    // This function verifies the `approve` function when the owner of the token is different from the message sender, but the message sender is approved for all tokens of the owner.
    function prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address spender, uint256 id) public { // OK halmos (hevm killed)
        require(spender != address(0) && spender != msg.sender);
        try token.mint(spender, id) {} catch {assert(false);}
        vm.prank(spender);
        try token.setApprovalForAll(msg.sender, true) {} catch {assert(false);}
        address owner = token.ownerOf(id);
        require(msg.sender != owner && token.isApprovedForAll(owner, msg.sender));
        vm.prank(msg.sender);
        try token.approve(spender, id) {} catch { assert(false); }
        assert(token.getApproved(id) ==  spender);
    }

    // This function verifies the `transferFrom` function of the ERC721 contract. It mints a token for the `from` address, checks if the caller is the owner or an approved operator, transfers the token to the `to` address, and verifies the balances and ownership.
    function prove_transferFrom(address from, address to, uint256 tokenId) public {
        require(from != address(0) && to != address(0) && from != to);
        try token.mint(from, tokenId) {} catch {assert(false);}
        address owner = token.ownerOf(tokenId);
        require(owner != address(0) && owner == from);
        require(msg.sender == owner || token.getApproved(tokenId) == msg.sender || token.isApprovedForAll(owner, msg.sender));
        uint256 _balancesFrom = token.balanceOf(from);
        uint256 _balancesTo = token.balanceOf(to);

        vm.prank(msg.sender);
        try token.transferFrom(from, to, tokenId) {} catch {assert(false);}

        assert(token.balanceOf(from) == _balancesFrom - 1);
        assert(token.balanceOf(to) == _balancesTo + 1);
        assert(token.ownerOf(tokenId) == to);
        assert(token.getApproved(tokenId) ==  address(0));
    }

    // This function verifies the `safeTransferFrom` function of the ERC721 contract, similar to `prove_transferFrom`.
    function prove_safeTransferFrom(address from, uint256 tokenId) public {
        require(from != address(0));
        try token.mint(from, tokenId) {} catch {assert(false);}
        address owner = token.ownerOf(tokenId);
        require(owner != address(0) && owner == from);
        require(msg.sender == owner || token.getApproved(tokenId) == msg.sender || token.isApprovedForAll(owner, msg.sender));
        uint256 _balancesFrom = token.balanceOf(from);
        uint256 _balancesTo = token.balanceOf(address(rec));

        vm.prank(msg.sender);
        try token.safeTransferFrom(from, address(rec), tokenId) {
            assert(token.balanceOf(from) == _balancesFrom - 1);
            assert(token.balanceOf(address(rec)) == _balancesTo + 1);
            assert(token.ownerOf(tokenId) == address(rec));
            assert(token.getApproved(tokenId) ==  address(0));
        } catch {assert(false);}

    }

    // This function mints a new ERC721 token with the given `id` and transfers ownership to the `to` address.
    function prove_Mint(address to, uint256 tokenId) public { // OK
        require(to != address(0));
        uint256 _balanceTo = token.balanceOf(to);

        try token.mint(to, tokenId) {} catch {assert(false);}

        assert(token.balanceOf(to) == _balanceTo + 1);
        assert(token.ownerOf(tokenId) == to);
    }

    // This function burns (destroys) the ERC721 token with the given `id`.
    function prove_Burn(uint256 tokenId) public {
        require(msg.sender != address(0));
        try token.mint(msg.sender, tokenId) {} catch {assert(false);}

        address owner = token.ownerOf(tokenId);
        require(owner != address(0));
        uint256 _balanceOwner = token.balanceOf(owner);

        vm.prank(msg.sender);
        try token.burn(tokenId) {} catch {assert(false);}

        assert(token.balanceOf(owner) == _balanceOwner - 1);
        assert(token.getApproved(tokenId) ==  address(0));
        //assert(token.ownerOf(tokenId) == address(0)); // This cannot be verified. Why?
    }

// ********************************** Revertable properties ***********************************************

    // This function verifies that the `approve` function reverts when the given token ID does not have an owner.
    function proveFail_ApproveWhenIdHasNotAnOwner(address spender, uint256 id) public { // OK hevm and halmos
        vm.prank(msg.sender);
        token.approve(spender, id);
    }

    // This function verifies that the `approve` function reverts when the caller is not the owner of the token and is not approved for all tokens of the owner.
    function proveFail_ApproveWhenIsNotApprovedForAll(address spender, address other, uint256 id) public { // OK halmos (hevm killed)
        require(spender != address(0) && spender != msg.sender);
        token.mint(spender, id);
        require(other != spender);
        vm.prank(other);
        token.setApprovalForAll(msg.sender, true);
        address owner = token.ownerOf(id);
        require(msg.sender != owner && !token.isApprovedForAll(owner, msg.sender));
        vm.prank(msg.sender);
        token.approve(spender, id);
    }

    // This function verifies that the `transferFrom` function reverts when the `from` address is not the owner of the token.
    function proveFail_transferFromWhenFromIsNotTheOwner(address from, address to, uint256 tokenId) public {
        // Simply not minting previously (setup)
        vm.prank(msg.sender);
        token.transferFrom(from, to, tokenId);
    }

    // This function verifies that the `transferFrom` function reverts when the `to` address is the zero address.
    function proveFail_transferFromWhenToIsAddressZero(address from, address to, uint256 tokenId) public {
        require(from != address(0) && to == address(0) && from != to);
        token.mint(from, tokenId);
        address owner = token.ownerOf(tokenId);
        require(owner != address(0) && owner == from);
        require(msg.sender == owner || token.getApproved(tokenId) == msg.sender || token.isApprovedForAll(owner, msg.sender));

        vm.prank(msg.sender);
        token.transferFrom(from, to, tokenId);
    }

    // This function verifies that the `mint` function reverts when the `to` address is the zero address.
    function proveFail_MintWhenToIsAddressZero(address to, uint256 tokenId) public { // OK
        require(to == address(0));
        token.mint(to, tokenId);
    }

    // This function verifies that the `burn` function reverts when the given token ID does not have an owner.
    function proveFail_Burn(uint256 tokenId) public {
        // Simply not having an owner for tokenId
        vm.prank(msg.sender);
        token.burn(tokenId);
    }

    // This function verifies that the `setApprovalForAll` function reverts when the caller is not the owner of the tokens.
    function proveFail_setApprovalForAll(address sender, address operator, bool approved) public {
        require(sender != msg.sender);
        vm.prank(sender);
        token.setApprovalForAll(operator, approved);
        assert(!token.isApprovedForAll(msg.sender, operator));
    }

}