// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/hevm/subjects/ERC20_Solmate_Hevm.t.sol";

contract Confirm_ERC20_Solmate_Hevm is ERC20_Solmate_Hevm {
    function _slice(bytes memory b) internal pure returns (bytes memory r) {
        r = new bytes(32);
        for (uint256 i = 0; i < 32; i++) r[i] = b[4 + i];
    }

    function test_cex_0() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_ApproveFromZeroAddress(address,uint256)", address(uint160(26)), uint256(1)));
        if (ok) console2.log("OUTCOME", 0, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 0, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 0, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_1() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_ApproveToZeroAddress(address,uint256)", address(uint160(26)), uint256(1)));
        if (ok) console2.log("OUTCOME", 1, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 1, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 1, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_2() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_ApproveZeroAddressForMSGSender(address,uint256)", address(uint160(26)), uint256(0)));
        if (ok) console2.log("OUTCOME", 2, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 2, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 2, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_3() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_MintToZeroAddress(uint256)", uint256(1)));
        if (ok) console2.log("OUTCOME", 3, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 3, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 3, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_4() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferFromToZeroAddress33(address,address,uint256)", address(uint160(44203)), address(uint160(2877692075601769315584)), uint256(11692013098647223345629478661730264157247460343808)));
        if (ok) console2.log("OUTCOME", 4, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 4, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 4, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_5() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256)", address(uint160(348449143747323396190147844895929714868224)), address(uint160(70368744177664)), uint256(0)));
        if (ok) console2.log("OUTCOME", 5, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 5, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 5, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_6() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address)", address(uint160(175458095443608895223302532115927662592)), address(uint160(5316911983139663491615228241121379328))));
        if (ok) console2.log("OUTCOME", 6, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 6, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 6, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_7() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferToZeroAddress(address,uint256)", address(uint160(26)), uint256(1)));
        if (ok) console2.log("OUTCOME", 7, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 7, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 7, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_8() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferZeroAmountToZeroAddressReverts(address)", address(uint160(26))));
        if (ok) console2.log("OUTCOME", 8, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 8, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 8, string.concat("revert:", vm.toString(ret)));
    }
}
