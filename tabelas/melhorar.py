import re
import pandas as pd
import statistics


def process_terminal_output(output):
    pass_pattern = re.compile(r"\[PASS\] (\w+)\(.*?\) \(paths: \d+, time: ([\d.]+)s")
    fail_pattern = re.compile(r"\[FAIL\] (\w+)\(.*?\) \(paths: \d+, time: ([\d.]+)s")

    function_times = {}

    for line in output.splitlines():
        pass_match = pass_pattern.search(line)
        fail_match = fail_pattern.search(line)

        if pass_match:
            func_name, time = pass_match.groups()
            time = float(time)
            if func_name not in function_times:
                function_times[func_name] = {"status": "PASS", "times": []}
            function_times[func_name]["times"].append(time)
        elif fail_match:
            func_name, time = fail_match.groups()
            time = float(time)
            if func_name not in function_times:
                function_times[func_name] = {"status": "FAIL", "times": []}
            function_times[func_name]["times"].append(time)
            function_times[func_name]["status"] = "FAIL"

    rows = []
    max_num_times = max(len(data["times"]) for data in function_times.values())

    for func_name, data in function_times.items():
        times = data["times"]
        mean_time = round(statistics.mean(times), 2)
        std_time = round(statistics.stdev(times), 2) if len(times) > 1 else 0

        row = (
            [func_name, data["status"]]
            + times
            + [""] * (max_num_times - len(times))
            + [mean_time, std_time]
        )
        rows.append(row)

    columns = (
        ["Função", "Status"]
        + [f"Tempo {i+1}" for i in range(max_num_times)]
        + ["Média (s)", "Desvio Padrão (s)"]
    )

    df = pd.DataFrame(rows, columns=columns)

    total_tests = sum(len(data["times"]) for data in function_times.values())
    total_passed = sum(
        len(data["times"])
        for data in function_times.values()
        if data["status"] == "PASS"
    )

    markdown_table = "| " + " | ".join(df.columns) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(df.columns)) + " |\n"
    for _, row in df.iterrows():
        markdown_table += (
            "| "
            + " | ".join([str(cell) if cell != "" else "-" for cell in row])
            + " |\n"
        )

    markdown_table += f"\n**Total de Testes Feitos:** {total_tests}\n"
    markdown_table += f"**Total de Testes Passados:** {total_passed}\n"

    return markdown_table


