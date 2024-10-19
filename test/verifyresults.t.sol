//SPDX-License-Identifier:MIT
pragma solidity >= 0.8.0;

import {Test, console2} from "forge-std/Test.sol";
import {ERC20Mock} from "../lib/openzeppelin-contracts/contracts/mocks/token/ERC20Mock.sol";
import {SafeERC20} from "../lib/openzeppelin-contracts/contracts/token/ERC20/utils/SafeERC20.sol";
import "../src/ERC20SOLMock.sol";
 contract ERC20SymbolicProperties is Test {
    using SafeERC20 for ERC20Mock;

    ERC20SolMock token;

    function setUp() public {
        token = new ERC20SolMock();
    }
    
    function testproveFail_MintToZeroAddress(uint256 amount) public {
        amount = 112777989180875142641012667662881322846184324395630932477102348584379903997143;
        require(amount > 0, "Invalid arguments");
        vm.expectRevert();
        token.mint(address(0), amount);
    }

    function testproveFail_TransferFromZeroAddressForMSGSender(address sender, address recipient, uint256 amount) public {
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
    }
 }