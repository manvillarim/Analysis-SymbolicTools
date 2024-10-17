import re


def processar_tabelas(entrada):
    tabelas = entrada.split("FIM")
    hevm = tabelas[0].strip().split("\n")
    kontrol = tabelas[1].strip().split("\n")
    halmos = tabelas[2].strip().split("\n")

    funcoes_status = {}

    # Processa a tabela hevm
    for linha in hevm:
        match = re.search(r"\|\s*(\w+)\s*\|\s*(PASS|FAIL)", linha)
        if match:
            funcao, status = match.groups()
            funcoes_status[funcao] = {"hevm": status, "kontrol": "N/A", "halmos": "N/A"}

    # Processa a tabela kontrol
    for linha in kontrol:
        match = re.search(r"\|\s*(\w+)\s*\|\s*(PASS|FAIL)", linha)
        if match:
            funcao, status = match.groups()
            if funcao in funcoes_status:
                funcoes_status[funcao]["kontrol"] = status

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
| proveFail_TransferUnderBalancej | PASS |
| prove_ZeroAddressHasNoToken | PASS |
| prove_TokenReceiverCanTransferFromTotalBalance | PASS |
| prove_TransferFromNoFees | PASS |
| prove_MintZeroTokens | PASS |
| proveFail_TransferFromUnderBalancei | PASS |
| prove_TransferZeroAmount | PASS |
| prove_TokenReceiverCanTransferFromTotalBalanceZero | PASS |
| prove_AllowanceUpdatedAfterBurn | PASS |
| prove_Approve | PASS |
| prove_SelfApproveAndTransferFromOwnAccount | PASS |
| prove_SelfTransferZeroAmountAllowed | PASS |
| prove_TransferFromDecreasesAllowance | PASS |
| prove_BurnSameAccount | PASS |
| prove_TransferFrom | PASS |
| prove_TransferFromZeroAmount | PASS |
| proveFail_TransferFromZeroAddress | PASS |
| prove_SelfTransferPositiveAmountAllowed | PASS |
| proveFail_BurnUnderBalance | PASS |
| proveFail_TransferFromAllowanceReachesZero | PASS |
| prove_MultipleTransfersAllowed | PASS |
| proveFail_MintToZeroAddress | PASS |
| prove_ApproveNonZeroAmount | PASS |
| prove_SelfApprovePositiveAmount | PASS |
| prove_TransferFromDoesNotUpdateOtherBalances | PASS |
| proveFail_TransferFromZeroAddressForMSGSender | PASS |
| prove_MsgSenderCanRetrieveOtherBalance | PASS |
| prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed | PASS |
| prove_Mint | PASS |
| proveFail_ApproveZeroAddress | PASS |
| proveFail_TransferToZeroAddress | PASS |
| proveFail_BurnUnderSupply | PASS |
| proveFail_ApproveFromZeroAddress | PASS |
| prove_MultipleTransfersOfZeroAmountAllowed | PASS |
| proveFail_ApproveZeroAddressForMSGSender | PASS |
| prove_TransferDoesNotUpdateOtherBalances | PASS |
| prove_BurnZeroTokens | PASS |
| prove_SelfApproveZeroAmountAllowed | PASS |
| prove_MsgSenderCanRetrieveOwnBalance | PASS |
| prove_MsgSenderCanTransferTotalBalance | PASS |
| prove_BurnDifferentAccount | PASS |
| prove_MsgSenderCanTransferTotalBalanceZero | PASS |
| proveFail_TransferFromUnderBalance | PASS |
| prove_ConsecutiveApprovePositiveToPositive | PASS |
| proveFail_BurnFromZeroAddress | PASS |
| prove_MultipleTransferFromAllowed | PASS |
| proveFail_TransferFromZeroAddress | PASS |
| proveFail_TransferUnderBalance | PASS |
| prove_Transfer | PASS |
| prove_IncreaseAllowance | PASS |
| prove_BalanceUpdatedAfterBurn | PASS |
| prove_ApproveZeroAmount | PASS |
| proveFail_TransferZeroAmountToZeroAddressReverts | PASS |
| proveFail_TransferFromToZeroAddress33 | PASS |
| prove_DecreaseAllowance | PASS |
| prove_ApproveMaxAmount | PASS |
| prove_BurnFromNonZeroAddress | PASS |
| proveFail_TransferFromZeroAmountToZeroAddressReverts | PASS |
| prove_MultipleTransferFromsOfZeroAmountAllowed | PASS |
| proveFail_MintOverflow | PASS |
| proveFail_ApproveToZeroAddress | PASS |
FIM
| prove_TransferFrom | FAIL |
| prove_Approve | FAIL |
| prove_MsgSenderCanTransferTotalBalanceZero | FAIL |
| prove_TransferFromDecreasesAllowance | FAIL |
| proveFail_BurnFromZeroAddress | FAIL |
| prove_ApproveNonZeroAmount | FAIL |
| proveFail_ApproveZeroAddress | FAIL |
| proveFail_TransferUnderBalance | FAIL |
| prove_MintZeroTokens | FAIL |
| prove_BurnZeroTokens | FAIL |
| prove_IncreaseAllowance | FAIL |
| prove_MultipleTransfersAllowed | FAIL |
| prove_SelfApproveAndTransferFromOwnAccount | FAIL |
| proveFail_TransferFromZeroAmountToZeroAddressReverts | FAIL |
| proveFail_TransferToZeroAddress | FAIL |
| proveFail_TransferFromZeroAddress | FAIL |
| prove_TransferDoesNotUpdateOtherBalances | PASS |
| prove_TransferFromNoFees | FAIL |
| prove_TransferZeroAmount | FAIL |
| prove_ZeroAddressHasNoToken | PASS |
| prove_SelfApproveZeroAmountAllowed | FAIL |
| proveFail_BurnUnderBalance | FAIL |
| proveFail_ApproveFromZeroAddress | FAIL |
| proveFail_TransferUnderBalancej | FAIL |
| prove_TokenReceiverCanTransferFromTotalBalanceZero | FAIL |
| proveFail_MintOverflow | FAIL |
| prove_MultipleTransfersOfZeroAmountAllowed | FAIL |
| prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed | FAIL |
| prove_BurnDifferentAccount | FAIL |
| prove_SelfTransferZeroAmountAllowed | FAIL |
| prove_MsgSenderCanRetrieveOwnBalance | FAIL |
| prove_TransferFromDoesNotUpdateOtherBalances | FAIL |
| prove_BurnFromNonZeroAddress | FAIL |
| proveFail_ApproveZeroAddressForMSGSender | FAIL |
| prove_ConsecutiveApprovePositiveToPositive | FAIL |
| proveFail_TransferFromZeroAddress | FAIL |
| prove_MultipleTransferFromAllowed | FAIL |
| prove_BalanceUpdatedAfterBurn | FAIL |
| prove_MultipleTransferFromsOfZeroAmountAllowed | FAIL |
| prove_DecreaseAllowance | FAIL |
| prove_Transfer | FAIL |
| proveFail_TransferFromToZeroAddress33 | FAIL |
| prove_SelfTransferPositiveAmountAllowed | FAIL |
| prove_TokenReceiverCanTransferFromTotalBalance | FAIL |
| prove_BurnSameAccount | FAIL |
| prove_ApproveZeroAmount | FAIL |
| proveFail_TransferZeroAmountToZeroAddressReverts | FAIL |
| prove_ApproveMaxAmount | FAIL |
| prove_MsgSenderCanRetrieveOtherBalance | FAIL |
| proveFail_BurnUnderSupply | FAIL |
| prove_Mint | FAIL |
| prove_MsgSenderCanTransferTotalBalance | FAIL |
| prove_TransferFromZeroAmount | FAIL |
| proveFail_ApproveToZeroAddress | FAIL |
| prove_SelfApprovePositiveAmount | FAIL |
| prove_AllowanceUpdatedAfterBurn | FAIL |
| proveFail_TransferFromAllowanceReachesZero | FAIL |
| proveFail_MintToZeroAddress | FAIL |
| proveFail_TransferFromUnderBalance | FAIL |
| proveFail_TransferFromUnderBalancei | FAIL |
| proveFail_TransferFromZeroAddressForMSGSender | FAIL |
FIM
| proveFail_ApproveFromZeroAddress | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_ApproveToZeroAddress | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.03 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| proveFail_ApproveZeroAddress | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| proveFail_ApproveZeroAddressForMSGSender | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| proveFail_BurnFromZeroAddress | PASS | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| proveFail_BurnUnderBalance | PASS | 0.03 | 0.03 | 0.03 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.03 | 0.04 | 0.04 | 0.01 |
| proveFail_BurnUnderSupply | PASS | 0.03 | 0.03 | 0.03 | 0.04 | 0.03 | 0.03 | 0.03 | 0.04 | 0.03 | 0.04 | 0.03 | 0.0 |
| proveFail_MintOverflow | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_MintToZeroAddress | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| proveFail_TransferFromAllowanceReachesZero | PASS | 0.2 | 0.2 | 0.2 | 0.2 | 0.21 | 0.2 | 0.2 | 0.22 | 0.2 | 0.21 | 0.2 | 0.01 |
| proveFail_TransferFromToZeroAddress33 | PASS | 0.08 | 0.08 | 0.08 | 0.08 | 0.09 | 0.08 | 0.08 | 0.09 | 0.08 | 0.08 | 0.08 | 0.0 |
| proveFail_TransferFromUnderBalance | PASS | 0.16 | 0.18 | 0.18 | 0.18 | 0.18 | 0.18 | 0.18 | 0.2 | 0.18 | 0.16 | 0.18 | 0.01 |
| proveFail_TransferFromUnderBalancei | PASS | 0.05 | 0.05 | 0.05 | 0.06 | 0.06 | 0.05 | 0.05 | 0.06 | 0.05 | 0.05 | 0.05 | 0.0 |
| proveFail_TransferFromZeroAddress | PASS | 0.03 | 0.02 | 0.03 | 0.02 | 0.03 | 0.02 | 0.03 | 0.02 | 0.03 | 0.02 | 0.03 | 0.01 |
| proveFail_TransferFromZeroAddressForMSGSender | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_TransferFromZeroAmountToZeroAddressReverts | PASS | 0.06 | 0.06 | 0.06 | 0.05 | 0.05 | 0.05 | 0.06 | 0.06 | 0.06 | 0.05 | 0.06 | 0.01 |
| proveFail_TransferToZeroAddress | PASS | 0.04 | 0.03 | 0.03 | 0.03 | 0.04 | 0.04 | 0.03 | 0.04 | 0.04 | 0.04 | 0.04 | 0.01 |
| proveFail_TransferUnderBalance | PASS | 0.09 | 0.09 | 0.09 | 0.09 | 0.09 | 0.09 | 0.09 | 0.1 | 0.09 | 0.09 | 0.09 | 0.0 |
| proveFail_TransferUnderBalancej | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.04 | 0.03 | 0.03 | 0.0 |
| proveFail_TransferZeroAmountToZeroAddressReverts | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.02 | 0.01 | 0.01 | 0.0 |
| prove_AllowanceUpdatedAfterBurn | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.08 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| prove_Approve | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.05 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.01 |
| prove_ApproveMaxAmount | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_ApproveNonZeroAmount | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_ApproveZeroAmount | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.05 | 0.04 | 0.04 | 0.0 |
| prove_BalanceUpdatedAfterBurn | PASS | 0.09 | 0.09 | 0.09 | 0.1 | 0.1 | 0.1 | 0.1 | 0.09 | 0.1 | 0.1 | 0.1 | 0.01 |
| prove_BurnDifferentAccount | PASS | 0.12 | 0.11 | 0.11 | 0.12 | 0.12 | 0.12 | 0.11 | 0.12 | 0.12 | 0.12 | 0.12 | 0.0 |
| prove_BurnFromNonZeroAddress | PASS | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.07 | 0.05 | 0.05 | 0.05 | 0.05 | 0.01 |
| prove_BurnSameAccount | PASS | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |
| prove_BurnZeroTokens | PASS | 0.04 | 0.04 | 0.04 | 0.03 | 0.04 | 0.04 | 0.03 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_ConsecutiveApprovePositiveToPositive | PASS | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |
| prove_DecreaseAllowance | PASS | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 | 0.09 | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 | 0.0 |
| prove_IncreaseAllowance | PASS | 0.08 | 0.07 | 0.07 | 0.07 | 0.07 | 0.08 | 0.07 | 0.07 | 0.07 | 0.08 | 0.07 | 0.0 |
| prove_Mint | PASS | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.0 |
| prove_MintZeroTokens | PASS | 0.03 | 0.03 | 0.03 | 0.04 | 0.04 | 0.04 | 0.03 | 0.04 | 0.03 | 0.04 | 0.04 | 0.01 |
| prove_MsgSenderCanRetrieveOtherBalance | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| prove_MsgSenderCanRetrieveOwnBalance | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.03 | 0.02 | 0.02 | 0.0 |
| prove_MsgSenderCanTransferTotalBalance | PASS | 0.1 | 0.09 | 0.09 | 0.09 | 0.09 | 0.1 | 0.09 | 0.09 | 0.1 | 0.09 | 0.09 | 0.0 |
| prove_MsgSenderCanTransferTotalBalanceZero | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| prove_MultipleTransferFromAllowed | PASS | 0.39 | 0.36 | 0.36 | 0.37 | 0.37 | 0.39 | 0.37 | 0.36 | 0.36 | 0.36 | 0.37 | 0.01 |
| prove_MultipleTransferFromsOfZeroAmountAllowed | PASS | 0.22 | 0.21 | 0.21 | 0.21 | 0.21 | 0.22 | 0.21 | 0.22 | 0.21 | 0.22 | 0.21 | 0.01 |
| prove_MultipleTransfersAllowed | PASS | 0.13 | 0.13 | 0.13 | 0.14 | 0.13 | 0.13 | 0.13 | 0.13 | 0.13 | 0.13 | 0.13 | 0.0 |
| prove_MultipleTransfersOfZeroAmountAllowed | PASS | 0.17 | 0.18 | 0.18 | 0.17 | 0.17 | 0.18 | 0.17 | 0.17 | 0.17 | 0.18 | 0.17 | 0.01 |
| prove_SelfApproveAndTransferFromOwnAccount | PASS | 0.18 | 0.17 | 0.17 | 0.17 | 0.17 | 0.19 | 0.17 | 0.17 | 0.17 | 0.17 | 0.17 | 0.01 |
| prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed | PASS | 0.1 | 0.09 | 0.09 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.09 | 0.1 | 0.1 | 0.0 |
| prove_SelfApprovePositiveAmount | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_SelfApproveZeroAmountAllowed | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.04 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| prove_SelfTransferPositiveAmountAllowed | PASS | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.07 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |
| prove_SelfTransferZeroAmountAllowed | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.05 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_TokenReceiverCanTransferFromTotalBalance | PASS | 0.17 | 0.17 | 0.17 | 0.17 | 0.17 | 0.18 | 0.17 | 0.17 | 0.17 | 0.17 | 0.17 | 0.0 |
| prove_TokenReceiverCanTransferFromTotalBalanceZero | PASS | 0.11 | 0.11 | 0.11 | 0.14 | 0.14 | 0.11 | 0.11 | 0.11 | 0.11 | 0.11 | 0.12 | 0.01 |
| prove_Transfer | PASS | 0.1 | 0.1 | 0.1 | 0.11 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.0 |
| prove_TransferDoesNotUpdateOtherBalances | PASS | 0.14 | 0.14 | 0.14 | 0.14 | 0.14 | 0.15 | 0.14 | 0.14 | 0.14 | 0.14 | 0.14 | 0.0 |
| prove_TransferFrom | PASS | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.17 | 0.16 | 0.16 | 0.16 | 0.16 | 0.16 | 0.0 |
| prove_TransferFromDecreasesAllowance | PASS | 0.15 | 0.14 | 0.14 | 0.15 | 0.15 | 0.15 | 0.15 | 0.15 | 0.15 | 0.15 | 0.15 | 0.0 |
| prove_TransferFromDoesNotUpdateOtherBalances | PASS | 0.18 | 0.18 | 0.18 | 0.18 | 0.18 | 0.19 | 0.17 | 0.18 | 0.18 | 0.18 | 0.18 | 0.0 |
| prove_TransferFromNoFees | PASS | 0.17 | 0.17 | 0.17 | 0.17 | 0.18 | 0.18 | 0.18 | 0.18 | 0.17 | 0.18 | 0.17 | 0.01 |
| prove_TransferFromZeroAmount | PASS | 0.09 | 0.09 | 0.09 | 0.09 | 0.09 | 0.09 | 0.08 | 0.09 | 0.09 | 0.09 | 0.09 | 0.0 |
| prove_TransferZeroAmount | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| prove_ZeroAddressHasNoToken | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
FIM
"""

funcoes_status = processar_tabelas(entrada)
tabela_markdown = gerar_tabela_markdown(funcoes_status)
print(tabela_markdown)
