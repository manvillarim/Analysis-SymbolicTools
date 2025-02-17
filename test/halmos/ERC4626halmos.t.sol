// SPDX-License-Identifier: AGPL-3.0-only
pragma solidity ^0.8.17;

import {Test, console2} from "forge-std/Test.sol";
import {ERC20Mock} from "lib/openzeppelin-contracts/contracts/mocks/token/ERC20Mock.sol";
import {ERC4626Mock} from "lib/openzeppelin-contracts/contracts/mocks/token/ERC4626Mock.sol";
import {Math} from "lib/openzeppelin-contracts/contracts/utils/math/Math.sol";
import "src/solmate/token/ERC4626Mock.sol";
import "src/solmate/token/ERC20SOLMock.sol";

contract ERC4626SymbolicProperties is Test {
    using Math for uint256;
    ERC20SolMock asset;
    ERC4626SMock vault;

    function setUp() public {
        asset = new ERC20SolMock();
        vault = new ERC4626SMock(asset);
    }

    // Proves that minting tokens increases the balance of the recipient
    function prove_mint_increases_balance(address recipient, uint256 amount) public {
        uint256 balanceBefore = vault.balanceOf(recipient);
        vm.prank(recipient);
        vault.mint(recipient, amount);
        uint256 balanceAfter = vault.balanceOf(recipient);
        assert(balanceAfter == balanceBefore + amount);
    }

    // Proves that burning tokens decreases the balance of the account
    function prove_burn_decreases_balance(address account, uint256 amount) public {
        uint256 balanceBefore = vault.balanceOf(account);
        require(balanceBefore >= amount, "Insufficient balance");
        require(vault.totalSupply() >= amount, "Insufficient supply");
        vm.prank(account);
        vault.burn(account, amount);
        uint256 balanceAfter = vault.balanceOf(account);
        assert(balanceAfter == balanceBefore - amount);
    }

    // Proves that transfer decreases the balance of the sender and increases the balance of the recipient
    function prove_transfer_updates_balances(address sender, address recipient, uint256 amount) public {
        require(sender != address(0) && recipient != address(0), "Invalid addresses");
        require(sender != recipient, "Sender and recipient cannot be the same");
        vm.prank(sender);
        vault.mint(sender, amount);
        uint256 senderBalanceBefore = vault.balanceOf(sender);
        uint256 recipientBalanceBefore = vault.balanceOf(recipient);
        require(senderBalanceBefore >= amount, "Insufficient balance");
        vm.prank(sender);
        bool success = vault.transfer(recipient, amount);
        require(success, "Transfer failed");
        uint256 senderBalanceAfter = vault.balanceOf(sender);
        uint256 recipientBalanceAfter = vault.balanceOf(recipient);
        assert(senderBalanceAfter == senderBalanceBefore - amount);
        assert(recipientBalanceAfter == recipientBalanceBefore + amount);
    }

    // Proves that transferFrom decreases the balance of the sender and increases the balance of the recipient
    function prove_transferFrom_updates_balances(address sender, address recipient, address spender, uint256 amount) public {
        require(sender != address(0) && recipient != address(0) && spender != address(0), "Invalid addresses");
        require(sender != recipient, "Sender and recipient cannot be the same");

        vm.prank(sender);
        vault.mint(sender, amount);
        vm.prank(sender);
        vault.approve(spender, amount);

        uint256 senderBalanceBefore = vault.balanceOf(sender);
        uint256 recipientBalanceBefore = vault.balanceOf(recipient);

        require(senderBalanceBefore >= amount, "Insufficient balance");

        vm.prank(spender);
        bool success = vault.transferFrom(sender, recipient, amount);
        require(success, "TransferFrom failed");

        uint256 senderBalanceAfter = vault.balanceOf(sender);
        uint256 recipientBalanceAfter = vault.balanceOf(recipient);

        assert(senderBalanceAfter == senderBalanceBefore - amount);
        assert(recipientBalanceAfter == recipientBalanceBefore + amount);
    }

    // Proves that approve sets the correct allowance
    function prove_approvesets_allowance(address owner, address spender, uint256 amount) public {
        require(owner != address(0) && spender != address(0), "Invalid addresses");

        vm.prank(owner);
        vault.approve(spender, amount);

        uint256 allowance = vault.allowance(owner, spender);
        assert(allowance == amount);
    }

    // Proves that approve overwrites the existing allowance
    function prove_approveoverwrites_allowance(address owner, address spender, uint256 amount1, uint256 amount2) public {
        require(owner != address(0) && spender != address(0), "Invalid addresses");
        require(amount1 != amount2, "Amounts should be different");

        vm.prank(owner);
        vault.approve(spender, amount1);

        vm.prank(owner);
        vault.approve(spender, amount2);

        uint256 allowance = vault.allowance(owner, spender);
        assert(allowance == amount2);
    }

    // Proves that convertToShares is greater than or equal to previewDeposit
    function prove_convertToShares_gte_previewDeposit(uint256 initialAssets, uint256 assets) public {
        // Set up the vault with some initial state
        asset.mint(address(this), initialAssets);
        asset.approve(address(vault), initialAssets);
        vault.deposit(initialAssets, address(this));

        // This needs a previous state
        require(msg.sender != address(this));
        vm.prank(msg.sender);
        assert(vault.convertToShares(assets) >= vault.previewDeposit(assets));
    }

    // Proves that convertToShares rounds down towards 0
    function prove_convertToShares_rounds_down_towards_0(uint256 initialAssets, uint256 assets) public {
        require(msg.sender != address(0) && msg.sender != address(this));

        // Set up the vault with some initial state
        asset.mint(address(this), initialAssets);
        asset.approve(address(vault), initialAssets);
        vault.deposit(initialAssets, address(this));

        require(msg.sender != address(this));
        vm.prank(msg.sender);
        uint256 expectedShares = assets.mulDiv(vault.totalSupply(), vault.totalAssets(), Math.Rounding.Floor);

        vm.prank(msg.sender);
        uint256 actualShares = vault.convertToShares(assets);
        assert(actualShares <= expectedShares);
    }

    // Proves that the share price is maintained after minting shares
    function prove_share_price_maintained_after_mint(uint256 shares, address receiver) public {
        // Set up the initial state of the vault
        require(vault.totalAssets() == 0 && vault.totalSupply() == 0, "Vault should be initially empty");

        // Mint tokens to the vault
        asset.mint(address(this), shares);
        vm.prank(address(this));
        asset.transfer(address(vault), shares);

        // Get the preview assets for the given shares
        uint256 previewAssets = vault.previewMint(shares);

        // Mint shares to the receiver
        require(receiver != address(this) && receiver != address(0), "Invalid receiver address");
        vm.prank(receiver);
        vault.mint(shares, receiver);

        // Assert the expected behavior
        assert(vault.totalAssets() == previewAssets);
        assert(vault.totalSupply() == shares);
        assert(vault.balanceOf(receiver) == shares);
    }

    // Proves that the share price is maintained after burning shares
    function prove_convertToAssets_lte_previewMint(uint256 shares) public {
        // Setup
        require(shares > 0);
        require(msg.sender != address(0) && msg.sender != address(this), "Invalid sender address");
        vm.prank(msg.sender);
        asset.mint(address(this), shares);
        asset.approve(address(vault), shares);
        vm.prank(address(this));
        vault.deposit(shares, address(this));

        // Set up the initial state of the vault
        require(vault.totalAssets() > 0 && vault.totalSupply() > 0, "Vault should not be empty");

        // Get the preview assets for the given shares
        uint256 previewAssets = vault.previewMint(shares);

        // Convert shares to assets
        uint256 convertedAssets = vault.convertToAssets(shares);

        // Assert the expected behavior
        assert(convertedAssets <= previewAssets); // Z3 is not smart enough to prove this
    }

    // Proves that convertToAssets is less than or equal to previewMint
    function prove_convertToAssets_rounds_down_towards_0(uint256 shares) public {
        // Setup
        require(msg.sender != address(0) && msg.sender != address(this), "Invalid sender address");
        vm.prank(msg.sender);
        asset.mint(address(this), shares);
        asset.approve(address(vault), shares);
        vm.prank(address(this));
        vault.deposit(shares, address(this));

        // Set up the initial state of the vault
        require(vault.totalAssets() > 0 && vault.totalSupply() > 0, "Vault should not be empty");

        // Get the preview redeem and convert to assets values
        uint256 previewRedeemAssets = vault.previewRedeem(shares);
        uint256 convertedAssets = vault.convertToAssets(shares);

        // Assert the expected behavior
        assert(convertedAssets <= previewRedeemAssets);
        assert(convertedAssets == previewRedeemAssets.mulDiv(vault.totalAssets(), vault.totalSupply(), Math.Rounding.Floor));
    }

    // Proves that maxDeposit returns the maximum value of the UINT256 type
    function prove_maxDeposit_returns_correct_value(address receiver) public view{
        assert(vault.maxDeposit(receiver) == 2 ** 256 - 1);
    }

    // Proves that maxMint returns the the maximum value of the UINT256 type
    function prove_maxMint_returns_correct_value(address receiver) public view{
        assert(vault.maxMint(receiver) == 2 ** 256 - 1);
    }

    // Proves that previewDeposit is less than or equal to deposit
    function prove_previewDepositRelationToDeposit(uint256 assets, address receiver) public {
        // Setup
        require(receiver != address(0) && receiver != address(this) && receiver != msg.sender, "Invalid receiver address");
        require(assets > 0, "Invalid asset amount");

        vm.prank(receiver);
        asset.mint(receiver, assets);
        asset.approve(address(vault), assets);

        // Get the preview deposit value
        uint256 previewDepositShares = vault.previewDeposit(assets);

        // Deposit assets into the vault
        vm.prank(receiver);
        uint256 depositedShares = vault.deposit(assets, receiver);

        // Assert the expected behavior
        assert(depositedShares <= previewDepositShares);
    }

    // Proves that previewRedeem is less than or equal to redeem
    function prove_previewRedeem_lte_redeem(address owner, uint256 redeemShares) public {
        require(msg.sender != address(0) && msg.sender != address(this) && owner!= address(0) && owner!= address(this));    
        // Setup

        uint256 totalAssets;
        asset.mint(address(this), totalAssets);
        asset.approve(address(vault), totalAssets);
        vault.deposit(totalAssets, owner);

        // Execution
        uint256 previewAssets = vault.previewRedeem(redeemShares);
        uint256 ownerAssetsBefore = asset.balanceOf(owner);
        uint256 redeemedAssets = vault.redeem(redeemShares, owner, owner);

        // Validation
        assert(redeemedAssets >= previewAssets);
        uint256 ownerAssetsAfter = asset.balanceOf(owner);
        assert(ownerAssetsAfter - ownerAssetsBefore >= redeemedAssets);
    }

    // Proves the integrity of the deposit function
    function prove_integrity_of_deposit(uint256 depositAmount, address depositor) public {
        vm.assume(depositAmount > 0);
        vm.assume(depositor != address(0)); // Assume a non-zero address

        asset.mint(depositor, depositAmount);
        vm.prank(depositor); // Use vm.prank to execute the following operations as the depositor
        asset.approve(address(vault), depositAmount);

        uint256 expectedShares = vault.previewDeposit(depositAmount);
        uint256 totalAssetsBefore = asset.balanceOf(address(vault));
        uint256 depositorSharesBefore = vault.balanceOf(depositor);

        uint256 shares = vault.deposit(depositAmount, depositor);

        // Validation
        uint256 totalAssetsAfter = asset.balanceOf(address(vault));
        uint256 depositorSharesAfter = vault.balanceOf(depositor);

        assert(depositorSharesAfter == depositorSharesBefore + shares);
        assert(totalAssetsAfter == totalAssetsBefore + depositAmount);
        assert(depositorSharesAfter <= vault.totalSupply());
        assert(shares == expectedShares);
    }


    // Proves the integrity of the withdraw function
    function prove_integrity_of_withdraw() public { // Times out with any genenalization
        uint256 depositAmount = 1000;
        asset.mint(address(this), depositAmount);
        asset.approve(address(vault), depositAmount);

        //uint256 shares = vault.deposit(depositAmount, address(this));

        uint256 withdrawAmount = 500;
        uint256 expectedShares = vault.previewWithdraw(withdrawAmount);

        uint256 withdrawnShares = vault.withdraw(withdrawAmount, address(this), address(this));

        assert(withdrawnShares == expectedShares);
        assert(asset.balanceOf(address(vault)) == depositAmount - withdrawAmount);
    }

    // Proves the integrity of the redeem function
    function prove_integrity_of_redeem() public {
        uint256 depositAmount = 1000;
        asset.mint(address(this), depositAmount);
        asset.approve(address(vault), depositAmount);

        uint256 shares = vault.deposit(depositAmount, address(this));

        uint256 redeemShares = shares / 2;
        uint256 expectedAssets = vault.previewRedeem(redeemShares);

        uint256 redeemedAssets = vault.redeem(redeemShares, address(this), address(this));

        assert(redeemedAssets == expectedAssets);
        assert(asset.balanceOf(address(this)) == redeemedAssets);
        assert(vault.balanceOf(address(this)) == shares - redeemShares);
    }

// ***************** Revert Test Cases ****************************

    // Proves that minting to the zero address reverts
    function proveFail_mint_to_zero_address_reverts(uint256 amount) public {
        try vault.mint(address(0), amount) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that minting an amount that would cause an overflow reverts
    function proveFail_mint_overflow_reverts(address recipient) public {
        require(recipient!= address(0), "ERC4626: mint to the zero address");
        vault.mint(recipient, 1);
        try vault.mint(recipient, type(uint256).max) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that burning more tokens than the account's balance reverts
    function proveFail_burn_exceeds_balance_reverts(address account, uint256 amount) public {
        vm.prank(account);
        vault.mint(account, amount);
        try vault.burn(account, amount + 1) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that burning tokens from the zero address reverts
    function proveFail_burn_from_zero_address_reverts(uint256 amount) public {
        try vault.burn(address(0), amount) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that transfer reverts when the sender's balance is insufficient
    function proveFail_transfer_insufficient_balance_reverts(address sender, address recipient, uint256 amountInit, uint256 amount) public {
        vm.prank(sender);
        vault.mint(sender, amountInit);
        uint256 senderBalanceBefore = vault.balanceOf(sender);
        require(amount > senderBalanceBefore, "Insufficient balance");
        try vault.transfer(recipient, amount) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that transfer reverts when transferring to the zero address
    function proveFail_transfer_to_zero_address_reverts(address sender, uint256 amount) public {
        vm.prank(sender);
        vault.mint(sender, amount);
        try vault.transfer(address(0), amount) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that transfer reverts when transferring from the zero address
    function proveFail_transfer_from_zero_address_reverts(address recipient, uint256 amount) public {
        require(recipient!= address(0), "ERC4626: transfer to the zero address");
        vm.prank(address(0));
        try vault.transfer(recipient, amount) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that transferFrom reverts when the sender's balance is insufficient
    function proveFail_transferFrom_insufficient_balance_reverts(address sender, address recipient, address spender, uint256 amountInit, uint256 amount) public {
        vm.prank(sender);
        vault.mint(sender, amountInit);
        vm.prank(sender);
        vault.approve(spender, amountInit);

        uint256 senderBalanceBefore = vault.balanceOf(sender);
        require(amount > senderBalanceBefore, "Insufficient balance");

        vm.prank(spender);
        try vault.transferFrom(sender, recipient, amount) {
                assert(false);
            } catch {
                assert(true);
            }
    }

    // Proves that transferFrom reverts when the spender's allowance is insufficient
    function proveFail_transferFrom_insufficient_allowance_reverts(address sender, address recipient, address spender, uint256 amount) public {
        vm.prank(sender);
        vault.mint(sender, amount);
        vm.prank(sender);
        vault.approve(spender, amount - 1);

        vm.prank(spender);
        try vault.transferFrom(sender, recipient, amount) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that transferFrom reverts when transferring to the zero address
    function proveFail_transferFrom_to_zero_address_reverts(address sender, address spender, uint256 amount) public {
        vm.prank(sender);
        vault.mint(sender, amount);
        vm.prank(sender);
        vault.approve(spender, amount);
        vm.prank(spender);
        try vault.transferFrom(sender, address(0), amount) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that transferFrom reverts when transferring from the zero address
    function proveFail_transferFrom_from_zero_address_reverts(address recipient, address spender, uint256 amount) public {
        require(recipient != address(0), "ERC4626: transfer to the zero address");
        vm.prank(spender);
        try vault.transferFrom(address(0), recipient, amount) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that approve reverts when approving the zero address
    function proveFail_approvezero_address_reverts(address owner, uint256 amount) public {
        require(owner!= address(0), "ERC4626: approve from the zero address");
        vm.prank(owner);
        try vault.approve(address(0), amount) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // Proves that approve reverts when the owner is the zero address
    function proveFail_approvefrom_zero_address_reverts(address spender, uint256 amount) public {
        require(spender!= address(0), "ERC4626: approve to the zero address");
        vm.prank(address(0));
        try vault.approve(spender, amount) {
            assert(false);
        } catch {
            assert(true);
        }
    }

    // The deposit function is expected to revert if msg.sender is this contract
    function proveFail_depositWithMSGSenderEqualsThis(address account, uint256 amount, uint256 assets, address receiver) public {
        // Setup
        require(account != address(0), "ERC4626: deposit from the zero address");
        require(receiver != address(0), "ERC4626: deposit to the zero address");
        require(account != receiver, "ERC4626: deposit to the same address");
        require(amount > 0 && assets > 0, "amount should be greater than zero");
        require(amount >= assets);

        vm.prank(account);
        vault.mint(account, amount);

        //uint256 _totalAssets = asset.balanceOf(address(vault));

        // Execution
        vm.prank(account);
        try vault.deposit(assets, receiver) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The deposit function is expected to revert if receiver is this contract
    function proveFail_depositWithReceiverEqualsThis(address msg_sender, address account, uint256 amount, uint256 assets, address receiver) public {
        require(msg_sender != address(this));
        require(receiver == address(this));
        require(amount > 0 && assets > 0, "amount should be greater than zero");
        require(amount >= assets);

        vm.prank(msg_sender);
        vault.mint(account, amount);

        vm.prank(msg_sender);
        try vault.deposit(assets, receiver) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The deposit function is expected to revert if amount < assets
    function proveFail_depositWithAmountLessThanAssets(address msg_sender, address account, uint256 amount, uint256 assets, address receiver) public {
        require(msg_sender != address(this));
        require(receiver != address(this));
        require(amount < assets);

        vm.prank(msg_sender);
        vault.mint(account, amount);

        //vm.prank(msg_sender);
        //uint256 _totalAssets = asset.balanceOf(address(this));

        vm.prank(msg_sender);
        try vault.deposit(assets, receiver) {
            assert(false);
        }
        catch {
            assert(true);
        }

    }


    // The redeem function is expected to revert if amount < shares
    function proveFail_redeemWithAmountLessThanShares(address msg_sender, address account, uint256 amount, uint256 shares, address receiver, address owner) public {
        require(msg_sender != address(this));
        require(receiver != address(this));
        require(amount < shares);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        try vault.redeem(shares, receiver, owner) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The mint function is expected to revert if msg.sender is this contract
    function proveFail_mintWithMSGSenderEqualsThis(uint256 shares, address receiver) public {
        // Setup
        require(receiver != address(0), "ERC4626: mint to the zero address");
        require(msg.sender == address(this), "msg.sender should be this contract");
        require(receiver != address(this), "receiver should not be this contract");
        require(shares > 0, "shares should be greater than zero");

        // Execution
        try vault.mint(receiver, shares) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The mint function is expected to revert if receiver is this contract
    function proveFail_mintWithReceiverAsThis(address msg_sender, address account, uint256 amount,uint256 shares, address receiver) public {
        require(msg_sender != address(this));
        require(receiver == address(this));
        require(amount >= shares);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        vm.prank(msg_sender);
        uint256 _receiverShares = vault.balanceOf(receiver);
        require(_receiverShares + shares <= vault.totalSupply());

        try vault.mint(shares, receiver) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The mint function is expected to revert if amount < shares
    function proveFail_mintWithAmountLessThanShares(address msg_sender, address account, uint256 amount,uint256 shares, address receiver) public {
        require(msg_sender != address(this));
        require(receiver != address(this));
        require(amount < shares);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        vm.prank(msg_sender);
        uint256 _receiverShares = vault.balanceOf(receiver);
        require(_receiverShares + shares <= vault.totalSupply());

        try vault.mint(shares, receiver) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The withdraw function is expected to revert if msg.sender is this contract
    function proveFail_withdrawWithMSGSenderEqualsThis(address msg_sender, address account, uint256 amount,uint256 assets, address receiver, address owner) public {
        require(msg_sender == address(this));
        require(receiver != address(this));
        require(msg_sender != owner);
        require(owner != address(this));
        require(owner != receiver);

        require(amount >= assets);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        uint256 _receiverAssets = asset.balanceOf(receiver);
        require(_receiverAssets + assets <= asset.totalSupply());
        vm.prank(msg_sender);
        try vault.withdraw(assets, receiver, owner) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The withdraw function is expected to revert if receiver is this contract
    function proveFail_withdrawWithReceiverEqualsThis(address msg_sender, address account, uint256 amount,uint256 assets, address receiver, address owner) public {
        require(msg_sender != address(this));
        require(receiver == address(this));
        require(msg_sender != owner);
        require(owner != address(this));
        require(owner != receiver);

        require(amount >= assets);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        uint256 _receiverAssets = asset.balanceOf(receiver);
        require(_receiverAssets + assets <= asset.totalSupply());
        vm.prank(msg_sender);
        try vault.withdraw(assets, receiver, owner) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The withdraw function is expected to revert if msg.sender == owner
    function proveFail_withdrawWithMSGSenderEqualsOwner(address msg_sender, address account, uint256 amount,uint256 assets, address receiver, address owner) public {
        require(msg_sender != address(this));
        require(receiver != address(this));
        require(msg_sender == owner);
        require(owner != address(this));
        require(owner != receiver);

        require(amount >= assets);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        uint256 _receiverAssets = asset.balanceOf(receiver);
        require(_receiverAssets + assets <= asset.totalSupply());
        vm.prank(msg_sender);
        try vault.withdraw(assets, receiver, owner) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The withdraw function is expected to revert if owner is this contract
    function proveFail_withdrawWithOwnerEqualsThis(address msg_sender, address account, uint256 amount,uint256 assets, address receiver, address owner) public {
        require(msg_sender != address(this));
        require(receiver != address(this));
        require(msg_sender != owner);
        require(owner == address(this));
        require(owner != receiver);

        require(amount >= assets);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        uint256 _receiverAssets = asset.balanceOf(receiver);
        require(_receiverAssets + assets <= asset.totalSupply());
        vm.prank(msg_sender);
        try vault.withdraw(assets, receiver, owner) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The withdraw function is expected to revert if owner == receiver
    function proveFail_withdrawWithOwnerEqualsReceiver(address msg_sender, address account, uint256 amount,uint256 assets, address receiver, address owner) public {
        require(msg_sender != address(this));
        require(receiver != address(this));
        require(msg_sender != owner);
        require(owner != address(this));
        require(owner == receiver);

        require(amount >= assets);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        uint256 _receiverAssets = asset.balanceOf(receiver);
        require(_receiverAssets + assets <= asset.totalSupply());
        vm.prank(msg_sender);
        try vault.withdraw(assets, receiver, owner) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The withdraw function is expected to revert if amount < assets
    function proveFail_withdrawWithAmountLessThanAssets(address msg_sender, address account, uint256 amount,uint256 assets, address receiver, address owner) public {
        require(msg_sender != address(this));
        require(receiver != address(this));
        require(msg_sender != owner);
        require(owner != address(this));
        require(owner == receiver);

        require(amount >= assets);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        uint256 _receiverAssets = asset.balanceOf(receiver);
        require(_receiverAssets + assets <= asset.totalSupply());
        vm.prank(msg_sender);
        try vault.withdraw(assets, receiver, owner) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }
    
    // The redeem function is expected to revert if msg.sender is this contract
    function proveFail_redeemWithMSGSenderEqualsThis(address msg_sender, address account, uint256 amount, uint256 shares, address receiver, address owner) public {
        require(msg_sender == address(this));
        require(receiver != address(this));
        require(amount >= shares);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        try vault.redeem(shares, receiver, owner) {
            assert(false);
        }
        catch {
            assert(true);
        }
    }

    // The redeem function is expected to revert if receiver is this contract
    function proveFail_redeemWithReceiverEqualsThis(address msg_sender, address account, uint256 amount, uint256 shares, address receiver, address owner) public {
        require(msg_sender != address(this));
        require(receiver == address(this));
        require(amount >= shares);

        vm.prank(msg_sender);
        vault.mint(amount, account);

        bool success;
        try vault.redeem(shares, receiver, owner) {
            success = true;
        }
        catch {
            success = false;
        }
        assert(!success);
    }
}