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
    
    function onERC1155Received() public pure returns(bytes4) {
        // Just to enable safe functions
        return this.onERC1155Received.selector;
    }

    function onERC1155BatchReceived() public pure returns (bytes4) {
        // Just to enable safe functions
        return this.onERC1155BatchReceived.selector;
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

    // prove_setApprovalForAll: Sets approval for operator to manage caller's tokens. Reverts if operator is caller.    
    function prove_setApprovalForAll(address operator, bool approved) public {
        require(msg.sender != operator && operator != address(0));
        vm.prank(msg.sender);
        try token.setApprovalForAll(operator, approved) {} catch{assert(false);}
        assert(token.isApprovedForAll(msg.sender, operator)==approved);
    }

    // prove_safeTransferFrom: Transfers token from one account to another if conditions like approval and balances are met. Reverts otherwise.
    function prove_safeTransferFrom(uint256 id, uint256 initAmount, uint256 amount) public { // Not OK
        bytes memory data = new bytes(3);
        try token.mint(address(from), id, initAmount, data) {} catch {assert(false);}
        uint256 _balanceIdFrom = token.balanceOf(address(from), id);
        uint256 _balanceIdTo = token.balanceOf(address(to), id);
        require(_balanceIdFrom >= amount);
        vm.prank(address(from));
        try token.safeTransferFrom(address(from), address(to), id, amount, data) {} catch {assert(false);}
        assert(token.balanceOf(address(from), id) == _balanceIdFrom - amount);
        assert(token.balanceOf(address(to), id) == _balanceIdTo + amount);
    }

    // prove_safeBatchTransferFrom: Transfers token from one account to another if conditions like approval and balances are met. Reverts otherwise.
    function prove_safeBatchTransferFrom(uint256 initAmount, uint256[] memory ids, uint256[] memory values) public { // Require additional timeout
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
        try token.safeBatchTransferFrom(address(from), address(to), ids, values, data) {} catch {assert(false);}
        for(uint8 i=0; i<ids.length; i++) {
            assert(token.balanceOf(address(from), ids[i]) == _balanceIdFrom[i] - values[i]);
            assert(token.balanceOf(address(to), ids[i]) == _balanceIdTo[i] + values[i]);
        }
    }

    // prove_mint: Mints new tokens for an account. Reverts if account is zero address.
    function prove_mint(uint256 id, uint256 amount) public {
        bytes memory data;
        uint256 _balanceAcc = token.balanceOf(address(from), id);
        try token.mint(address(from), id, amount, data) {} catch{assert(false);}
        assert(token.balanceOf(address(from), id) == _balanceAcc + amount);
    }

    // prove_burn: Burns tokens of an account if balance allows. Reverts if account is zero address or balance less than amount.
    function prove_burn(uint256 id, uint256 amount) public {
        bytes memory data;
        try token.mint(address(from), id, amount, data) {} catch{assert(false);}
        uint256 _balanceAcc = token.balanceOf(address(from), id);
        try token.burn(address(from), id, amount) {} catch {assert(false);}
        assert(token.balanceOf(address(from), id) == _balanceAcc - amount);
    }

// ********************************* Revertable properties **************************************

    // proveFail_setApprovalForAllSenderEqualsOperator: Negated case of setApprovalForAll. Expects revert if operator is caller.
    function proveFail_setApprovalForAllSenderEqualsOperator(address operator, bool approved) public {
        require(operator == address(0));
        vm.prank(msg.sender);
        try token.setApprovalForAll(operator, approved) {assert(false);} catch {assert(true);}
    }

    // proveFail_safeTransferFromWhenSenderIsNotMSGSender: Negated case of safeTransferFrom. Expects revert when sende is not msg.sender.
    function proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256 id, uint256 amount) public {
        bytes memory data;
        vm.prank(msg.sender);
        try token.safeTransferFrom(address(from), address(to), id, amount, data) {assert(false);} catch {assert(true);}
    }

    // proveFail_safeTransferFromWhenSenderIsNotMSGSender: Negated case of safeTransferFrom. Expects revert when sende is not msg.sender.
    function proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256 id, uint256 amount) public {
        vm.prank(address(from));
        token.setApprovalForAll(address(from), true);
        bytes memory data;
        vm.prank(address(from));
        try token.safeTransferFrom(address(from), address(to), id, amount, data) {assert(false);} catch {assert(true);}
    }

    // proveFail_safeTransferFromZeroAddressForFrom: Negated case of safeTransferFrom. Expects revert when from is the zero address.
    function proveFail_safeTransferFromZeroAddressForFrom(uint256 id, uint256 amount) public {
        bytes memory data;
        vm.prank(address(from));
        try token.safeTransferFrom(address(from), address(0), id, amount, data) {assert(false);} catch {assert(true);}
    }

    // proveFail_safeTransferFromZeroAddressForTo: Negated case of safeTransferFrom. Expects revert when to is the zero address.
    function proveFail_safeTransferFromZeroAddressForTo(uint256 id, uint256 amount) public {
        bytes memory data;
        try token.safeTransferFrom(address(0), address(to), id, amount, data) {assert(false);} catch {assert(true);}
    }

    // proveFail_safeTransferFromBalanceLessThanAmount: Negated case of safeTransferFrom. Expects revert if balance less than transfer amount.
    function proveFail_safeTransferFromBalanceLessThanAmount(uint256 id, uint256 initAmount, uint256 amount) public {
        vm.prank(msg.sender);
        bytes memory data;
        try token.mint(address(from), id, initAmount, data) {} catch{assert(false);}
        uint256 _balanceIdFrom = token.balanceOf(address(from), id);
        require(_balanceIdFrom < amount);
        vm.prank(address(from));
        try token.safeTransferFrom(address(from), address(to), id, amount, data) {assert(false);} catch {assert(true);}
    }

    // proveFail_mintZeroAddress: Negated case of mint. Expects revert for zero address.
    function proveFail_mintZeroAddress(uint256 id, uint256 amount) public {
        bytes memory data;
        try token.mint(address(0), id, amount, data) {assert(false);} catch {assert(true);}
    }

    // proveFail_burnZeroAddress: Negated case of burn. Expects revert for zero address.
    function proveFail_burnZeroAddress(uint256 id, uint256 amount) public {
        try token.burn(address(0), id, amount) {assert(false);} catch {assert(true);}
    }

    // proveFail_burnBalanceLessThanAmount: Negated case of burn. Expects revert if balance less than burn amount.
    function proveFail_burnBalanceLessThanAmount(uint256 id, uint256 initAmount, uint256 amount) public {
        bytes memory data;
        try token.mint(address(from), id, initAmount, data) {} catch{assert(false);}
        uint256 balanceAcc = token.balanceOf(address(from), id);
        require(balanceAcc < amount);
        try token.burn(address(from), id, amount) {assert(false);} catch {assert(true);}
    }

}