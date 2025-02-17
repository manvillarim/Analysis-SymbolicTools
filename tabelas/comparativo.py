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
| Function | Status |
|--------|--------|
| proveFail_burnZeroAddress | FAIL |
| proveFail_setApprovalForAllSenderEqualsOperator | FAIL |
| proveFail_mintZeroAddress | PASS |
| proveFail_burnBalanceLessThanAmount | PASS |
| proveFail_safeTransferFromWhenSenderIsNotMSGSender | FAIL |
| prove_mint | PASS |
| proveFail_safeTransferFromWhenSenderIsNotApprovedForAll | PASS |
| prove_safeBatchTransferFrom | ERROR |
| prove_safeTransferFrom | PASS |
| prove_burn | PASS |
| proveFail_safeTransferFromBalanceLessThanAmount | PASS |
| proveFail_safeTransferFromZeroAddressForTo | PASS |
| prove_setApprovalForAll | PASS |
| proveFail_safeTransferFromZeroAddressForFrom | PASS |
FIM
FIM
| Function | Status | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Average (s) | Standard Deviation (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| proveFail_burnBalanceLessThanAmount | PASS | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.0 |
| proveFail_burnZeroAddress | FAIL | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_mintZeroAddress | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| proveFail_safeTransferFromBalanceLessThanAmount | PASS | 0.19 | 0.18 | 0.18 | 0.18 | 0.18 | 0.19 | 0.18 | 0.18 | 0.18 | 0.18 | 0.18 | 0.0 |
| proveFail_safeTransferFromWhenSenderIsNotApprovedForAll | PASS | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.0 |
| proveFail_safeTransferFromWhenSenderIsNotMSGSender | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| proveFail_safeTransferFromZeroAddressForFrom | PASS | 0.02 | 0.03 | 0.02 | 0.02 | 0.02 | 0.03 | 0.02 | 0.02 | 0.02 | 0.03 | 0.02 | 0.0 |
| proveFail_safeTransferFromZeroAddressForTo | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| proveFail_setApprovalForAllSenderEqualsOperator | FAIL | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| prove_burn | PASS | 0.05 | 0.04 | 0.04 | 0.04 | 0.04 | 0.05 | 0.04 | 0.05 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_mint | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_safeBatchTransferFrom | PASS | 3.81 | 3.78 | 3.81 | 3.79 | 3.77 | 3.79 | 3.8 | 3.83 | 3.78 | 3.9 | 3.81 | 0.04 |
| prove_safeTransferFrom | PASS | 0.17 | 0.17 | 0.17 | 0.17 | 0.17 | 0.17 | 0.17 | 0.18 | 0.17 | 0.18 | 0.17 | 0.0 |
| prove_setApprovalForAll | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
FIM
"""

funcoes_status = processar_tabelas(entrada)
tabela_markdown = gerar_tabela_markdown(funcoes_status)
print(tabela_markdown)
