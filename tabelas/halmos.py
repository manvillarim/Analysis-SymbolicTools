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


terminal_output = """[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.12s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_burnZeroAddress(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.19s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 3.81s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.17s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 11 passed; 3 failed; time: 4.61s
Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.12s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_burnZeroAddress(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.18s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 3.78s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.17s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 11 passed; 3 failed; time: 4.58s

real    0m5,423s
user    0m8,639s
sys     0m0,371s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.12s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_burnZeroAddress(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.18s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 3.81s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.17s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 11 passed; 3 failed; time: 4.60s

real    0m5,442s
user    0m8,613s
sys     0m0,357s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.12s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_burnZeroAddress(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.18s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 3.79s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.17s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 11 passed; 3 failed; time: 4.59s

real    0m5,438s
user    0m8,701s
sys     0m0,337s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.12s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_burnZeroAddress(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.18s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 3.77s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.17s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 11 passed; 3 failed; time: 4.56s

real    0m5,407s
user    0m8,642s
sys     0m0,359s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.12s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_burnZeroAddress(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.19s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 3.79s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.17s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 11 passed; 3 failed; time: 4.59s

real    0m5,445s
user    0m8,670s
sys     0m0,364s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.12s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_burnZeroAddress(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.18s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 3.80s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.17s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 11 passed; 3 failed; time: 4.59s

real    0m5,437s
user    0m8,654s
sys     0m0,336s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.12s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_burnZeroAddress(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.18s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 3.83s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.18s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 11 passed; 3 failed; time: 4.63s

real    0m5,471s
user    0m8,674s
sys     0m0,380s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.12s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_burnZeroAddress(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.18s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 2, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 3.78s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.17s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 11 passed; 3 failed; time: 4.57s

real    0m5,432s
user    0m8,627s
sys     0m0,379s
manoel@mirkwood-ii:~/hevm$ time halmos --function prove --solver-timeout-assertion 10000000 --smt-exp-by-const 2
[⠒] Compiling...
No files changed, compilation skipped

Running 14 tests for test/halmos/ERC1155halmos.t.sol:ERC1155ymbolicProperties
[PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.12s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_burnZeroAddress(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_mintZeroAddress(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256) (paths: 3, time: 0.18s, bounds: [])
Counterexample: 
    p_amount_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
    p_id_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256) (paths: 1, time: 0.02s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256) (paths: 1, time: 0.01s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool) (paths: 4, time: 0.03s, bounds: [])
[PASS] prove_burn(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_mint(uint256,uint256) (paths: 1, time: 0.04s, bounds: [])
[PASS] prove_safeBatchTransferFrom(uint256,uint256[],uint256[]) (paths: 9, time: 3.90s, bounds: [ids=[0, 1, 2], values=[0, 1, 2]])
[PASS] prove_safeTransferFrom(uint256,uint256,uint256) (paths: 3, time: 0.18s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 5, time: 0.03s, bounds: [])
Symbolic test result: 11 passed; 3 failed; time: 4.70s
"""

markdown_result = process_terminal_output(terminal_output)
print(markdown_result)
