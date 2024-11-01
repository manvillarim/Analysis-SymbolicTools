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
[PASS] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256) (paths: 7, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_Burn(uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_BurnReverts(uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256) (paths: 3, time: 0.01s, bounds: [])
Counterexample: 
    p_from_address_00 = 0x1804c8ab1f12e6bbf3894d4083f33e07309d1f38
    p_tokenId_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] prove_safeTransferFrom(address,uint256) (paths: 4, time: 0.12s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 3, time: 0.02s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
    p_sender_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] prove_setApprovalForAllReverts(address,address,bool) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFrom(address,address,uint256) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256) (paths: 5, time: 0.02s, bounds: [])
[PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
Symbolic test result: 12 passed; 2 failed; time: 0.74s
[PASS] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256) (paths: 7, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_Burn(uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_BurnReverts(uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256) (paths: 3, time: 0.01s, bounds: [])
Counterexample: 
    p_from_address_00 = 0x1804c8ab1f12e6bbf3894d4083f33e07309d1f38
    p_tokenId_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] prove_safeTransferFrom(address,uint256) (paths: 4, time: 0.10s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
    p_sender_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] prove_setApprovalForAllReverts(address,address,bool) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_transferFrom(address,address,uint256) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256) (paths: 2, time: 0.05s, bounds: [])
[PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256) (paths: 7, time: 0.08s, bounds: [])
[PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_Burn(uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_BurnReverts(uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256) (paths: 3, time: 0.01s, bounds: [])
Counterexample: 
    p_from_address_00 = 0x1804c8ab1f12e6bbf3894d4083f33e07309d1f38
    p_tokenId_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] prove_safeTransferFrom(address,uint256) (paths: 4, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
    p_sender_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] prove_setApprovalForAllReverts(address,address,bool) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_transferFrom(address,address,uint256) (paths: 7, time: 0.13s, bounds: [])
[PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256) (paths: 6, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256) (paths: 7, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_Burn(uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_BurnReverts(uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256) (paths: 3, time: 0.01s, bounds: [])
Counterexample: 
    p_from_address_00 = 0x1804c8ab1f12e6bbf3894d4083f33e07309d1f38
    p_tokenId_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] prove_safeTransferFrom(address,uint256) (paths: 4, time: 0.10s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
    p_sender_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] prove_setApprovalForAllReverts(address,address,bool) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFrom(address,address,uint256) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256) (paths: 7, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_Burn(uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_BurnReverts(uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256) (paths: 3, time: 0.01s, bounds: [])
Counterexample: 
    p_from_address_00 = 0x1804c8ab1f12e6bbf3894d4083f33e07309d1f38
    p_tokenId_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] prove_safeTransferFrom(address,uint256) (paths: 4, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 3, time: 0.02s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
    p_sender_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] prove_setApprovalForAllReverts(address,address,bool) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFrom(address,address,uint256) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256) (paths: 5, time: 0.02s, bounds: [])
[PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256) (paths: 7, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_Burn(uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_BurnReverts(uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256) (paths: 3, time: 0.01s, bounds: [])
Counterexample: 
    p_from_address_00 = 0x1804c8ab1f12e6bbf3894d4083f33e07309d1f38
    p_tokenId_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] prove_safeTransferFrom(address,uint256) (paths: 4, time: 0.10s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 3, time: 0.02s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
    p_sender_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] prove_setApprovalForAllReverts(address,address,bool) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFrom(address,address,uint256) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256) (paths: 5, time: 0.02s, bounds: [])
[PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256) (paths: 7, time: 0.08s, bounds: [])
[PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_Burn(uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_BurnReverts(uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256) (paths: 3, time: 0.01s, bounds: [])
Counterexample: 
    p_from_address_00 = 0x1804c8ab1f12e6bbf3894d4083f33e07309d1f38
    p_tokenId_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] prove_safeTransferFrom(address,uint256) (paths: 4, time: 0.11s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 3, time: 0.02s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
    p_sender_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] prove_setApprovalForAllReverts(address,address,bool) (paths: 5, time: 0.04s, bounds: [])
[PASS] prove_transferFrom(address,address,uint256) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256) (paths: 7, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_Burn(uint256) (paths: 1, time: 0.06s, bounds: [])
[PASS] prove_BurnReverts(uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256) (paths: 3, time: 0.01s, bounds: [])
Counterexample: 
    p_from_address_00 = 0x1804c8ab1f12e6bbf3894d4083f33e07309d1f38
    p_tokenId_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] prove_safeTransferFrom(address,uint256) (paths: 4, time: 0.10s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
    p_sender_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] prove_setApprovalForAllReverts(address,address,bool) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFrom(address,address,uint256) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256) (paths: 7, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_Burn(uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_BurnReverts(uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256) (paths: 3, time: 0.01s, bounds: [])
Counterexample: 
    p_from_address_00 = 0x1804c8ab1f12e6bbf3894d4083f33e07309d1f38
    p_tokenId_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] prove_safeTransferFrom(address,uint256) (paths: 4, time: 0.10s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 3, time: 0.02s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
    p_sender_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] prove_setApprovalForAllReverts(address,address,bool) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFrom(address,address,uint256) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
[PASS] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256) (paths: 2, time: 0.03s, bounds: [])
[PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256) (paths: 4, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256) (paths: 7, time: 0.07s, bounds: [])
[PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256) (paths: 2, time: 0.04s, bounds: [])
[PASS] prove_Burn(uint256) (paths: 1, time: 0.05s, bounds: [])
[PASS] prove_BurnReverts(uint256) (paths: 1, time: 0.01s, bounds: [])
[PASS] prove_Mint(address,uint256) (paths: 3, time: 0.04s, bounds: [])
[PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256) (paths: 3, time: 0.01s, bounds: [])
Counterexample: 
    p_from_address_00 = 0x1804c8ab1f12e6bbf3894d4083f33e07309d1f38
    p_tokenId_uint256_00 = 0x0000000000000000000000000000000000000000000000000000000000000000 (0)
[FAIL] prove_safeTransferFrom(address,uint256) (paths: 4, time: 0.10s, bounds: [])
[PASS] prove_setApprovalForAll(address,bool) (paths: 3, time: 0.03s, bounds: [])
Counterexample: 
    p_approved_bool_00 = false
    p_operator_address_00 = 0x0000000000000000000000000000000000000000
    p_sender_address_00 = 0x0000000000000000000000000000000000000000
[FAIL] prove_setApprovalForAllReverts(address,address,bool) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFrom(address,address,uint256) (paths: 7, time: 0.12s, bounds: [])
[PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256) (paths: 5, time: 0.03s, bounds: [])
[PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256) (paths: 6, time: 0.06s, bounds: [])
"""

markdown_result = process_terminal_output(terminal_output)
print(markdown_result)
