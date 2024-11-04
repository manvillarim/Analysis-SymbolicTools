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
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.37s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.91s

real    0m1,223s
user    0m1,326s
sys     0m0,132s
manoel@mirkwood-ii:~/hevm$ mkdir out
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠊] Compiling...
[⠢] Compiling 59 files with Solc 0.8.25
[⠔] Solc 0.8.25 finished in 4.11s
Compiler run successful!

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.37s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.91s

real    0m6,086s
user    0m5,859s
sys     0m0,356s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.37s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.10s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.91s

real    0m1,800s
user    0m1,985s
sys     0m0,319s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠢] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.38s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.92s

real    0m1,941s
user    0m2,035s
sys     0m0,313s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
^[[A[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 11, time: 1.57s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 2.12s

real    0m3,017s
user    0m6,321s
sys     0m0,348s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.37s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.10s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.92s

real    0m1,782s
user    0m1,974s
sys     0m0,288s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠢] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.37s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.91s

real    0m1,915s
user    0m1,985s
sys     0m0,352s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.37s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.90s

real    0m1,806s
user    0m2,007s
sys     0m0,306s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.39s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.92s

real    0m1,815s
user    0m1,991s
sys     0m0,292s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.07s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.37s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.91s

real    0m1,813s
user    0m1,999s
sys     0m0,303s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.07s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.38s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.91s

real    0m1,799s
user    0m1,976s
sys     0m0,275s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 7, time: 0.37s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 0.92s

real    0m1,820s
user    0m1,994s
sys     0m0,297s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_burnZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.06s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.02s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 1.40s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 13 passed; 1 failed; time: 1.94s
"""

markdown_result = process_terminal_output(terminal_output)
print(markdown_result)
