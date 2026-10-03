// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/halmos/subjects/ERC4626_OpenZeppelin_Halmos.t.sol";

contract Confirm_ERC4626_OpenZeppelin_Halmos is ERC4626_OpenZeppelin_Halmos {
    function _slice(bytes memory b) internal pure returns (bytes memory r) {
        r = new bytes(32);
        for (uint256 i = 0; i < 32; i++) r[i] = b[4 + i];
    }

    function test_cex_0() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_mintWithReceiverAsThis(address,address,uint256,uint256,address)", address(uint160(2)), address(uint160(1)), uint256(0), uint256(0), address(uint160(728815563385977040452943777879061427756277306518))));
        if (ok) console2.log("OUTCOME", 0, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 0, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 0, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_1() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_redeemWithMSGSenderEqualsThis(address,address,uint256,uint256,address,address)", address(uint160(728815563385977040452943777879061427756277306518)), address(uint160(952663243820296983343487351865964846429153394685)), uint256(0), uint256(0), address(uint160(508838219283308115488970380773768246779799535618)), address(uint160(728815563385977040452943777879061427756277306518))));
        if (ok) console2.log("OUTCOME", 1, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 1, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 1, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_2() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_redeemWithMSGSenderEqualsThis(address,address,uint256,uint256,address,address)", address(uint160(728815563385977040452943777879061427756277306518)), address(uint160(775609937646656434991963838905742918028373654307)), uint256(0), uint256(0), address(uint160(616575190297235952581039995430603336813107610644)), address(uint160(513809870187012055358204624502405599835466761350))));
        if (ok) console2.log("OUTCOME", 2, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 2, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 2, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_3() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_redeemWithReceiverEqualsThis(address,address,uint256,uint256,address,address)", address(uint160(2)), address(uint160(1)), uint256(0), uint256(0), address(uint160(728815563385977040452943777879061427756277306518)), address(uint160(728815563385977040452943777879061427756277306518))));
        if (ok) console2.log("OUTCOME", 3, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 3, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 3, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_4() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_redeemWithReceiverEqualsThis(address,address,uint256,uint256,address,address)", address(uint160(8)), address(uint160(2)), uint256(0), uint256(0), address(uint160(728815563385977040452943777879061427756277306518)), address(uint160(1))));
        if (ok) console2.log("OUTCOME", 4, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 4, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 4, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_5() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithAmountLessThanAssets(address,address,uint256,uint256,address,address)", address(uint160(2)), address(uint160(3)), uint256(0), uint256(0), address(uint160(1)), address(uint160(1))));
        if (ok) console2.log("OUTCOME", 5, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 5, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 5, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_6() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithMSGSenderEqualsOwner(address,address,uint256,uint256,address,address)", address(uint160(1)), address(uint160(3)), uint256(0), uint256(0), address(uint160(2)), address(uint160(1))));
        if (ok) console2.log("OUTCOME", 6, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 6, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 6, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_7() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithMSGSenderEqualsThis(address,address,uint256,uint256,address,address)", address(uint160(728815563385977040452943777879061427756277306518)), address(uint160(2)), uint256(0), uint256(0), address(uint160(1)), address(uint160(2535301200456458802993406410752))));
        if (ok) console2.log("OUTCOME", 7, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 7, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 7, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_8() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithOwnerEqualsReceiver(address,address,uint256,uint256,address,address)", address(uint160(2)), address(uint160(3)), uint256(0), uint256(0), address(uint160(1)), address(uint160(1))));
        if (ok) console2.log("OUTCOME", 8, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 8, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 8, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_9() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithOwnerEqualsThis(address,address,uint256,uint256,address,address)", address(uint160(1)), address(uint160(3)), uint256(0), uint256(0), address(uint160(2)), address(uint160(728815563385977040452943777879061427756277306518))));
        if (ok) console2.log("OUTCOME", 9, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 9, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 9, string.concat("revert:", vm.toString(ret)));
    }

    function test_cex_10() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_withdrawWithReceiverEqualsThis(address,address,uint256,uint256,address,address)", address(uint160(1)), address(uint160(3)), uint256(0), uint256(0), address(uint160(728815563385977040452943777879061427756277306518)), address(uint160(2))));
        if (ok) console2.log("OUTCOME", 10, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 10, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 10, string.concat("revert:", vm.toString(ret)));
    }
}
