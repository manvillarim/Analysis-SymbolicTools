// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/halmos/subjects/ERC20_Solmate_Halmos.t.sol";

contract Confirm_ERC20_Solmate_Halmos is ERC20_Solmate_Halmos {
    function _slice(bytes memory b) internal pure returns (bytes memory r) {
        r = new bytes(32);
        for (uint256 i = 0; i < 32; i++) r[i] = b[4 + i];
    }

    function test_cex_0() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_ApproveFromZeroAddress(address,uint256)", address(uint160(730750818665451459101842416358141509827966271488)), uint256(115792089237316195423570985008687907853269984665640564039457584007913129639935)));
        if (ok) console2.log("OUTCOME", 0, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 0, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 0, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_1() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_ApproveToZeroAddress(address,uint256)", address(uint160(1160280361043977809595951758657988597271183780014)), uint256(115792089237316195423570985008687907853269984665640564039457584007913129639935)));
        if (ok) console2.log("OUTCOME", 1, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 1, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 1, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_2() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_ApproveZeroAddress(address,uint256)", address(uint160(0)), uint256(0)));
        if (ok) console2.log("OUTCOME", 2, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 2, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 2, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_3() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_ApproveZeroAddressForMSGSender(address,uint256)", address(uint160(730750818665451459101842416358141509827966271488)), uint256(0)));
        if (ok) console2.log("OUTCOME", 3, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 3, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 3, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_4() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_MintToZeroAddress(uint256)", uint256(115792089237316195423570985008687907853269984665640564039457584007913129639935)));
        if (ok) console2.log("OUTCOME", 4, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 4, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 4, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_5() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferFromToZeroAddress33(address,address,uint256)", address(uint160(728815563385977040452943777879061427756277306518)), address(uint160(1)), uint256(115792089237316195423570985008687907853269984665640564039457584007913129639935)));
        if (ok) console2.log("OUTCOME", 5, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 5, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 5, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_6() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferFromToZeroAddress33(address,address,uint256)", address(uint160(728815563385977040452943777879061427756277306518)), address(uint160(9223372036854775808)), uint256(43422033463993573283839119378257965444976244249615211514796594002967423614976)));
        if (ok) console2.log("OUTCOME", 6, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 6, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 6, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_7() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256)", address(uint160(1233701573041335019340183910623612409567528682678)), address(uint160(147020036636321914924508835156675110038584728450)), uint256(0)));
        if (ok) console2.log("OUTCOME", 7, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 7, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 7, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_8() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address)", address(uint160(1)), address(uint160(2))));
        if (ok) console2.log("OUTCOME", 8, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 8, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 8, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_9() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferToZeroAddress(address,uint256)", address(uint160(730750818665451459101842416358141509827966271488)), uint256(115792089237316195423570985008687907853269984665640564039457584007913129639935)));
        if (ok) console2.log("OUTCOME", 9, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 9, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 9, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_10() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_TransferZeroAmountToZeroAddressReverts(address)", address(uint160(1461501637330902908062480030890447807682306899967))));
        if (ok) console2.log("OUTCOME", 10, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 10, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 10, string.concat("revert:", vm.toString(ret)));
    }
}
