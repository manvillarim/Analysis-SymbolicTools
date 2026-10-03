// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/hevm/subjects/ERC4626_Solmate_Hevm.t.sol";

contract Confirm_ERC4626_Solmate_Hevm is ERC4626_Solmate_Hevm {
    function _slice(bytes memory b) internal pure returns (bytes memory r) {
        r = new bytes(32);
        for (uint256 i = 0; i < 32; i++) r[i] = b[4 + i];
    }

    function test_cex_0() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_approvefrom_zero_address_reverts(address,uint256)", address(uint160(9903520314283042199192993804)), uint256(0)));
        if (ok) console2.log("OUTCOME", 0, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 0, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 0, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_1() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_approvezero_address_reverts(address,uint256)", address(uint160(9903520314283042199192993804)), uint256(0)));
        if (ok) console2.log("OUTCOME", 1, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 1, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 1, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_2() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_burn_from_zero_address_reverts(uint256)", uint256(0)));
        if (ok) console2.log("OUTCOME", 2, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 2, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 2, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_3() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_mintWithMSGSenderEqualsThis(uint256,address)", uint256(115792089237316195423570985008687907853269984665640564039457584007913129639935), address(uint160(16777216))));
        if (ok) console2.log("OUTCOME", 3, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 3, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 3, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_4() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_mint_to_zero_address_reverts(uint256)", uint256(0)));
        if (ok) console2.log("OUTCOME", 4, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 4, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 4, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_5() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_transferFrom_from_zero_address_reverts(address,address,uint256)", address(uint160(633825300114114700748351602692)), address(uint160(182687707388621800777412581967183397419871109386)), uint256(0)));
        if (ok) console2.log("OUTCOME", 5, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 5, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 5, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_6() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_transferFrom_to_zero_address_reverts(address,address,uint256)", address(uint160(22835965805554293464440283218188781636269637632)), address(uint160(87729534520060945902328115851620777994)), uint256(115792089237316195423570985008687907853269984665640564039457584007913129639935)));
        if (ok) console2.log("OUTCOME", 6, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 6, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 6, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_7() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_transfer_from_zero_address_reverts(address,uint256)", address(uint160(9903520314283042199192993804)), uint256(0)));
        if (ok) console2.log("OUTCOME", 7, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 7, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 7, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_8() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_transfer_to_zero_address_reverts(address,uint256)", address(uint160(696898287454081973172991196020261297061888)), uint256(0)));
        if (ok) console2.log("OUTCOME", 8, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 8, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 8, string.concat("revert:", vm.toString(ret)));
    }
}
