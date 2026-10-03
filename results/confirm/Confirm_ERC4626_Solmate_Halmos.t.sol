// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/halmos/subjects/ERC4626_Solmate_Halmos.t.sol";

contract Confirm_ERC4626_Solmate_Halmos is ERC4626_Solmate_Halmos {
    function _slice(bytes memory b) internal pure returns (bytes memory r) {
        r = new bytes(32);
        for (uint256 i = 0; i < 32; i++) r[i] = b[4 + i];
    }

    function test_cex_0() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_approvefrom_zero_address_reverts(address,uint256)", address(uint160(730750818665451459101842416358141509827966271488)), uint256(0)));
        if (ok) console2.log("OUTCOME", 0, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 0, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 0, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_1() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_approvezero_address_reverts(address,uint256)", address(uint160(1159602743760608647600499099441526091252210873429)), uint256(0)));
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
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_mintWithReceiverAsThis(address,address,uint256,uint256,address)", address(uint160(1)), address(uint160(0)), uint256(0), uint256(0), address(uint160(728815563385977040452943777879061427756277306518))));
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
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_transferFrom_from_zero_address_reverts(address,address,uint256)", address(uint160(154212696630166877417522988827951551195941085333)), address(uint160(0)), uint256(0)));
        if (ok) console2.log("OUTCOME", 5, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 5, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 5, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_6() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_transferFrom_to_zero_address_reverts(address,address,uint256)", address(uint160(730750818665451459101842416358141509827966271488)), address(uint160(730750818665451459101842416358141509827966271488)), uint256(0)));
        if (ok) console2.log("OUTCOME", 6, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 6, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 6, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_7() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_transferFrom_to_zero_address_reverts(address,address,uint256)", address(uint160(730750818665451459101842416358141509827966271488)), address(uint160(730750818665451459101842416358141509827966271488)), uint256(115792089237316195423570985008687907853269984665640564039457584007913129639935)));
        if (ok) console2.log("OUTCOME", 7, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 7, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 7, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_8() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_transfer_from_zero_address_reverts(address,uint256)", address(uint160(730750818665451459101842416358141509827966271488)), uint256(0)));
        if (ok) console2.log("OUTCOME", 8, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 8, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 8, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_9() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_transfer_to_zero_address_reverts(address,uint256)", address(uint160(85070591730234615865843651857942052864)), uint256(0)));
        if (ok) console2.log("OUTCOME", 9, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 9, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 9, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_10() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithAmountLessThanAssets(address,address,uint256,uint256,address,address)", address(uint160(1)), address(uint160(2)), uint256(0), uint256(0), address(uint160(0)), address(uint160(0))));
        if (ok) console2.log("OUTCOME", 10, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 10, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 10, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_11() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithMSGSenderEqualsOwner(address,address,uint256,uint256,address,address)", address(uint160(0)), address(uint160(2)), uint256(0), uint256(0), address(uint160(1)), address(uint160(0))));
        if (ok) console2.log("OUTCOME", 11, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 11, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 11, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_12() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithMSGSenderEqualsThis(address,address,uint256,uint256,address,address)", address(uint160(728815563385977040452943777879061427756277306518)), address(uint160(618970019642690137449562112)), uint256(0), uint256(0), address(uint160(1)), address(uint160(0))));
        if (ok) console2.log("OUTCOME", 12, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 12, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 12, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_13() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithOwnerEqualsReceiver(address,address,uint256,uint256,address,address)", address(uint160(1)), address(uint160(2)), uint256(0), uint256(0), address(uint160(0)), address(uint160(0))));
        if (ok) console2.log("OUTCOME", 13, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 13, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 13, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_14() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithOwnerEqualsThis(address,address,uint256,uint256,address,address)", address(uint160(0)), address(uint160(2361183241434822606848)), uint256(0), uint256(0), address(uint160(1)), address(uint160(728815563385977040452943777879061427756277306518))));
        if (ok) console2.log("OUTCOME", 14, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 14, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 14, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_15() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithReceiverEqualsThis(address,address,uint256,uint256,address,address)", address(uint160(713623846352979940529142984724747568191373312)), address(uint160(140737488355328)), uint256(0), uint256(0), address(uint160(728815563385977040452943777879061427756277306518)), address(uint160(0))));
        if (ok) console2.log("OUTCOME", 15, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 15, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 15, string.concat("revert:", vm.toString(ret)));
    }
}
