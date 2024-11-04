// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import {Test, console2} from "forge-std/Test.sol";
import {ERC1155} from "lib/openzeppelin-contracts/contracts/token/ERC1155/ERC1155.sol"; // A contract to be formally verified

contract ERC1155C is ERC1155 {
    constructor(string memory uri_) ERC1155(uri_) {}

    function mint(address to, uint256 id, uint256 value, bytes memory data) public {
        _mint(to, id, value, data);
    }

    function burn(address from, uint256 id, uint256 value) public {
        _burn(from, id, value);
    }
}

contract ERC1155RecTest {
    
function onERC1155Received(
        address,
        address,
        uint256,
        uint256,
        bytes calldata
    ) external virtual returns (bytes4) {
        return ERC1155RecTest.onERC1155Received.selector;
    }

    function onERC1155BatchReceived(
        address,
        address,
        uint256[] calldata,
        uint256[] calldata,
        bytes calldata
    ) external virtual returns (bytes4) {
        return ERC1155RecTest.onERC1155BatchReceived.selector;
    }
}

contract ERC1155ymbolicProperties is Test {

    ERC1155C token;
    ERC1155RecTest from;
    ERC1155RecTest to;

    function setUp() public {
        token = new ERC1155C("ERC1155");
        from = new ERC1155RecTest();
        to = new ERC1155RecTest();
    }
    function testproveFail_safeTransferFromWhenSenderIsNotApprovedForAllFuzz(uint256 id, uint256 amount) public {
        /*vm.prank(address(from));
        token.setApprovalForAll(address(from), true);*/
        bytes memory data;
        vm.prank(address(from));
        vm.expectRevert();
        token.safeTransferFrom(address(from), address(to), id, amount, data);
    }

    /*function testproveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256 id, uint256 amount) public {
        id = 0;
        amount = 0;
        bytes memory data;
        vm.prank(msg.sender);
        vm.expectRevert();
        token.safeTransferFrom(address(from), address(to), id, amount, data);
    }
    function testprove_mintFuzz(uint256 id, uint256 amount, bytes memory data) public {
        require(address(from) != address(0));
        uint256 _balanceAcc = token.balanceOf(address(from), id);
        token.mint(address(from), id, amount, data);
        assert(token.balanceOf(address(from), id) == _balanceAcc + amount);
    }

    function testprove_safeBatchTransferFromFuzz(uint256 initAmount, uint256[] memory ids, uint256[] memory values) public { // Require additional timeout
        require(ids.length == values.length && ids.length == 2 && ids[0]!=ids[1]);
        bytes memory data = new bytes(3);
        uint256[] memory _balanceIdFrom = new uint256[](ids.length);
        uint256[] memory _balanceIdTo = new uint256[](ids.length);
        for(uint8 i=0; i<ids.length; i++) {
            try token.mint(address(from), ids[i], initAmount, data) {} catch {assert(false);}
            _balanceIdFrom[i] = token.balanceOf(address(from), ids[i]);
            _balanceIdTo[i] = token.balanceOf(address(to), ids[i]);
            require(_balanceIdFrom[i] >= values[i]);
        }
        vm.prank(address(from));
        token.safeBatchTransferFrom(address(from), address(to), ids, values, data);
        for(uint8 i=0; i<ids.length; i++) {
            assert(token.balanceOf(address(from), ids[i]) == _balanceIdFrom[i] - values[i]);
            assert(token.balanceOf(address(to), ids[i]) == _balanceIdTo[i] + values[i]);
        }
    }

    function testproveFail_burnBalanceLessThanAmount(uint256 id, uint256 initAmount, uint256 amount) public {
        id = 0x0000000000000000000000000000000000000000000000000000000000000000;
        initAmount = 0x0000000000000000000000000000000000000000000000000000000000000000;
        bytes memory data;
        try token.mint(address(from), id, initAmount, data) {} catch{assert(false);}
        uint256 balanceAcc = token.balanceOf(address(from), id);
        require(balanceAcc < amount);
        try token.burn(address(from), id, amount) {assert(false);} catch {assert(true);}
    }

    /*function testprove_safeTransferFromFuzz(address from, uint256 tokenId) public {
        /*from = 0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38;
        tokenId = 7237447289098456910489210153605429003754138173869686222113041559658740842496;*/
        /*vm.assume(from != address(0));
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