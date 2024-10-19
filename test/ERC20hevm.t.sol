//SPDX-License-Identifier:MIT
pragma solidity >= 0.8.0;

import {Test, console2} from "forge-std/Test.sol";
import {ERC20Mock} from "../lib/openzeppelin-contracts/contracts/mocks/token/ERC20Mock.sol";
import {SafeERC20} from "../lib/openzeppelin-contracts/contracts/token/ERC20/utils/SafeERC20.sol";
import "../src/ERC20SOLMock.sol";
 /*contract ERC20SymbolicProperties is Test {
    using SafeERC20 for ERC20SolMock;

    ERC20SolMock token;

    function setUp() public {
        token = new ERC20SolMock();
    }

    // Proves approving a spender to transfer tokens. Checks allowance is set correctly.
    function prove_Approve(address spender, uint256 amount) public { 
        require(msg.sender != address(0) && spender != address(0));
        vm.prank(msg.sender);
        try token.approve(spender, amount) returns (bool success) { assert(success); } catch { assert(false); } 
        assert(token.allowance(msg.sender, spender) ==  amount);
    }

    // Proves minting new tokens. Checks total supply and recipient balance increase.
    function prove_Mint(address account, uint256 amount) public { 
        uint256 _balanceRecipient;
        uint256 _totalSupply;
        _totalSupply = token.totalSupply();
        require(account != address(0));
        _balanceRecipient = token.balanceOf(account);
        try token.mint(account, amount) {} catch { assert(false); } 
        assert(token.totalSupply() == _totalSupply + amount);
        assert(token.balanceOf(account) == _balanceRecipient + amount);
    }

    // Proves minting zero tokens. Checks balance is not changed.
    function prove_MintZeroTokens(address account) public {
        require(account != address(0), "Invalid arguments");
        uint256 initialBalance = token.balanceOf(account);
        token.mint(account, 0);
        assert(token.balanceOf(account) == initialBalance);
    }

    // Proves burning tokens, when using the same account. Checks total supply and recipient balance decrease.
    function prove_BurnSameAccount(address account, uint256 amount) public { 
        require(account != address(0));
        try token.mint(account, amount) {} catch { assert(false); } 
        uint256 _balanceRecipient = token.balanceOf(account);
        uint256 _totalSupply = token.totalSupply();
        require(_balanceRecipient >= amount);
        try token.burn(account, amount) {} catch { assert(false); } 
        assert(token.totalSupply() == _totalSupply - amount);
        assert(token.balanceOf(account) == _balanceRecipient - amount);
    }

    // Proves burning tokens, when using different accounts. Checks total supply and recipient balance decrease.
    function prove_BurnDifferentAccount(address account1, uint256 amount1, address account2, uint256 amount2) public { 
        require(account1 != address(0) && account2 != address(0) && account1 != account2);
        require(amount1 + amount2 >= amount1 || amount1 + amount2 >= amount2);
        try token.mint(account1, amount1) {} catch { assert(false); } 
        try token.mint(account2, amount2) {} catch { assert(false); } 
        uint256 _balanceRecipient1 = token.balanceOf(account1);
        uint256 _balanceRecipient2 = token.balanceOf(account2);
        uint256 _totalSupply = token.totalSupply();
        require(_balanceRecipient1 >= amount1);
        try token.burn(account1, amount1) {} catch { assert(false); } 
        assert(token.totalSupply() == _totalSupply - amount1);
        assert(token.balanceOf(account1) == _balanceRecipient1 - amount1);
        assert(token.balanceOf(account2) == _balanceRecipient2); // This must not change
    }

    // Proves transferring tokens. Checks sender and recipient balances update.
    function prove_Transfer(address recipient, uint256 preAmount, uint256 amount) public { 
        require(msg.sender != address(0));
        token.mint(msg.sender, preAmount);
        uint256 _balanceSender = token.balanceOf(msg.sender);
        uint256 _totalSupply = token.totalSupply();
        require(msg.sender != recipient && recipient != address(0) && _balanceSender >= amount);
        uint256 _balanceRecipient = token.balanceOf(recipient);
        vm.prank(msg.sender);
        try token.transfer(recipient, amount) returns (bool success) { assert(success); } catch { assert(false); } 
        assert(token.balanceOf(msg.sender) <=  _balanceSender - amount);
        assert(token.balanceOf(recipient) ==  _balanceRecipient + amount);
        assert(token.totalSupply() == _totalSupply);
    }

    // Proves transferring tokens via an approved allowance. Checks balances and allowance update.
    function prove_TransferFrom(address sender, address recipient, uint256 preAmount, uint256 amount) public { 
        require(msg.sender != address(0) && sender != address(0));
        token.mint(msg.sender, preAmount);
        uint256 _balanceSender = token.balanceOf(sender);
        uint256 _allowanceFromTo = token.allowance(sender, msg.sender);
        require(_balanceSender >= amount && _allowanceFromTo >= amount && recipient != address(0));
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
    function prove_IncreaseAllowance(address spender, uint256 addedValue) public { 
        require(msg.sender != address(0) && spender != address(0));
        uint256 _allowanceFromTo = token.allowance(msg.sender, spender);
        uint256 _balanceSpender = token.balanceOf(spender);
        uint256 _totalSupply = token.totalSupply();
        require(_allowanceFromTo + addedValue >= _allowanceFromTo && _allowanceFromTo + addedValue >= addedValue);
        vm.prank(msg.sender);
        try token.approve(spender, _allowanceFromTo + addedValue) { } catch { assert(false); } 
        assert(token.allowance(msg.sender, spender) ==  _allowanceFromTo + addedValue);
        assert(token.balanceOf(spender) ==  _balanceSpender);
        assert(token.totalSupply() == _totalSupply);
    }

    // Proves decreasing allowance. Checks allowance is decreased.
    function prove_DecreaseAllowance(address spender, uint256 subtractedValue) public { 
        require(msg.sender != address(0) && spender != address(0));
        vm.prank(msg.sender);
        uint256 _allowanceFromTo = token.allowance(msg.sender, spender);
        uint256 _balanceSpender = token.balanceOf(spender);
        uint256 _totalSupply = token.totalSupply();
        require(_allowanceFromTo >= subtractedValue);
        try token.approve(spender, _allowanceFromTo - subtractedValue) { } catch { assert(false); } 
        assert(token.allowance(msg.sender, spender) ==  _allowanceFromTo - subtractedValue );
        assert(token.balanceOf(spender) ==  _balanceSpender);
        assert(token.totalSupply() == _totalSupply);
    }

    // Proves burning from non-zero address. Checks balance is decreased.
    function prove_BurnFromNonZeroAddress(address account, uint256 amount) public {
        require(account != address(0) && amount > 0, "Invalid arguments");
        token.mint(account, amount);
        uint256 initialBalance = token.balanceOf(account);
        token.burn(account, amount);
        assert(token.balanceOf(account) == initialBalance - amount);
    }

    // Proves burning zero tokens. Checks balance is not changed.
    function prove_BurnZeroTokens(address account) public {
        require(account != address(0), "Invalid arguments");
        uint256 initialBalance = token.balanceOf(account);
        token.burn(account, 0);
        assert(token.balanceOf(account) == initialBalance);
    }

    // Proves that approve works as expected.
    function prove_ApproveNonZeroAmount(address owner, address spender, uint256 amount) public {
        require(owner != address(0) && spender != address(0) && amount > 0, "Invalid arguments");
        vm.prank(owner);
        token.approve(spender, amount);
        assert(token.allowance(owner, spender) == amount);
    }

    // Proves approving zero amount
    function prove_ApproveZeroAmount(address owner, address spender) public {
        require(owner != address(0) && spender != address(0), "Invalid arguments");
        token.approve(spender, 0);
        assert(token.allowance(owner, spender) == 0);
    }

    // Proves approving max amount
    function prove_ApproveMaxAmount(address owner, address spender) public {
        require(owner != address(0) && spender != address(0), "Invalid arguments");
        vm.prank(owner);
        token.approve(spender, type(uint256).max);
        assert(token.allowance(owner, spender) == type(uint256).max);
    }

    // Proves that transfering zero amount reverts.
    function prove_TransferZeroAmount(address sender, address recipient) public {
        require(sender != address(0) && recipient != address(0), "Invalid arguments");
        require(sender != recipient, "Invalid arguments");
        uint256 initialSenderBalance = token.balanceOf(sender);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        vm.prank(sender);
        token.transfer(recipient, 0);
        assert(token.balanceOf(sender) == initialSenderBalance);
        assert(token.balanceOf(recipient) == initialRecipientBalance);
    }

    // Proves that transferring from a zero address works.
    function prove_TransferFromZeroAmount(address owner, address spender, address recipient) public {
        require(owner != address(0) && spender != address(0) && recipient != address(0), "Invalid arguments");
        require(owner != recipient, "Invalid arguments");
        uint256 initialOwnerBalance = token.balanceOf(owner);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        vm.prank(spender);
        token.transferFrom(owner, recipient, 0);
        assert(token.balanceOf(owner) == initialOwnerBalance);
        assert(token.balanceOf(recipient) == initialRecipientBalance);
    }

    // Proves that a zero address SHOULD have no tokens.
    function prove_ZeroAddressHasNoToken() public view {
        assert(token.balanceOf(address(0)) == 0);
    }

    // Proves that a msg.sender SHOULD be able to retrieve balance of himself/herself
    function prove_MsgSenderCanRetrieveOwnBalance(uint256 amount) public {
        token.mint(msg.sender, amount);
        assert(token.balanceOf(msg.sender) == amount);
    }

    // Proves that a msg.sender SHOULD be able to retrieve balance of another address
    function prove_MsgSenderCanRetrieveOtherBalance(address otherAddress, uint256 amount) public {
        require(otherAddress != address(0) && amount > 0, "Invalid arguments");
        require(msg.sender != otherAddress, "msg.sender and otherAddress cannot be the same");
        token.mint(otherAddress, amount);
        assert(token.balanceOf(otherAddress) == amount);
    }

    // Proves that consecutive approves from the same owner to the same spender
    function prove_ConsecutiveApprovePositiveToPositive(
        address owner,
        address spender,
        uint256 amount1,
        uint256 amount2
    ) public {
        require(owner != address(0) && spender != address(0), "Invalid arguments");
        vm.prank(owner);
        token.approve(spender, amount1);
        vm.prank(owner);
        token.approve(spender, amount2);
        assert(token.allowance(owner, spender) == amount2);
    }
    // Proves that a transferFrom SHOULD NOT charge fees
    function prove_TransferFromNoFees(
        address owner,
        address spender,
        address recipient,
        uint256 amount
    ) public {
        require(owner != address(0) && spender != address(0) && recipient != address(0), "Invalid addresses");
        require(owner != recipient, "Invalid arguments");
        require(amount > 0, "Invalid amount");
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
    function proveFail_TransferFromAllowanceReachesZero(
        address owner,
        address spender,
        address recipient,
        uint256 amount,
        uint256 allowance
    ) public {
        require(owner != address(0) && spender != address(0) && recipient != address(0), "Invalid addresses");
        require(amount > 0 && allowance > 0 && allowance < amount, "Invalid amounts");
        require(owner != recipient, "Invalid arguments");

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
        token.transferFrom(owner, recipient, amount - allowance);
    }
    // Proves that multiple transfers SHOULD be allowed if the sender has enough balance and allowance
    function prove_MultipleTransfersAllowed(
        address sender,
        address recipient,
        uint256 amount1,
        uint256 amount2
    ) public {
        require(sender != address(0) && recipient != address(0), "Invalid addresses");
        require(amount1 > 0 && amount2 > 0, "Invalid amounts");
        require(sender != recipient, "Invalid arguments");

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
    function prove_MultipleTransferFromAllowed(
        address owner,
        address spender,
        address recipient,
        uint256 amount1,
        uint256 amount2
    ) public {
        require(owner != address(0) && spender != address(0) && recipient != address(0), "Invalid addresses");
        require(amount1 > 0 && amount2 > 0, "Invalid amounts");
        require(owner != recipient, "Invalid arguments");
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
    function prove_SelfApprovePositiveAmount(address owner, uint256 amount) public {
        require(owner != address(0) && amount > 0, "Invalid inputs");
        vm.prank(owner);
        token.approve(owner, amount);
        assert(token.allowance(owner, owner) == amount);
    }

    // Proves that the owner can approve the spender to spend the amount of tokens
    function prove_SelfApproveAndTransferFromOwnAccount(
        address owner,
        address recipient,
        uint256 amount
    ) public {
        require(owner != address(0) && recipient != address(0) && amount > 0, "Invalid inputs");
        require(owner != recipient, "Invalid arguments");
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
    function prove_SelfTransferPositiveAmountAllowed(address account, uint256 amount) public {
        require(account != address(0) && amount > 0, "Invalid inputs");
        token.mint(account, amount);
        uint256 initialBalance = token.balanceOf(account);
        vm.prank(account);
        token.transfer(account, amount);
        assert(token.balanceOf(account) == initialBalance);
    }

    // Proves that the token receiver can transfer the amount of tokens from the token sender
    function prove_TokenReceiverCanTransferFromTotalBalance(
        address tokenSender,
        address tokenReceiver,
        uint256 amount
    ) public {
        require(tokenSender != address(0) && tokenReceiver != address(0) && amount > 0, "Invalid inputs");
        require(tokenSender != tokenReceiver, "Invalid arguments");
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
    function prove_MsgSenderCanTransferTotalBalance(
        address tokenSender,
        address tokenReceiver,
        uint256 amount
    ) public {
        require(tokenSender != address(0) && tokenReceiver != address(0) && amount > 0, "Invalid inputs");
        require(tokenSender != tokenReceiver, "Invalid arguments");
        token.mint(tokenSender, amount);
        uint256 initialSenderBalance = token.balanceOf(tokenSender);
        uint256 initialReceiverBalance = token.balanceOf(tokenReceiver);
        vm.prank(tokenSender);
        token.transfer(tokenReceiver, amount);
        assert(token.balanceOf(tokenSender) == initialSenderBalance - amount);
        assert(token.balanceOf(tokenReceiver) == initialReceiverBalance + amount);
    }

    // Proves that the transfer function does not update the balances of the token sender and receiver
    function prove_TransferDoesNotUpdateOtherBalances(
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
    function prove_TransferFromDecreasesAllowance(
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
    function prove_TransferFromDoesNotUpdateOtherBalances(
        address tokenSender,
        address tokenReceiver,
        address spender,
        address otherUser,
        uint256 amount
    ) public {
        require(tokenSender != address(0) && tokenReceiver != address(0) && spender != address(0) && otherUser != address(0));
        require(tokenSender != tokenReceiver && tokenSender != spender && tokenSender != otherUser);
        require(tokenReceiver != spender && tokenReceiver != otherUser && spender != otherUser);
        require(amount > 0 && amount < type(uint256).max);
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
    function prove_MultipleTransfersOfZeroAmountAllowed(
        address sender,
        address recipient,
        uint8 numTransfers
    ) public {
        require(sender != address(0) && recipient != address(0));
        require(sender != recipient);
        require(numTransfers > 0 && numTransfers < 4);
        uint256 initialSenderBalance = token.balanceOf(sender);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        for (uint256 i = 0; i < numTransfers; i++) {
            token.transfer(recipient, 0);
        }
        assert(token.balanceOf(sender) == initialSenderBalance);
        assert(token.balanceOf(recipient) == initialRecipientBalance);
    }

    // Proves that multiple transferFroms of zero amount are allowed
    function prove_MultipleTransferFromsOfZeroAmountAllowed(
        address tokenSender,
        address tokenReceiver,
        address spender,
        uint8 numTransfers
    ) public {
        require(tokenSender != address(0) && tokenReceiver != address(0) && spender != address(0));
        require(tokenSender != tokenReceiver && tokenSender != spender && tokenReceiver != spender);
        require(numTransfers > 0 && numTransfers < 4);
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
    function prove_SelfApproveZeroAmountAllowed(address owner) public {
        require(owner != address(0));
        vm.prank(owner);
        token.approve(owner, 0);
        assert(token.allowance(owner, owner) == 0);
    }

    // Proves that self-approval and transferFrom of zero amount are allowed
    function prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(
        address owner,
        address recipient
    ) public {
        require(owner != address(0) && recipient != address(0));
        require(owner != recipient);
        token.approve(owner, 0);
        uint256 initialOwnerBalance = token.balanceOf(owner);
        uint256 initialRecipientBalance = token.balanceOf(recipient);
        token.transferFrom(owner, recipient, 0);
        assert(token.balanceOf(owner) == initialOwnerBalance);
        assert(token.balanceOf(recipient) == initialRecipientBalance);
    }

    // Proves that self-transfer of zero amount is allowed
    function prove_SelfTransferZeroAmountAllowed(address account) public {
        require(account != address(0));
        uint256 initialBalance = token.balanceOf(account);
        token.transfer(account, 0);
        assert(token.balanceOf(account) == initialBalance);
    }
    // Proves that a token receiver can transferFrom the total balance of a token
    function prove_TokenReceiverCanTransferFromTotalBalanceZero(
        address tokenSender,
        address tokenReceiver,
        address spender
    ) public {
        require(tokenSender != address(0) && tokenReceiver != address(0) && spender != address(0));
        require(tokenSender != tokenReceiver && tokenSender != spender && tokenReceiver != spender);
        token.approve(spender, 0);
        uint256 initialSenderBalance = token.balanceOf(tokenSender);
        uint256 initialReceiverBalance = token.balanceOf(tokenReceiver);
        token.transferFrom(tokenSender, tokenReceiver, 0);
        assert(token.balanceOf(tokenSender) == initialSenderBalance);
        assert(token.balanceOf(tokenReceiver) == initialReceiverBalance);
    }

    // Proves that a token sender can transfer the total balance of a token
    function prove_MsgSenderCanTransferTotalBalanceZero(
        address tokenSender,
        address tokenReceiver
    ) public {
        require(tokenSender != address(0) && tokenReceiver != address(0));
        require(tokenSender != tokenReceiver);
        uint256 initialSenderBalance = token.balanceOf(tokenSender);
        uint256 initialReceiverBalance = token.balanceOf(tokenReceiver);
        token.transfer(tokenReceiver, 0);
        assert(token.balanceOf(tokenSender) == initialSenderBalance);
        assert(token.balanceOf(tokenReceiver) == initialReceiverBalance);
    }

    // Proves that a token sender can transferFrom the total balance of a token to the zero address
    function proveFail_TransferFromZeroAmountToZeroAddressReverts(
        address tokenSender,
        address spender
    ) public {
        require(tokenSender != address(0) && spender != address(0));
        require(tokenSender != spender);
        token.approve(spender, 0);
        vm.prank(spender);
        token.transferFrom(tokenSender, address(0), 0);
    }

    // Proves that a token sender can transfer the zero amount of a token to the zero address
    function proveFail_TransferZeroAmountToZeroAddressReverts(address sender) public {
        require(sender != address(0));
        token.transfer(address(0), 0);
    }

    // Proves that the allowance of a token sender is updated after burning
    function prove_AllowanceUpdatedAfterBurn(
        address tokenSender,
        address spender,
        uint256 amount
    ) public {
        require(tokenSender != address(0) && spender != address(0));
        require(tokenSender != spender);
        require(amount > 0 && amount < type(uint256).max);
        token.mint(tokenSender, amount);
        vm.prank(tokenSender);
        token.approve(spender, amount);
        token.burn(tokenSender, amount);
        assert(token.allowance(tokenSender, spender) == amount);
    }

    // Proves that the balance of a token sender is updated after burning. The balance of the tokenSender is decreased by the burned amount. 
    function prove_BalanceUpdatedAfterBurn(
        address tokenApprover,
        address tokenApprovee,
        uint256 amount
    ) public {
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
// *********************************************** Revertable properties ********************************************************

    // Proves approve reverts on zero address for msg.sender.
    function proveFail_ApproveZeroAddressForMSGSender(address spender, uint256 amount) public { // Only hevm
        require(msg.sender == address(0) && spender != address(0));
        vm.prank(msg.sender);
        token.approve(spender, amount);
    }

    // Proves approve reverts on zero address for spender.
    function proveFail_ApproveZeroAddress(address spender, uint256 amount) public {
        require(msg.sender != address(0) && spender == address(0));
        vm.prank(msg.sender);
        token.approve(spender, amount);
    }

    // Proves minting to zero address reverts.
    function proveFail_MintToZeroAddress(uint256 amount) public {
        require(amount > 0, "Invalid arguments");

        token.mint(address(0), amount);
    }


    // Proves minting overflow. Checks minting fails.
    function proveFail_MintOverflow(address account) public {
        require(account != address(0), "Invalid arguments");

        token.mint(account, type(uint256).max);

        token.mint(account, 1);
    }


    // Proves transferFrom reverts on zero address for msg.sender.
    function proveFail_TransferFromZeroAddressForMSGSender(address sender, address recipient, uint256 amount) public {
        require(msg.sender == address(0) && recipient != address(0) && sender != address(0));
            vm.prank(msg.sender);
            
            token.transferFrom(sender, recipient, amount);
    }

    // Proves that transferring more tokens than the sender has reverts
    function proveFail_TransferUnderBalancej(address recipient, uint256 amount) public {
        require(msg.sender != address(0) && recipient != address(0) && token.balanceOf(msg.sender) < amount);
            vm.prank(msg.sender);
            
            token.transfer(recipient, amount);
    }

    // Proves that transferring from an account more tokens than it has reverts
    function proveFail_TransferFromUnderBalancei(address sender, address recipient, uint256 amount) public {
        require(msg.sender != address(0) && sender != address(0) && recipient != address(0));
            require(token.balanceOf(sender) < amount || token.allowance(sender, msg.sender) < amount);
                vm.prank(msg.sender);
                
                token.transferFrom(sender, recipient, amount);
    }


    // Proves for underflow when burning tokens  
    function proveFail_BurnUnderSupply(address account, uint256 amount) public {
        require(account != address(0));
            require(token.balanceOf(account) < amount || token.totalSupply() < amount);
                
                token.burn(account, amount);
    }

    // Proves burning from zero address reverts.
    function proveFail_BurnFromZeroAddress(uint256 amount) public {
        require(amount > 0, "Invalid arguments");

        token.burn(address(0), amount);
    }


    // Proves burning an amount that is greater than the balance of the account reverts.
    function proveFail_BurnUnderBalance(address account, uint256 amount) public {
        require(account != address(0), "Invalid arguments");
        
        token.mint(account, 100);
        
        require(amount > 100, "Burn amount must be greater than account balance");
        
        token.burn(account, amount);
    }

    // Proves approving from zero address reverts.
    function proveFail_ApproveFromZeroAddress(address spender, uint256 amount) public {
        require(spender != address(0) && amount > 0, "Invalid arguments");

        vm.prank(address(0));

        token.approve(spender, amount);
    }


    // Proves approving to zero address reverts.
    function proveFail_ApproveToZeroAddress(address owner, uint256 amount) public {
        require(owner != address(0) && amount > 0, "Invalid arguments");

        vm.prank(owner);

        token.approve(address(0), amount);
    }


    // Proves that transferring to the zero address reverts.
    function proveFail_TransferToZeroAddress(address sender, uint256 amount) public {
        require(sender != address(0) && amount > 0, "Invalid arguments");

        token.mint(sender, amount);
        
        vm.prank(sender);

        token.transfer(address(0), amount);
    }


    // Proves that transferring from the zero address reverts.
    function proveFail_TransferFromZeroAddress(address recipient, uint256 amount) public {
        require(recipient != address(0) && amount > 0, "Invalid arguments");

        token.transferFrom(address(0), recipient, amount);
    }


    // Proves that transferring more than the balance reverts.
    function proveFail_TransferUnderBalance(address sender, uint256 amount) public {
        require(sender != address(0) && amount > 0, "Invalid arguments");

        token.mint(sender, amount - 1);
        
        vm.prank(sender);

        token.transfer(address(0xdead), amount);
    }


    // Proves that transferring to the zero address reverts.
    function proveFail_TransferFromToZeroAddress33(address owner, address spender, uint256 amount) public {
        require(owner != address(0) && spender != address(0) && amount > 0, "Invalid arguments");
        
        token.mint(owner, amount);
        token.approve(spender, amount);
        
        vm.prank(spender);
        
        token.transferFrom(owner, address(0), amount);
    }

    // Proves that transferring from the zero address reverts.
    function proveFail_TransferFromZeroAddress(address spender, address recipient, uint256 amount) public {
        require(spender != address(0) && recipient != address(0) && amount > 0, "Invalid arguments");
        
        vm.prank(spender);
        
        token.transferFrom(address(0), recipient, amount);
    }

    // Proves that transferring from an address with a balance under the amount reverts.
    function proveFail_TransferFromUnderBalance(address owner, address spender, uint256 amount) public {
        require(owner != address(0) && spender != address(0) && amount > 0, "Invalid arguments");

        token.mint(owner, amount - 1);
        
        token.approve(spender, amount);
        
        vm.prank(spender);
        
        token.transferFrom(owner, address(0xdead), amount);
    }
}*/