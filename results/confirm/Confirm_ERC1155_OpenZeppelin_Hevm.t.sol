// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

import "test/hevm/subjects/ERC1155_OpenZeppelin_Hevm.t.sol";

contract Confirm_ERC1155_OpenZeppelin_Hevm is ERC1155_OpenZeppelin_Hevm {
    function _slice(bytes memory b) internal pure returns (bytes memory r) {
        r = new bytes(32);
        for (uint256 i = 0; i < 32; i++) r[i] = b[4 + i];
    }

    function test_cex_0() public {
        vm.prank(0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38);
        (bool ok, bytes memory ret) = address(this).call(abi.encodeWithSignature("proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256)", uint256(7237005577332262213973186563042994240829374041602535252466099000494570602496), uint256(0)));
        if (ok) console2.log("OUTCOME", 0, "success");
        else if (ret.length >= 36 && bytes4(ret) == bytes4(0x4e487b71)) console2.log("OUTCOME", 0, string.concat("panic:", vm.toString(uint256(bytes32(_slice(ret))))));
        else console2.log("OUTCOME", 0, string.concat("revert:", vm.toString(ret)));
    }
}
