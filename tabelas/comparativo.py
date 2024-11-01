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
| prove_MintWhenToIsAddressZeroReverts | PASS |
| prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender | PASS |
| prove_transferFromWhenToIsAddressZeroReverts | PASS |
| prove_Burn | PASS |
| prove_BurnReverts | PASS |
| prove_Mint | PASS |
| prove_ApproveWhenIdHasNotAnOwnerReverts | FAIL |
| prove_setApprovalForAllReverts | FAIL |
| prove_setApprovalForAll | PASS |
| prove_ApproveWhenIsNotApprovedForAllReverts | PASS |
| prove_transferFromWhenFromIsNotTheOwnerReverts | PASS |
| prove_transferFrom | PASS |
| prove_ApproveWhenOwnerEqualsMSGSender | PASS |
FIM
FIM
| Função | Status | Tempo 1 | Tempo 2 | Tempo 3 | Tempo 4 | Tempo 5 | Tempo 6 | Tempo 7 | Tempo 8 | Tempo 9 | Tempo 10 | Média (s) | Desvio Padrão (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| prove_ApproveWhenIdHasNotAnOwnerReverts | PASS | 0.04 | 0.04 | 0.05 | 0.04 | 0.03 | 0.03 | 0.04 | 0.04 | 0.04 | 0.03 | 0.04 | 0.01 |
| prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| prove_ApproveWhenIsNotApprovedForAllReverts | PASS | 0.07 | 0.07 | 0.08 | 0.07 | 0.07 | 0.07 | 0.08 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| prove_ApproveWhenOwnerEqualsMSGSender | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_Burn | PASS | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.06 | 0.05 | 0.05 | 0.05 | 0.0 |
| prove_BurnReverts | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| prove_Mint | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_MintWhenToIsAddressZeroReverts | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| prove_safeTransferFrom | FAIL | 0.12 | 0.1 | 0.11 | 0.1 | 0.11 | 0.1 | 0.11 | 0.1 | 0.1 | 0.1 | 0.11 | 0.01 |
| prove_setApprovalForAll | PASS | 0.02 | 0.03 | 0.03 | 0.03 | 0.02 | 0.02 | 0.02 | 0.03 | 0.02 | 0.03 | 0.03 | 0.01 |
| prove_setApprovalForAllReverts | FAIL | 0.03 | 0.04 | 0.04 | 0.03 | 0.03 | 0.03 | 0.04 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| prove_transferFrom | PASS | 0.12 | 0.12 | 0.13 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.0 |
| prove_transferFromWhenFromIsNotTheOwnerReverts | PASS | 0.02 | 0.03 | 0.03 | 0.03 | 0.02 | 0.02 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| prove_transferFromWhenToIsAddressZeroReverts | PASS | 0.06 | 0.06 | 0.07 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |
FIM
"""

funcoes_status = processar_tabelas(entrada)
tabela_markdown = gerar_tabela_markdown(funcoes_status)
print(tabela_markdown)
