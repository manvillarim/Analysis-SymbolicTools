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

    function testprove_safeTransferFromFuzz(address from, uint256 tokenId) public {
        /*from = 0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38;
        tokenId = 7237447289098456910489210153605429003754138173869686222113041559658740842496;*/
        vm.assume(from != address(0));
        try token.mint(from, tokenId) {} catch {assert(false);}
        address owner = token.ownerOf(tokenId);
        vm.assume(owner != address(0) && owner == from);
        vm.assume(msg.sender == owner || token.getApproved(tokenId) == msg.sender || token.isApprovedForAll(owner, msg.sender));
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
    
    function testproveFail_ApproveWhenIdHasNotAnOwner(address spender, uint256 id) public { // OK hevm and halmos
        spender = 0x0000000000000000000000000000000000001312;
        id = 0;
        vm.prank(msg.sender);
        vm.expectRevert();
        token.approve(spender, id);
    }
    function testproveFail_setApprovalForAllFuzz(address sender, address operator, bool approved) public {
        sender = 0x0040000080000000800000010000200000000002;
        operator = 0x1000000000000000200000000000000400000000;
        approved = false;
        vm.assume(sender != msg.sender);
        vm.prank(sender);
        vm.expectRevert();
        token.setApprovalForAll(operator, approved);
        assert(!token.isApprovedForAll(msg.sender, operator));
    }

    /*function testproveFail_MintToZeroAddressFuzz(uint256 amount) public {
        vm.assume(amount > 0);
        vm.expectRevert();
        token.mint(address(0), amount);
    }*/

    /*function testproveFail_TransferFromZeroAddressForMSGSender(address sender, address recipient, uint256 amount) public {
        sender = 0x1000000001000000000000000000000000004000;
        recipient = 0x0000000000000000000000000000000000000040;
        amount = 0;
        require(recipient != address(0) && sender != address(0));
            vm.prank(address(0));
            vm.expectRevert();
            token.transferFrom(sender, recipient, amount);
    }

    function testproveFail_ApproveZeroAddressForMSGSender(address spender, uint256 amount) public { // Only hevm
        spender = 0x8000000000000000000000000000000000000000;
        amount = 0;
        require(spender != address(0));
        vm.prank(address(0));
        vm.expectRevert();
        token.approve(spender, amount);
    }

    function testproveFail_ApproveZeroAddress(address spender, uint256 amount) public {
        spender = address(0);
        amount = 0;
        require(msg.sender != address(0) && spender == address(0));
        vm.prank(msg.sender);
        vm.expectRevert();
        token.approve(spender, amount);
    }
    
    function testproveFail_TransferToZeroAddress(address sender, uint256 amount) public {
        sender = 0x8000000000000000000000000000000000000000;
        amount = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
        require(sender != address(0) && amount > 0, "Invalid arguments");

        token.mint(sender, amount);
        
        vm.prank(sender);
        vm.expectRevert();
        token.transfer(address(0), amount);
    }

    function testproveFail_ApproveFromZeroAddress(address spender, uint256 amount) public {
        spender = 0x8000000000000000000000000000000000000000;
        amount = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
        require(spender != address(0) && amount > 0, "Invalid arguments");

        vm.prank(address(0));
        vm.expectRevert();
        token.approve(spender, amount);
    }

    function testproveFail_TransferZeroAmountToZeroAddressReverts(address sender) public {
        sender = 0x8000000000000000000000000000000000000000;
        require(sender != address(0));
        vm.expectRevert();
        token.transfer(address(0), 0);
    }

    function testproveFail_TransferFromToZeroAddress33(address owner, address spender, uint256 amount) public {
        owner = 0x000000000000000000000000000000000000ACAb;
        spender = 0x2000000000000000020002C02000000084000000;
        amount = 115792089237316195423570985008687907853269984665640564039457584007913129639935;
        require(owner != address(0) && spender != address(0) && amount > 0, "Invalid arguments");
        
        token.mint(owner, amount);
        token.approve(spender, amount);

        vm.expectRevert();        
        vm.prank(spender);
        token.transferFrom(owner, address(0), amount);
    }

    function testproveFail_TransferFromZeroAmountToZeroAddressReverts(
        address tokenSender,
        address spender
    ) public {
        tokenSender = 0x0208000080008000008000000200000000120000;
        spender = 0x0400FffF00Ff20A7200210Ff6f1B20FD11eC30C4;
        require(tokenSender != address(0) && spender != address(0));
        require(tokenSender != spender);
        token.approve(spender, 0);
        vm.prank(spender);
        vm.expectRevert();
        token.transferFrom(tokenSender, address(0), 0);
    }

    function testproveFail_ApproveToZeroAddress(address owner, uint256 amount) public {
        owner = 0x8000000000000000000000000000000000000000;
        amount = 57896044618658097711785492504343953926634992332820282019728792003956564819968;
        require(owner != address(0) && amount > 0, "Invalid arguments");

        vm.prank(owner);
        vm.expectRevert();
        token.approve(address(0), amount);
    }*/

 }