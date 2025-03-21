

//SPDX-License-Identifier:MIT
pragma solidity >= 0.8.0;

import {Test, console2} from "forge-std/Test.sol";
import {ERC20Mock} from "../lib/openzeppelin-contracts/contracts/mocks/token/ERC20Mock.sol";
import {SafeERC20} from "../lib/openzeppelin-contracts/contracts/token/ERC20/utils/SafeERC20.sol";
 contract ERC20SymbolicProperties is Test {
    using SafeERC20 for ERC20Mock;

    ERC20Mock token;

    function setUp() public {
        token = new ERC20Mock();
    }
    function testFailproveFail_MintToZeroAddress(uint256 amount) public {
        vm.assume(amount > 0);
        vm.prank(address(0));
        token.mint(address(0), 112777989180875142641012667662881322846184324395630932477102348584379903997143);
    }

    // Proves approving a spender to transfer tokens. Checks allowance is set correctly.
    /*function testprove_ApproveFuzz(address spender, uint256 amount) public { 
        vm.assume(msg.sender != address(0) && spender != address(0));
        vm.prank(msg.sender);
        try token.approve(spender, amount) returns (bool success) { assert(success); } catch { assert(false); } 
        assert(token.allowance(msg.sender, spender) ==  amount);
    }

    // Proves minting new tokens. Checks total supply and recipient balance increase.
    function testprove_MintFuzz(address account, uint256 amount) public { 
        uint256 _balanceRecipient;
        uint256 _totalSupply;
        _totalSupply = token.totalSupply();
        vm.assume(account != address(0));
        _balanceRecipient = token.balanceOf(account);
        try token.mint(account, amount) {} catch { assert(false); } 
        assert(token.totalSupply() == _totalSupply + amount);
        assert(token.balanceOf(account) == _balanceRecipient + amount);
    }

    // Proves minting zero tokens. Checks balance is not changed.
    function testprove_MintZeroTokensFuzz(address account) public {
        vm.assume(account != address(0));
        uint256 initialBalance = token.balanceOf(account);
        token.mint(account, 0);
        assert(token.balanceOf(account) == initialBalance);
    }

    // Proves burning tokens, when using the same account. Checks total supply and recipient balance decrease.
    function testprove_BurnSameAccountFuzz(address account, uint256 amount) public { 
        vm.assume(account != address(0));
        try token.mint(account, amount) {} catch { assert(false); } 
        uint256 _balanceRecipient = token.balanceOf(account);
        uint256 _totalSupply = token.totalSupply();
        vm.assume(_balanceRecipient >= amount);
        try token.burn(account, amount) {} catch { assert(false); } 
        assert(token.totalSupply() == _totalSupply - amount);
        assert(token.balanceOf(account) == _balanceRecipient - amount);
    }

    // Proves burning tokens, when using different accounts. Checks total supply and recipient balance decrease.
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

    // Proves transferring tokens. Checks sender and recipient balances update.
    function testprove_TransferFuzz(address recipient, uint256 preAmount, uint256 amount) public { 
        vm.assume(msg.sender != address(0));
        token.mint(msg.sender, preAmount);
        uint256 _balanceSender = token.balanceOf(msg.sender);
        uint256 _totalSupply = token.totalSupply();
        vm.assume(msg.sender != recipient && recipient != address(0) && _balanceSender >= amount);
        uint256 _balanceRecipient = token.balanceOf(recipient);
        vm.prank(msg.sender);
        try token.transfer(recipient, amount) returns (bool success) { assert(success); } catch { assert(false); } 
        assert(token.balanceOf(msg.sender) <=  _balanceSender - amount);
        assert(token.balanceOf(recipient) ==  _balanceRecipient + amount);
        assert(token.totalSupply() == _totalSupply);
    }

    // Proves transferring tokens via an approved allowance. Checks balances and allowance update.
    function testprove_TransferFromFuzz(address sender, address recipient, uint256 preAmount, uint256 amount) public { 
        vm.assume(msg.sender != address(0) && sender != address(0));
        token.mint(msg.sender, preAmount);
        uint256 _balanceSender = token.balanceOf(sender);
        uint256 _allowanceFromTo = token.allowance(sender, msg.sender);
        vm.assume(_balanceSender >= amount && _allowanceFromTo >= amount && recipient != address(0));
        uint256 _balanceRecipient = token.balanceOf(recipient);
        uint256 _totalSupply = token.totalSupply();
        vm.prank(msg.sender);
        try token.transferFrom(sender, recipient, amount) returns (bool success) { assert(success); } catch { assert(false); } 
        assert(token.balanceOf(sender) ==  _balanceSender - amount);
        assert(token.balanceOf(recipient) ==  _balanceRecipient + amount);
        assert(token.allowance(sender, msg.sender) ==  _allowanceFromTo - amount);
        assert(token.totalSupply() == _totalSupply);
    }

    // Proves increasing allowance. Checks allowance is increased.
    function testprove_IncreaseAllowanceFuzz(address spender, uint256 addedValue) public { 
        vm.assume(msg.sender != address(0) && spender != address(0));
        uint256 _allowanceFromTo = token.allowance(msg.sender, spender);
        uint256 _balanceSpender = token.balanceOf(spender);
        uint256 _totalSupply = token.totalSupply();
        vm.assume(_allowanceFromTo + addedValue >= _allowanceFromTo && _allowanceFromTo + addedValue >= addedValue);
        vm.prank(msg.sender);
        try token.approve(spender, _allowanceFromTo + addedValue) { } catch { assert(false); } 
        assert(token.allowance(msg.sender, spender) ==  _allowanceFromTo + addedValue);
        assert(token.balanceOf(spender) ==  _balanceSpender);
        assert(token.totalSupply() == _totalSupply);
    }

    // Proves decreasing allowance. Checks allowance is decreased.
    function testprove_DecreaseAllowanceFuzz(address spender, uint256 subtractedValue) public { 
        vm.assume(msg.sender != address(0) && spender != address(0));
        vm.prank(msg.sender);
        uint256 _allowanceFromTo = token.allowance(msg.sender, spender);
        uint256 _balanceSpender = token.balanceOf(spender);
        uint256 _totalSupply = token.totalSupply();
        vm.assume(_allowanceFromTo >= subtractedValue);
        try token.approve(spender, _allowanceFromTo - subtractedValue) { } catch { assert(false); } 
        assert(token.allowance(msg.sender, spender) ==  _allowanceFromTo - subtractedValue );
        assert(token.balanceOf(spender) ==  _balanceSpender);
        assert(token.totalSupply() == _totalSupply);
    }

    // Proves burning from non-zero address. Checks balance is decreased.
    function testprove_BurnFromNonZeroAddressFuzz(address account, uint256 amount) public {
        vm.assume(account != address(0) && amount > 0);
        token.mint(account, amount);
        uint256 initialBalance = token.balanceOf(account);
        token.burn(account, amount);
        assert(token.balanceOf(account) == initialBalance - amount);
    }

    // Proves burning zero tokens. Checks balance is not changed.
    function testprove_BurnZeroTokensFuzz(address account) public {
        vm.assume(account != address(0));
        uint256 initialBalance = token.balanceOf(account);
        token.burn(account, 0);
        assert(token.balanceOf(account) == initialBalance);
    }

    // Proves that approve works as expected.
    function testprove_ApproveNonZeroAmountFuzz(address owner, address spender, uint256 amount) public {
        vm.assume(owner != address(0) && spender != address(0) && amount > 0);
        vm.prank(owner);
        token.approve(spender, amount);
        assert(token.allowance(owner, spender) == amount);
    }

    // Proves approving zero amount
    function testprove_ApproveZeroAmountFuzz(address owner, address spender) public {
        vm.assume(owner != address(0) && spender != address(0));
        token.approve(spender, 0);
        assert(token.allowance(owner, spender) == 0);
    }

    // Proves approving max amount
    function testprove_ApproveMaxAmountFuzz(address owner, address spender) public {
        vm.assume(owner != address(0) && spender != address(0));
        vm.prank(owner);
        token.approve(spender, type(uint256).max);
        assert(token.allowance(owner, spender) == type(uint256).max);
    }

    // Proves that transfering zero amount reverts.
    function testprove_TransferZeroAmountFuzz(address sender, address recipient) public {
        vm.assume(sender != address(0) && recipient != address(0));
        vm.assume(sender != recipient);
        uint256 initialSenderBalance = token.balanceOf(sender);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        vm.prank(sender);
        token.transfer(recipient, 0);
        assert(token.balanceOf(sender) == initialSenderBalance);
        assert(token.balanceOf(recipient) == initialRecipientBalance);
    }

    // Proves that transferring from a zero address works.
    function testprove_TransferFromZeroAmountFuzz(address owner, address spender, address recipient) public {
        vm.assume(owner != address(0) && spender != address(0) && recipient != address(0));
        vm.assume(owner != recipient);
        uint256 initialOwnerBalance = token.balanceOf(owner);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        vm.prank(spender);
        token.transferFrom(owner, recipient, 0);
        assert(token.balanceOf(owner) == initialOwnerBalance);
        assert(token.balanceOf(recipient) == initialRecipientBalance);
    }

    // Proves that a zero address SHOULD have no tokens.
    function testprove_ZeroAddressHasNoTokenFuzz() public view {
        assert(token.balanceOf(address(0)) == 0);
    }

    // Proves that a msg.sender SHOULD be able to retrieve balance of himself/herself
    function testprove_MsgSenderCanRetrieveOwnBalanceFuzz(uint256 amount) public {
        token.mint(msg.sender, amount);
        assert(token.balanceOf(msg.sender) == amount);
    }

    // Proves that a msg.sender SHOULD be able to retrieve balance of another address
    function testprove_MsgSenderCanRetrieveOtherBalanceFuzz(address otherAddress, uint256 amount) public {
        vm.assume(otherAddress != address(0) && amount > 0);
        vm.assume(msg.sender != otherAddress);
        token.mint(otherAddress, amount);
        assert(token.balanceOf(otherAddress) == amount);
    }

    // Proves that consecutive approves from the same owner to the same spender
    function testprove_ConsecutiveApprovePositiveToPositiveFuzz(
        address owner,
        address spender,
        uint256 amount1,
        uint256 amount2
    ) public {
        vm.assume(owner != address(0) && spender != address(0));
        vm.prank(owner);
        token.approve(spender, amount1);
        vm.prank(owner);
        token.approve(spender, amount2);
        assert(token.allowance(owner, spender) == amount2);
    }
    // Proves that a transferFrom SHOULD NOT charge fees
    function testprove_TransferFromNoFeesFuzz(
        address owner,
        address spender,
        address recipient,
        uint256 amount
    ) public {
        vm.assume(owner != address(0) && spender != address(0) && recipient != address(0));
        vm.assume(owner != recipient);
        vm.assume(amount > 0);
        token.mint(owner, amount);
        vm.prank(owner);
        token.approve(spender, amount);
        uint256 initialOwnerBalance = token.balanceOf(owner);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        vm.prank(spender);
        token.transferFrom(owner, recipient, amount);
        assert(token.balanceOf(owner) == initialOwnerBalance - amount);
        assert(token.balanceOf(recipient) == initialRecipientBalance + amount);
    }
    // Proves that multiple calls of transferFrom SHOULD NOT be allowed once allowance reach zero even if the tokenSender's balance is more than the allowance
    function testproveFail_TransferFromAllowanceReachesZeroFuzz(
        address owner,
        address spender,
        address recipient,
        uint256 amount,
        uint256 allowance
    ) public {
        vm.assume(owner != address(0) && spender != address(0) && recipient != address(0));
        vm.assume(amount > 0 && allowance > 0 && allowance < amount);
        vm.assume(owner != recipient);

        token.mint(owner, amount);
        vm.prank(owner);
        token.approve(spender, allowance);

        uint256 initialOwnerBalance = token.balanceOf(owner);
        uint256 initialRecipientBalance = token.balanceOf(recipient);

        vm.prank(spender);
        token.transferFrom(owner, recipient, allowance);

        assert(token.balanceOf(owner) == initialOwnerBalance - allowance);
        assert(token.balanceOf(recipient) == initialRecipientBalance + allowance);

        vm.prank(spender);
        vm.expectRevert();
        token.transferFrom(owner, recipient, amount - allowance);
    }
    // Proves that multiple transfers SHOULD be allowed if the sender has enough balance and allowance
    function testprove_MultipleTransfersAllowed(
        address sender,
        address recipient,
        uint256 amount1,
        uint256 amount2
    ) public {
        vm.assume(sender != address(0) && recipient != address(0));
        vm.assume(amount1 > 0 && amount2 > 0);
        vm.assume(sender != recipient);

        uint256 totalAmount = amount1 + amount2;
        token.mint(sender, totalAmount);

        uint256 initialSenderBalance = token.balanceOf(sender);
        uint256 initialRecipientBalance = token.balanceOf(recipient);

        vm.prank(sender);
        token.transfer(recipient, amount1);
        vm.prank(sender);
        token.transfer(recipient, amount2);
        assert(token.balanceOf(sender) == initialSenderBalance - totalAmount);
        assert(token.balanceOf(recipient) == initialRecipientBalance + totalAmount);
    }

    // Proves that multiple transferFrom calls SHOULD be allowed if the owner has enough balance and allowance
    function testprove_MultipleTransferFromAllowedFuzz(
        address owner,
        address spender,
        address recipient,
        uint256 amount1,
        uint256 amount2
    ) public {
        vm.assume(owner != address(0) && spender != address(0) && recipient != address(0));
        vm.assume(amount1 > 0 && amount2 > 0);
        vm.assume(owner != recipient);
        uint256 totalAmount = amount1 + amount2;
        token.mint(owner, totalAmount);
        vm.prank(owner);
        token.approve(spender, totalAmount);
        uint256 initialOwnerBalance = token.balanceOf(owner);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        vm.prank(spender);
        token.transferFrom(owner, recipient, amount1);
        vm.prank(spender);
        token.transferFrom(owner, recipient, amount2);
        assert(token.balanceOf(owner) == initialOwnerBalance - totalAmount);
        assert(token.balanceOf(recipient) == initialRecipientBalance + totalAmount);
    }

    // Proves that the owner can approve the spender to spend the amount of tokens
    function testprove_SelfApprovePositiveAmountFuzz(address owner, uint256 amount) public {
        vm.assume(owner != address(0) && amount > 0);
        vm.prank(owner);
        token.approve(owner, amount);
        assert(token.allowance(owner, owner) == amount);
    }

    // Proves that the owner can approve the spender to spend the amount of tokens
    function testprove_SelfApproveAndTransferFromOwnAccountFuzz(
        address owner,
        address recipient,
        uint256 amount
    ) public {
        vm.assume(owner != address(0) && recipient != address(0) && amount > 0);
        vm.assume(owner != recipient);
        token.mint(owner, amount);
        vm.prank(owner);
        token.approve(owner, amount);
        uint256 initialOwnerBalance = token.balanceOf(owner);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        vm.prank(owner);
        token.transferFrom(owner, recipient, amount);
        assert(token.balanceOf(owner) == initialOwnerBalance - amount);
        assert(token.balanceOf(recipient) == initialRecipientBalance + amount);
    }

    // Proves that the owner can transfer the amount of tokens
    function testprove_SelfTransferPositiveAmountAllowedFuzz(address account, uint256 amount) public {
        vm.assume(account != address(0) && amount > 0);
        token.mint(account, amount);
        uint256 initialBalance = token.balanceOf(account);
        vm.prank(account);
        token.transfer(account, amount);
        assert(token.balanceOf(account) == initialBalance);
    }

    // Proves that the token receiver can transfer the amount of tokens from the token sender
    function testprove_TokenReceiverCanTransferFromTotalBalanceFuzz(
        address tokenSender,
        address tokenReceiver,
        uint256 amount
    ) public {
        vm.assume(tokenSender != address(0) && tokenReceiver != address(0) && amount > 0);
        vm.assume(tokenSender != tokenReceiver);
        token.mint(tokenSender, amount);
        vm.prank(tokenSender);
        token.approve(tokenReceiver, amount);
        uint256 initialSenderBalance = token.balanceOf(tokenSender);
        uint256 initialReceiverBalance = token.balanceOf(tokenReceiver);
        vm.prank(tokenReceiver);
        token.transferFrom(tokenSender, tokenReceiver, amount);
        assert(token.balanceOf(tokenSender) == initialSenderBalance - amount);
        assert(token.balanceOf(tokenReceiver) == initialReceiverBalance + amount);
    }

    // Proves that the msg.sender can transfer the amount of tokens from the token sender
    function testprove_MsgSenderCanTransferTotalBalanceFuzz(
        address tokenSender,
        address tokenReceiver,
        uint256 amount
    ) public {
        vm.assume(tokenSender != address(0) && tokenReceiver != address(0) && amount > 0);
        vm.assume(tokenSender != tokenReceiver);
        token.mint(tokenSender, amount);
        uint256 initialSenderBalance = token.balanceOf(tokenSender);
        uint256 initialReceiverBalance = token.balanceOf(tokenReceiver);
        vm.prank(tokenSender);
        token.transfer(tokenReceiver, amount);
        assert(token.balanceOf(tokenSender) == initialSenderBalance - amount);
        assert(token.balanceOf(tokenReceiver) == initialReceiverBalance + amount);
    }

    // Proves that the transfer function does not update the balances of the token sender and receiver
    function testprove_TransferDoesNotUpdateOtherBalances(
        address tokenSender,
        address tokenReceiver,
        address otherUser,
        uint256 amount
    ) public {
        vm.assume(tokenSender != address(0) && tokenReceiver != address(0) && otherUser != address(0));
        vm.assume(tokenSender != tokenReceiver && tokenSender != otherUser && tokenReceiver != otherUser);
        vm.assume(amount > 0);
        token.mint(tokenSender, amount);
        uint256 initialSenderBalance = token.balanceOf(tokenSender);
        uint256 initialReceiverBalance = token.balanceOf(tokenReceiver);
        uint256 initialOtherUserBalance = token.balanceOf(otherUser);
        vm.prank(tokenSender);
        token.transfer(tokenReceiver, amount);
        assert(token.balanceOf(tokenSender) == initialSenderBalance - amount);
        assert(token.balanceOf(tokenReceiver) == initialReceiverBalance + amount);
        assert(token.balanceOf(otherUser) == initialOtherUserBalance);
    }
    // Proves that the transferFrom function decreases the allowance of the spender
    function testprove_TransferFromDecreasesAllowanceFuzz(
        address tokenSender,
        address tokenReceiver,
        address spender,
        uint256 amount
    ) public {
        vm.assume(tokenSender != address(0) && tokenReceiver != address(0) && spender != address(0));
        vm.assume(tokenSender != tokenReceiver && tokenSender != spender && tokenReceiver != spender);
        vm.assume(amount > 0 && amount < type(uint256).max);
        token.mint(tokenSender, amount);
        vm.prank(tokenSender);
        token.approve(spender, amount);
        uint256 initialAllowance = token.allowance(tokenSender, spender);
        vm.prank(spender);
        token.transferFrom(tokenSender, tokenReceiver, amount);
        assert(token.allowance(tokenSender, spender) == initialAllowance - amount);
    }

    // Proves that the transferFrom function does not update the balances of the token sender and receiver
    function testprove_TransferFromDoesNotUpdateOtherBalancesFuzz(
        address tokenSender,
        address tokenReceiver,
        address spender,
        address otherUser,
        uint256 amount
    ) public {
        vm.assume(tokenSender != address(0) && tokenReceiver != address(0) && spender != address(0) && otherUser != address(0));
        vm.assume(tokenSender != tokenReceiver && tokenSender != spender && tokenSender != otherUser);
        vm.assume(tokenReceiver != spender && tokenReceiver != otherUser && spender != otherUser);
        vm.assume(amount > 0 && amount < type(uint256).max);
        token.mint(tokenSender, amount);
        vm.prank(tokenSender);
        token.approve(spender, amount);
        uint256 initialSenderBalance = token.balanceOf(tokenSender);
        uint256 initialReceiverBalance = token.balanceOf(tokenReceiver);
        uint256 initialOtherUserBalance = token.balanceOf(otherUser);
        vm.prank(spender);
        token.transferFrom(tokenSender, tokenReceiver, amount);
        assert(token.balanceOf(tokenSender) == initialSenderBalance - amount);
        assert(token.balanceOf(tokenReceiver) == initialReceiverBalance + amount);
        assert(token.balanceOf(otherUser) == initialOtherUserBalance);
    }

    // Proves that multiple transfers of zero amount are allowed
    function testprove_MultipleTransfersOfZeroAmountAllowedFuzz(
        address sender,
        address recipient,
        uint8 numTransfers
    ) public {
        vm.assume(sender != address(0) && recipient != address(0));
        vm.assume(sender != recipient);
        vm.assume(numTransfers > 0 && numTransfers < 4);
        uint256 initialSenderBalance = token.balanceOf(sender);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        for (uint256 i = 0; i < numTransfers; i++) {
            token.transfer(recipient, 0);
        }
        assert(token.balanceOf(sender) == initialSenderBalance);
        assert(token.balanceOf(recipient) == initialRecipientBalance);
    }

    // Proves that multiple transferFroms of zero amount are allowed
    function testprove_MultipleTransferFromsOfZeroAmountAllowedFuzz(
        address tokenSender,
        address tokenReceiver,
        address spender,
        uint8 numTransfers
    ) public {
        vm.assume(tokenSender != address(0) && tokenReceiver != address(0) && spender != address(0));
        vm.assume(tokenSender != tokenReceiver && tokenSender != spender && tokenReceiver != spender);
        vm.assume(numTransfers > 0 && numTransfers < 4);
        try token.approve(spender, 0) {
            // Should not revert
        } catch {
            assert(false);
        }
        numTransfers = 4;
        uint256 initialSenderBalance = token.balanceOf(tokenSender);
        uint256 initialReceiverBalance = token.balanceOf(tokenReceiver);
        for (uint256 i = 0; i < numTransfers; i++) {
            token.transferFrom(tokenSender, tokenReceiver, 0);
        }
        assert(token.balanceOf(tokenSender) == initialSenderBalance);
        assert(token.balanceOf(tokenReceiver) == initialReceiverBalance);
    }

    // Proves that self-approval of zero amount is allowed
    function testprove_SelfApproveZeroAmountAllowedFuzz(address owner) public {
        vm.assume(owner != address(0));
        vm.prank(owner);
        token.approve(owner, 0);
        assert(token.allowance(owner, owner) == 0);
    }

    // Proves that self-approval and transferFrom of zero amount are allowed
    function testprove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowedFuzz(
        address owner,
        address recipient
    ) public {
        vm.assume(owner != address(0) && recipient != address(0));
        vm.assume(owner != recipient);
        token.approve(owner, 0);
        uint256 initialOwnerBalance = token.balanceOf(owner);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        token.transferFrom(owner, recipient, 0);
        assert(token.balanceOf(owner) == initialOwnerBalance);
        assert(token.balanceOf(recipient) == initialRecipientBalance);
    }

    // Proves that self-transfer of zero amount is allowed
    function testprove_SelfTransferZeroAmountAllowedFuzz(address account) public {
        vm.assume(account != address(0));
        uint256 initialBalance = token.balanceOf(account);
        token.transfer(account, 0);
        assert(token.balanceOf(account) == initialBalance);
    }
    // Proves that a token receiver can transferFrom the total balance of a token
    function testprove_TokenReceiverCanTransferFromTotalBalanceZeroFuzz(
        address tokenSender,
        address tokenReceiver,
        address spender
    ) public {
        vm.assume(tokenSender != address(0) && tokenReceiver != address(0) && spender != address(0));
        vm.assume(tokenSender != tokenReceiver && tokenSender != spender && tokenReceiver != spender);
        token.approve(spender, 0);
        uint256 initialSenderBalance = token.balanceOf(tokenSender);
        uint256 initialReceiverBalance = token.balanceOf(tokenReceiver);
        token.transferFrom(tokenSender, tokenReceiver, 0);
        assert(token.balanceOf(tokenSender) == initialSenderBalance);
        assert(token.balanceOf(tokenReceiver) == initialReceiverBalance);
    }

    // Proves that a token sender can transfer the total balance of a token
    function testprove_MsgSenderCanTransferTotalBalanceZeroFuzz(
        address tokenSender,
        address tokenReceiver
    ) public {
        vm.assume(tokenSender != address(0) && tokenReceiver != address(0));
        vm.assume(tokenSender != tokenReceiver);
        uint256 initialSenderBalance = token.balanceOf(tokenSender);
        uint256 initialReceiverBalance = token.balanceOf(tokenReceiver);
        token.transfer(tokenReceiver, 0);
        assert(token.balanceOf(tokenSender) == initialSenderBalance);
        assert(token.balanceOf(tokenReceiver) == initialReceiverBalance);
    }

    // Proves that a token sender can transferFrom the total balance of a token to the zero address
    function testproveFail_TransferFromZeroAmountToZeroAddressRevertsFuzz(
        address tokenSender,
        address spender
    ) public {
        vm.assume(tokenSender != address(0) && spender != address(0));
        vm.assume(tokenSender != spender);
        token.approve(spender, 0);
        vm.prank(spender);
        vm.expectRevert();
        token.transferFrom(tokenSender, address(0), 0);
    }

    // Proves that a token sender can transfer the zero amount of a token to the zero address
    function testproveFail_TransferZeroAmountToZeroAddressRevertsFuzz(address sender) public {
        vm.assume(sender != address(0));
        vm.expectRevert();
        token.transfer(address(0), 0);
    }

    // Proves that the allowance of a token sender is updated after burning
    function testprove_AllowanceUpdatedAfterBurnFuzz(
        address tokenSender,
        address spender,
        uint256 amount
    ) public {
        vm.assume(tokenSender != address(0) && spender != address(0));
        vm.assume(tokenSender != spender);
        vm.assume(amount > 0 && amount < type(uint256).max);
        token.mint(tokenSender, amount);
        vm.prank(tokenSender);
        token.approve(spender, amount);
        token.burn(tokenSender, amount);
        assert(token.allowance(tokenSender, spender) == amount);
    }

    // Proves that the balance of a token sender is updated after burning. The balance of the tokenSender is decreased by the burned amount. 
    function testprove_BalanceUpdatedAfterBurnFuzz(
        address tokenApprover,
        address tokenApprovee,
        uint256 amount
    ) public {
        vm.assume(tokenApprover != address(0) && tokenApprovee != address(0));
        vm.assume(tokenApprover != tokenApprovee);
        vm.assume(amount > 0);
        token.mint(tokenApprover, amount);
        token.approve(tokenApprovee, amount);
        uint256 initialApproverBalance = token.balanceOf(tokenApprover);
        uint256 initialApproveeBalance = token.balanceOf(tokenApprovee);
        vm.prank(tokenApprovee);
        token.burn(tokenApprover, amount);
        assert(token.balanceOf(tokenApprover) == initialApproverBalance - amount);
        assert(token.balanceOf(tokenApprovee) == initialApproveeBalance);
    }
// *********************************************** Revertable properties ********************************************************

    // Proves approve reverts on zero address for msg.sender.
    function testproveFail_ApproveZeroAddressForMSGSenderFuzz(address spender, uint256 amount) public { // Only hevm
        vm.assume(msg.sender == address(0));
        vm.assume(spender != address(0));
        vm.prank(msg.sender);
        vm.expectRevert();
        token.approve(spender, amount);
    }

    // Proves approve reverts on zero address for spender.
    function testproveFail_ApproveZeroAddressFuzz(address spender, uint256 amount) public {
        vm.assume(msg.sender != address(0));
        vm.assume(spender == address(0));
        vm.prank(msg.sender);
        vm.expectRevert();
        token.approve(spender, amount);
    }

    // Proves minting to zero address reverts.
    function testproveFail_MintToZeroAddressFuzz(uint256 amount) public {
        vm.assume(amount > 0);
        
        // Tenta realizar a cunhagem de tokens para o endereço zero, o que deve falhar
        vm.expectRevert();
        token.mint(address(0), amount);
    }


    // Proves minting overflow. Checks minting fails.
    function testproveFail_MintOverflowFuzz(address account) public {
        vm.assume(account != address(0));

        token.mint(account, type(uint256).max);
        vm.expectRevert();
        token.mint(account, 1);
    }


    // Proves transferFrom reverts on zero address for msg.sender.
    function testproveFail_TransferFromZeroAddressForMSGSenderFuzz(address sender, address recipient, uint256 amount) public {
        vm.assume(msg.sender == address(0));
        vm.assume(recipient != address(0));
        vm.assume(sender != address(0));
            vm.prank(msg.sender);
            vm.expectRevert();
            token.transferFrom(sender, recipient, amount);
    }

    // Proves that transferring more tokens than the sender has reverts
    function testproveFail_TransferUnderBalancejFuzz(address recipient, uint256 amount) public {
        vm.assume(msg.sender != address(0) && recipient != address(0) && token.balanceOf(msg.sender) < amount);
            vm.prank(msg.sender);
            vm.expectRevert();
            token.transfer(recipient, amount);
    }

    // Proves that transferring from an account more tokens than it has reverts
    /*function testproveFail_TransferFromUnderBalanceiFuzz(address sender, address recipient, uint256 amount) public {
        vm.assume(msg.sender != address(0) && sender != address(0) && recipient != address(0));
            vm.assume(token.balanceOf(sender) < amount || token.allowance(sender, msg.sender) < amount);
                vm.prank(msg.sender);
                vm.expectRevert();
                token.transferFrom(sender, recipient, amount);
    }

    // Proves for overflow when increasing allowance
    function testproveFail_TransferFromNotEnoughAmountFuzz(address sender, address recipient, uint256 amount) public {
        vm.assume(msg.sender != address(0) && sender != address(0));
            vm.assume(token.balanceOf(sender) >= amount && token.allowance(sender, msg.sender) >= amount && recipient != address(0));
                vm.assume(type(uint256).max - token.balanceOf(recipient) < amount);
                    vm.prank(msg.sender);
                    vm.expectRevert();
                    token.transferFrom(sender, recipient, amount);
    }

    // Proves for overflow when increasing allowance
    function testproveFail_IncreaseAllowanceUnderAllowanceFuzz(address spender, uint256 addedValue) public {
        vm.assume(msg.sender != address(0) && spender != address(0));
            uint256 _allowanceFromTo = token.allowance(msg.sender, spender);
            vm.assume(_allowanceFromTo + addedValue < _allowanceFromTo || _allowanceFromTo + addedValue < addedValue);
                vm.prank(msg.sender);
                vm.expectRevert();
                token.approve(spender, _allowanceFromTo + addedValue);
    }

    // Proves for underflow when decreasing allowance
    function testproveFail_DecreaseAllowanceUnderAllowanceFuzz(address spender, uint256 subtractedValue) public {
        vm.assume(msg.sender != address(0) && spender != address(0));
            vm.prank(msg.sender);
            uint256 _allowanceFromTo = token.allowance(msg.sender, spender);
            vm.assume(_allowanceFromTo < subtractedValue);
                vm.prank(msg.sender);
                vm.ex
                token.approve(spender, _allowanceFromTo - subtractedValue);
    }

    // Proves for overflow when minting tokens
    function testproveFail_MintUnderSupplyFuzz(address account, uint256 amount) public {
        vm.assume(account != address(0));
            vm.assume(token.totalSupply() + amount < token.totalSupply());
                vm.expectRevert();
                token.mint(account, amount);
    }


    // Proves for underflow when burning tokens  
    function testproveFail_BurnUnderSupplyFuzz(address account, uint256 amount) public {
        vm.assume(account != address(0));
            vm.assume(token.balanceOf(account) < amount || token.totalSupply() < amount);
                vm.expectRevert();
                token.burn(account, amount);
    }

    // Proves burning from zero address reverts.
    function testproveFail_BurnFromZeroAddressFuzz(uint256 amount) public {
        vm.assume(amount > 0);
        vm.expectRevert();
        token.burn(address(0), amount);
    }


    // Proves burning an amount that is greater than the balance of the account reverts.
    function testproveFail_BurnUnderBalanceFuzz(address account, uint256 amount) public {
        vm.assume(account != address(0));
        
        token.mint(account, 100);
        
        vm.assume(amount > 100);
        vm.expectRevert();
        token.burn(account, amount);
    }

    // Proves approving from zero address reverts.
    function testproveFail_ApproveFromZeroAddressFuzz(address spender, uint256 amount) public {
        vm.assume(spender != address(0) && amount > 0);

        vm.prank(address(0));
        vm.expectRevert();
        token.approve(spender, amount);
    }


    // Proves approving to zero address reverts.
    function testproveFail_ApproveToZeroAddressFuzz(address owner, uint256 amount) public {
        vm.assume(owner != address(0) && amount > 0);

        vm.prank(owner);
        vm.expectRevert();
        token.approve(address(0), amount);
    }


    // Proves that transferring to the zero address reverts.
    function testproveFail_TransferToZeroAddressFuzz(address sender, uint256 amount) public {
        vm.assume(sender != address(0) && amount > 0);

        token.mint(sender, amount);
        
        vm.prank(sender);
        vm.expectRevert();
        token.transfer(address(0), amount);
    }


    // Proves that transferring from the zero address reverts.
    function testproveFail_TransferFromZeroAddressFuzz(address recipient, uint256 amount) public {
        vm.assume(recipient != address(0) && amount > 0);
        vm.expectRevert();
        token.transferFrom(address(0), recipient, amount);
    }


    // Proves that transferring more than the balance reverts.
    function testproveFail_TransferUnderBalanceFuzz(address sender, uint256 amount) public {
        vm.assume(sender != address(0) && amount > 0);

        token.mint(sender, amount - 1);
        
        vm.prank(sender);
        vm.expectRevert();
        token.transfer(address(0xdead), amount);
    }


    // Proves that transferring to the zero address reverts.
    function testproveFail_TransferFromToZeroAddress33Fuzz(address owner, address spender, uint256 amount) public {
        vm.assume(owner != address(0) && spender != address(0) && amount > 0);
        
        token.mint(owner, amount);
        token.approve(spender, amount);
        
        vm.prank(spender);
        vm.expectRevert();
        token.transferFrom(owner, address(0), amount);
    }

    // Proves that transferring from the zero address reverts.
    function testproveFail_TransferFromZeroAddressFuzz(address spender, address recipient, uint256 amount) public {
        vm.assume(spender != address(0) && recipient != address(0) && amount > 0);
        
        vm.prank(spender);
        vm.expectRevert();
        token.transferFrom(address(0), recipient, amount);
    }

    // Proves that transferring from an address with a balance under the amount reverts.
    function testproveFail_TransferFromUnderBalanceFuzz(address owner, address spender, uint256 amount) public {
        vm.assume(owner != address(0) && spender != address(0) && amount > 0);

        token.mint(owner, amount - 1);
        
        token.approve(spender, amount);
        
        vm.prank(spender);
        vm.expectRevert();
        token.transferFrom(owner, address(0xdead), amount);
    }*/
}