terminal_output = """
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 5, time: 0.06s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 15, time: 0.20s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0000000000000000000000000000000000000002
Counterexample: 
    p_amount_uint256 = 0xb87c44c08000102010b3bfbf80008f98c001b1ffff0000000000000000000000 (83445127683894876214681179471890527537723466594599135206640548101483254513664)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0010000000000000000000040000002000000011
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 8, time: 0.17s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 10, time: 0.09s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address = 0xa000000000000000000000000000000000000000
    p_sender_address = 0x6000000000000000000000000000000000000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.21s, bounds: [])
Counterexample: 
    p_spender_address = 0x0000000000000000000000000000000000000001
    p_tokenSender_address = 0x0000000000000000000000000000000000000010
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.10s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.06s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.12s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.11s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.08s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.07s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.21s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.25s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.27s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.21s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.14s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.16s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.18s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.13s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 7, time: 0.19s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 7, time: 0.17s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.16s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 4, time: 0.16s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.21s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.17s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.08s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])
Symbolic test result: 51 passed; 10 failed; time: 5.90s

real    0m10,394s
user    0m10,480s
sys     0m0,427s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 100000 --smt-exp-by-const 2
[⠢] Compiling...
No files changed, compilation skipped

Running 61 tests for test/ERC20halmos.t.sol:ERC20SymbolicProperties
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.04s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 15, time: 0.24s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0000000000000000000000000000000000000002
Counterexample: 
    p_amount_uint256 = 0xb87c44c08000102010b3bfbf80008f98c001b1ffff0000000000000000000000 (83445127683894876214681179471890527537723466594599135206640548101483254513664)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0010000000000000000000040000002000000011
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 8, time: 0.18s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 10, time: 0.09s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address = 0xa000000000000000000000000000000000000000
    p_sender_address = 0x6000000000000000000000000000000000000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.22s, bounds: [])
Counterexample: 
    p_spender_address = 0x0000000000000000000000000000000000000001
    p_tokenSender_address = 0x0000000000000000000000000000000000000010
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.10s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.07s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.11s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.11s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.08s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.07s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.19s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.24s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.25s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.20s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.14s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.16s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.11s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.18s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.12s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 7, time: 0.18s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 7, time: 0.16s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.15s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 4, time: 0.14s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.21s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.19s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.09s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])
Symbolic test result: 51 passed; 10 failed; time: 5.89s
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 5, time: 0.06s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.03s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 15, time: 0.24s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0000000000000000000000000000000000000002
Counterexample: 
    p_amount_uint256 = 0xb87c44c08000102010b3bfbf80008f98c001b1ffff0000000000000000000000 (83445127683894876214681179471890527537723466594599135206640548101483254513664)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0010000000000000000000040000002000000011
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 8, time: 0.19s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 9, time: 0.09s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address = 0xa000000000000000000000000000000000000000
    p_sender_address = 0x6000000000000000000000000000000000000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.21s, bounds: [])
Counterexample: 
    p_spender_address = 0x0000000000000000000000000000000000000001
    p_tokenSender_address = 0x0000000000000000000000000000000000000010
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.10s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.04s, bounds: [])
Counterexample: 
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.07s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.06s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.05s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.12s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.12s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.06s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.09s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.07s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.14s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.30s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.25s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.20s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.14s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.16s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.11s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.18s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.12s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 7, time: 0.18s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 7, time: 0.16s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.15s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 4, time: 0.15s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.21s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.17s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.08s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])
Symbolic test result: 51 passed; 10 failed; time: 5.95s
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.04s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 3, time: 0.02s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.03s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 15, time: 0.20s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0000000000000000000000000000000000000002
Counterexample: 
    p_amount_uint256 = 0xb87c44c08000102010b3bfbf80008f98c001b1ffff0000000000000000000000 (83445127683894876214681179471890527537723466594599135206640548101483254513664)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0010000000000000000000040000002000000011
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 8, time: 0.17s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 9, time: 0.08s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address = 0xa000000000000000000000000000000000000000
    p_sender_address = 0x6000000000000000000000000000000000000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.21s, bounds: [])
Counterexample: 
    p_spender_address = 0x0000000000000000000000000000000000000001
    p_tokenSender_address = 0x0000000000000000000000000000000000000010
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.10s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.06s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.12s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.12s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.08s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.07s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.14s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.31s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.25s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.20s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.14s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.17s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.11s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.17s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.13s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 7, time: 0.19s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 7, time: 0.18s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.16s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 4, time: 0.15s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.21s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.18s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.08s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])
Symbolic test result: 51 passed; 10 failed; time: 5.87s
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.04s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 5, time: 0.06s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 15, time: 0.21s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0000000000000000000000000000000000000002
Counterexample: 
    p_amount_uint256 = 0xb87c44c08000102010b3bfbf80008f98c001b1ffff0000000000000000000000 (83445127683894876214681179471890527537723466594599135206640548101483254513664)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0010000000000000000000040000002000000011
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 8, time: 0.18s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 10, time: 0.09s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.07s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address = 0xa000000000000000000000000000000000000000
    p_sender_address = 0x6000000000000000000000000000000000000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.22s, bounds: [])
Counterexample: 
    p_spender_address = 0x0000000000000000000000000000000000000001
    p_tokenSender_address = 0x0000000000000000000000000000000000000010
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.10s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.07s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.11s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.11s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.06s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.08s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.08s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.15s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.08s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.32s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.26s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.23s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.15s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.17s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.11s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.17s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.13s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 7, time: 0.19s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 7, time: 0.18s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.16s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 4, time: 0.14s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.21s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.18s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.09s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])
Symbolic test result: 51 passed; 10 failed; time: 6.03s
Running 61 tests for test/ERC20halmos.t.sol:ERC20SymbolicProperties
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 5, time: 0.06s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 15, time: 0.26s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0000000000000000000000000000000000000002
Counterexample: 
    p_amount_uint256 = 0xb87c44c08000102010b3bfbf80008f98c001b1ffff0000000000000000000000 (83445127683894876214681179471890527537723466594599135206640548101483254513664)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0010000000000000000000040000002000000011
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 9, time: 0.22s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 11, time: 0.10s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.07s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.05s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address = 0xa000000000000000000000000000000000000000
    p_sender_address = 0x6000000000000000000000000000000000000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.23s, bounds: [])
Counterexample: 
    p_spender_address = 0x0000000000000000000000000000000000000001
    p_tokenSender_address = 0x0000000000000000000000000000000000000010
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.11s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.04s, bounds: [])
Counterexample: 
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.07s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.05s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.13s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.13s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.08s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.09s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.17s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.39s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.26s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.21s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.15s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.18s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.18s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.14s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 7, time: 0.20s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 7, time: 0.17s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.16s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 4, time: 0.15s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.19s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.17s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.09s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])
Symbolic test result: 51 passed; 10 failed; time: 6.39s
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.04s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 5, time: 0.06s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 15, time: 0.20s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0000000000000000000000000000000000000002
Counterexample: 
    p_amount_uint256 = 0xb87c44c08000102010b3bfbf80008f98c001b1ffff0000000000000000000000 (83445127683894876214681179471890527537723466594599135206640548101483254513664)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0010000000000000000000040000002000000011
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 8, time: 0.17s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 11, time: 0.10s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address = 0xa000000000000000000000000000000000000000
    p_sender_address = 0x6000000000000000000000000000000000000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.22s, bounds: [])
Counterexample: 
    p_spender_address = 0x0000000000000000000000000000000000000001
    p_tokenSender_address = 0x0000000000000000000000000000000000000010
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.10s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.07s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.12s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.11s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.08s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.07s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.21s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.25s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.26s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.20s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.14s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.16s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.11s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.17s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.12s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 7, time: 0.18s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 6, time: 0.16s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.15s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 4, time: 0.15s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.20s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.18s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.08s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])
Symbolic test result: 51 passed; 10 failed; time: 5.85s
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 15, time: 0.20s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0000000000000000000000000000000000000002
Counterexample: 
    p_amount_uint256 = 0xb87c44c08000102010b3bfbf80008f98c001b1ffff0000000000000000000000 (83445127683894876214681179471890527537723466594599135206640548101483254513664)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0010000000000000000000040000002000000011
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 8, time: 0.18s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 10, time: 0.09s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address = 0xa000000000000000000000000000000000000000
    p_sender_address = 0x6000000000000000000000000000000000000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.22s, bounds: [])
Counterexample: 
    p_spender_address = 0x0000000000000000000000000000000000000001
    p_tokenSender_address = 0x0000000000000000000000000000000000000010
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.10s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.06s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.05s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.12s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.11s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.08s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.08s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.20s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.24s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.25s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.20s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.14s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.17s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.11s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.18s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.12s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 7, time: 0.19s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 7, time: 0.16s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.15s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 4, time: 0.14s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.20s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.18s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.09s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])
Symbolic test result: 51 passed; 10 failed; time: 5.90s
Running 61 tests for test/ERC20halmos.t.sol:ERC20SymbolicProperties
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 15, time: 0.21s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0000000000000000000000000000000000000002
Counterexample: 
    p_amount_uint256 = 0xb87c44c08000102010b3bfbf80008f98c001b1ffff0000000000000000000000 (83445127683894876214681179471890527537723466594599135206640548101483254513664)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0010000000000000000000040000002000000011
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 8, time: 0.17s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 11, time: 0.10s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address = 0xa000000000000000000000000000000000000000
    p_sender_address = 0x6000000000000000000000000000000000000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.22s, bounds: [])
Counterexample: 
    p_spender_address = 0x0000000000000000000000000000000000000001
    p_tokenSender_address = 0x0000000000000000000000000000000000000010
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.10s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.07s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.12s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.12s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.06s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.08s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.07s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.15s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.31s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.26s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.21s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.14s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.17s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.11s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.18s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.14s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 7, time: 0.21s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 7, time: 0.17s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.16s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 4, time: 0.16s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.20s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.18s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.09s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])
Symbolic test result: 51 passed; 10 failed; time: 6.03s
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveFromZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveToZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_ApproveZeroAddress(uint256) (paths: 1, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_spender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] proveFail_BurnFromZeroAddress(uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_BurnUnderBalance(address,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] proveFail_BurnUnderSupply(address,uint256) (paths: 4, time: 0.03s, bounds: [])
[PASS] proveFail_MintOverflow(address) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
[FAIL] proveFail_MintToZeroAddress(uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256) (paths: 15, time: 0.20s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0000000000000000000000000000000000000002
Counterexample: 
    p_amount_uint256 = 0xb87c44c08000102010b3bfbf80008f98c001b1ffff0000000000000000000000 (83445127683894876214681179471890527537723466594599135206640548101483254513664)
    p_owner_address = 0x00000000000000000000000000000000aaaa0001
    p_spender_address = 0x0010000000000000000000040000002000000011
[FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256) (paths: 8, time: 0.17s, bounds: [])
[PASS] proveFail_TransferFromUnderBalance(address,address,uint256) (paths: 10, time: 0.09s, bounds: [])
[PASS] proveFail_TransferFromUnderBalancei(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,address,uint256) (paths: 6, time: 0.04s, bounds: [])
[PASS] proveFail_TransferFromZeroAddress(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_recipient_address = 0xa000000000000000000000000000000000000000
    p_sender_address = 0x6000000000000000000000000000000000000000
[FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (paths: 6, time: 0.21s, bounds: [])
Counterexample: 
    p_spender_address = 0x0000000000000000000000000000000000000001
    p_tokenSender_address = 0x0000000000000000000000000000000000000010
[FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (paths: 7, time: 0.10s, bounds: [])
Counterexample: 
    p_amount_uint256 = 0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff (115792089237316195423570985008687907853269984665640564039457584007913129639935)
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferToZeroAddress(address,uint256) (paths: 4, time: 0.06s, bounds: [])
[PASS] proveFail_TransferUnderBalance(address,uint256) (paths: 5, time: 0.04s, bounds: [])
[PASS] proveFail_TransferUnderBalancej(address,uint256) (paths: 4, time: 0.03s, bounds: [])
Counterexample: 
    p_sender_address = 0x8000000000000000000000000000000000000000
[FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.07s, bounds: [])
[PASS] prove_Approve(address,uint256) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ApproveMaxAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_ApproveNonZeroAmount(address,address,uint256) (paths: 6, time: 0.05s, bounds: [])
[PASS] prove_ApproveZeroAmount(address,address) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256) (paths: 8, time: 0.12s, bounds: [])
[PASS] prove_BurnDifferentAccount(address,uint256,address,uint256) (paths: 8, time: 0.11s, bounds: [])
[PASS] prove_BurnFromNonZeroAddress(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_BurnSameAccount(address,uint256) (paths: 3, time: 0.06s, bounds: [])
[PASS] prove_BurnZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256) (paths: 5, time: 0.05s, bounds: [])
[PASS] prove_DecreaseAllowance(address,uint256) (paths: 4, time: 0.08s, bounds: [])
[PASS] prove_IncreaseAllowance(address,uint256) (paths: 3, time: 0.07s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.05s, bounds: [])
[PASS] prove_MintZeroTokens(address) (paths: 3, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256) (paths: 9, time: 0.19s, bounds: [])
[PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256) (paths: 18, time: 0.24s, bounds: [])
[PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8) (paths: 14, time: 0.25s, bounds: [])
[PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256) (paths: 12, time: 0.20s, bounds: [])
[PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8) (paths: 11, time: 0.14s, bounds: [])
WARNING:halmos:prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8): paths have not been fully explored due to the loop unrolling bound: 2
(see https://github.com/a16z/halmos/wiki/warnings#loop-bound)
[PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256) (paths: 11, time: 0.16s, bounds: [])
[PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_SelfApprovePositiveAmount(address,uint256) (paths: 4, time: 0.04s, bounds: [])
[PASS] prove_SelfApproveZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256) (paths: 4, time: 0.05s, bounds: [])
[PASS] prove_SelfTransferZeroAmountAllowed(address) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256) (paths: 11, time: 0.17s, bounds: [])
[PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address) (paths: 11, time: 0.13s, bounds: [])
[PASS] prove_Transfer(address,uint256,uint256) (paths: 7, time: 0.18s, bounds: [])
[PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256) (paths: 7, time: 0.17s, bounds: [])
[PASS] prove_TransferFrom(address,address,uint256,uint256) (paths: 7, time: 0.17s, bounds: [])
[PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256) (paths: 4, time: 0.15s, bounds: [])
[PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256) (paths: 20, time: 0.21s, bounds: [])
[PASS] prove_TransferFromNoFees(address,address,address,uint256) (paths: 13, time: 0.17s, bounds: [])
[PASS] prove_TransferFromZeroAmount(address,address,address) (paths: 8, time: 0.08s, bounds: [])
[PASS] prove_TransferZeroAmount(address,address) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ZeroAddressHasNoToken() (paths: 1, time: 0.01s, bounds: [])
Symbolic test result: 51 passed; 10 failed; time: 5.86s
"""

markdown_result = process_terminal_output(terminal_output)
print(markdown_result)
