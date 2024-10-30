//SPDX-License-Identifier:MIT
pragma solidity >= 0.8.0;

import {Test, console2} from "forge-std/Test.sol";
import {ERC20Mock} from "../lib/openzeppelin-contracts/contracts/mocks/token/ERC20Mock.sol";
import {SafeERC20} from "../lib/openzeppelin-contracts/contracts/token/ERC20/utils/SafeERC20.sol";
import "../src/ERC20SOLMock.sol";
import "../src/erc20ruim.sol";
contract ERC20SymbolicProperties is Test {
    using SafeERC20 for ERC20r;

    ERC20r token;

    function setUp() public {
        token = new ERC20r(0);
    }

    function testprove_MsgSenderCanRetrieveOtherBalance() public{
        address otherAddress = 0x0400000000000000000000000000000000000000;
        uint256 amount = 0x00000000000000100400c210a64e82028500b3d13c84c2008b00000000000000;
        require(otherAddress != address(0) && amount > 0, "Invalid arguments");
        require(msg.sender != otherAddress, "msg.sender and otherAddress cannot be the same");
        token.mint(otherAddress, amount);
        assert(token.balanceOf(otherAddress) == amount);
    }

    function testproveFail_TransferFromUnderBalance(address owner, address spender, uint256 amount) public {
        owner = 0x00000000000000000000000000000000aAAa0001;
        spender = 0x0000000000000000000000000200000000000000;
        amount = 0x0000000000000000001fffffff10200000000000000000000000000000000000;
        require(owner != address(0) && spender != address(0) && amount > 0, "Invalid arguments");

        token.mint(owner, amount - 1);
        
        token.approve(spender, amount);
        
        vm.prank(spender);
        vm.expectRevert();
        token.transferFrom(owner, address(0xdead), amount);
    }

    function testprove_BalanceUpdatedAfterBurn(
        address tokenApprover,
        address tokenApprovee,
        uint256 amount
    ) public {
        amount = 0x0000000000000000000000000e40200cd8137a83800022078e98441f00461fc2;
        tokenApprovee = 0x0000000040000000000000000000000000000000;
        tokenApprover = 0x0000010100000000000000000000000000800000;
        require(tokenApprover != address(0) && tokenApprovee != address(0));
        require(tokenApprover != tokenApprovee);
        require(amount > 0);
        token.mint(tokenApprover, amount);
        token.approve(tokenApprovee, amount);
        uint256 initialApproverBalance = token.balanceOf(tokenApprover);
        uint256 initialApproveeBalance = token.balanceOf(tokenApprovee);
        vm.prank(tokenApprovee);
        token.burn(tokenApprover, amount);
        assert(token.balanceOf(tokenApprover) == initialApproverBalance - amount);
        assert(token.balanceOf(tokenApprovee) == initialApproveeBalance);
    }

    function testprove_BurnDifferentAccountFuzz(address account1, uint256 amount1, address account2, uint256 amount2) public { 
        vm.assume(account1 != address(0) && account2 != address(0) && account1 != account2);
        vm.assume(amount1 + amount2 >= amount1 || amount1 + amount2 >= amount2);
        try token.mint(account1, amount1) {} catch { assert(false); } 
        try token.mint(account2, amount2) {} catch { assert(false); } 
        uint256 _balanceRecipient1 = token.balanceOf(account1);
        uint256 _balanceRecipient2 = token.balanceOf(account2);
        uint256 _totalSupply = token.totalSupply();
        vm.assume(_balanceRecipient1 >= amount1);
        try token.burn(account1, amount1) {} catch { assert(false); } 
        assert(token.totalSupply() == _totalSupply - amount1);
        assert(token.balanceOf(account1) == _balanceRecipient1 - amount1);
        assert(token.balanceOf(account2) == _balanceRecipient2); // This must not change
    }

    function testprove_MsgSenderCanRetrieveOwnBalanceFuzz(uint256 amount) public {
        token.mint(msg.sender, amount);
        assert(token.balanceOf(msg.sender) == amount);
    }
}
