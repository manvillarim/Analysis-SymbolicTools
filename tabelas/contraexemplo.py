import re


def extract_failures_and_counterexamples(text):
    failures = []
    counterexample = None

    lines = text.split("\n")
    for line in lines:
        fail_match = re.match(r"\[FAIL\] (\w+)", line)
        counter_match = re.match(r"Counterexample:", line)

        if fail_match:
            failure_name = fail_match.group(1)
            counterexample = ""
        elif counter_match:
            counterexample = ""
        elif counterexample is not None:
            if line.strip():
                counterexample += line.strip() + " "
            else:
                failures.append((failure_name, counterexample.strip()))
                counterexample = None

    if counterexample:
        failures.append((failure_name, counterexample.strip()))

    return failures


def generate_markdown_table(failures):
    markdown = "| Function Name | Counterexample |\n"
    markdown += "|--------------|---------------|\n"
    for failure, counterexample in failures:
        markdown += f"| {failure} | {counterexample} |\n"
    return markdown


text = """Counterexample: 
    p_amount_uint256_00 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address_00 = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address_00 = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.04s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.02s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address_00 = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.02s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 2, time: 0.01s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 4, time: 0.03s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.03s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.02s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 16, time: 0.37s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0100000000038000440108020000004000000000000000000000000000000000 (452312848584706206528434140988820484163156322014720363298890076337114972160)
    p_owner_address_00 = 0x7fa9385be102ac3eac297483dd6233d62b3e1496
    p_spender_address_00 = 0x0000000000000000000000000000008000000000
Counterexample: 
    p_amount_uint256_00 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address_00 = 0x7fa9385be102ac3eac297483dd6233d62b3e1496
    p_spender_address_00 = 0x0000001000000000000000000000000000000000
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 11, time: 0.15s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 11, time: 0.08s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.02s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address_00 = 0x0000000000000000000000000000000040000000
    p_sender_address_00 = 0x0000000000000000000000000000000040000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
Counterexample: 
    p_spender_address_00 = 0x0000000000000000000000000000000000000040
    p_tokenSender_address_00 = 0x0000000000000000000000000000000000000020
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.08s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x810102852054040210480000281024080003ea00002300200000d40000000001 (58350141706876298166454238418836993676218598869373590084719947305071281176577)
    p_sender_address_00 = 0x0000000000000000000008000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 5, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.02s, bounds: [])
Counterexample: 
    p_sender_address_00 = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.05s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.02s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.03s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.10s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.16s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.11s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.06s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.32s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.21s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.29s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.12s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.16s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.10s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.02s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.15s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.12s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 8, time: 0.17s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 9, time: 0.30s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.15s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 5, time: 0.18s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.27s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.19s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.07s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.06s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])"""
failures = extract_failures_and_counterexamples(text)
markdown_table = generate_markdown_table(failures)
print(markdown_table)
