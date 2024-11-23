import re


def processar_tabelas(entrada):
    tabelas = entrada.split("FIM")
    hevm = tabelas[0].strip().split("\n")
    # kontrol = tabelas[1].strip().split("\n")
    halmos = tabelas[2].strip().split("\n")

    funcoes_status = {}

    # Processa a tabela hevm
    for linha in hevm:
        match = re.search(r"\|\s*(\w+)\s*\|\s*(PASS|FAIL)", linha)
        if match:
            funcao, status = match.groups()
            funcoes_status[funcao] = {"hevm": status, "kontrol": "N/A", "halmos": "N/A"}

    # Processa a tabela kontrol
    # for linha in kontrol:
    # match = re.search(r"\|\s*(\w+)\s*\|\s*(PASS|FAIL)", linha)
    # if match:
    #    funcao, status = match.groups()
    #   if funcao in funcoes_status:
    #      funcoes_status[funcao]["kontrol"] = status

    # Processa a tabela halmos
    for linha in halmos:
        match = re.search(r"\|\s*(\w+)\s*\|\s*(PASS|FAIL)", linha)
        if match:
            funcao, status = match.groups()
            if funcao in funcoes_status:
                funcoes_status[funcao]["halmos"] = status

    return funcoes_status


def gerar_tabela_markdown(funcoes_status):
    tabela_markdown = "| Função | HEVM Status | Kontrol Status | Halmos Status |\n"
    tabela_markdown += "|--------|-------------|----------------|---------------|\n"

    for funcao, status in funcoes_status.items():
        tabela_markdown += f"| {funcao} | {status['hevm']} | {status['kontrol']} | {status['halmos']} |\n"

    return tabela_markdown


# Exemplo de uso
entrada = """
| Função | Status |
|--------|--------|
| prove_safeTransferFrom | FAIL |
| prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender | PASS |
| proveFail_transferFromWhenFromIsNotTheOwner | FAIL |
| proveFail_ApproveWhenIdHasNotAnOwner | FAIL |
| prove_Burn | PASS |
| proveFail_ApproveWhenIsNotApprovedForAll | PASS |
| proveFail_setApprovalForAll | FAIL |
| prove_Mint | PASS |
| proveFail_transferFromWhenToIsAddressZero | PASS |
| proveFail_MintWhenToIsAddressZero | PASS |
| proveFail_Burn | PASS |
| prove_setApprovalForAll | PASS |
| prove_transferFrom | PASS |
| prove_ApproveWhenOwnerEqualsMSGSender | PASS |
FIM
FIM
| Function | Status | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Time 11 | Average (s) | Standard Deviation (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| proveFail_ApproveWhenIdHasNotAnOwner | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| proveFail_ApproveWhenIsNotApprovedForAll | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.08 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| proveFail_Burn | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| proveFail_MintWhenToIsAddressZero | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| proveFail_setApprovalForAllReverts | FAIL | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| proveFail_transferFromWhenFromIsNotTheOwner | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_transferFromWhenToIsAddressZero | PASS | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |
| prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.08 | 0.07 | 0.0 |
| prove_ApproveWhenOwnerEqualsMSGSender | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_Burn | PASS | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.0 |
| prove_Mint | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_safeTransferFrom | FAIL | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.0 |
| prove_setApprovalForAll | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| prove_transferFrom | PASS | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.0 |
FIM
"""

funcoes_status = processar_tabelas(entrada)
tabela_markdown = gerar_tabela_markdown(funcoes_status)
print(tabela_markdown)
