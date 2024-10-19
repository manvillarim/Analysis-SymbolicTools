def gerar_tabela_markdown_pass_fail(entrada):
    linhas = entrada.split("\n")
    funcoes_status = []
    for linha in linhas:
        if "[PASS]" in linha or "[FAIL]" in linha:
            status, funcao = linha.strip().split(" ", 1)
            status = status.replace("[", "").replace("]", "")
            nome_funcao = funcao.split("(")[0]
            funcoes_status.append((nome_funcao, status))

    tabela_markdown = "| Função | Status |\n"
    tabela_markdown += "|--------|--------|\n"

    for funcao, status in funcoes_status:
        tabela_markdown += f"| {funcao} | {status} |\n"

    return tabela_markdown


entrada = """[RUNNING] proveFail_TransferUnderBalancej(address,uint256)
   [PASS] proveFail_TransferUnderBalancej(address,uint256)
[RUNNING] prove_ZeroAddressHasNoToken()
   [PASS] prove_ZeroAddressHasNoToken()
[RUNNING] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256)
   [PASS] prove_TokenReceiverCanTransferFromTotalBalance(address,address,uint256)
[RUNNING] prove_TransferFromNoFees(address,address,address,uint256)
   [PASS] prove_TransferFromNoFees(address,address,address,uint256)
[RUNNING] prove_MintZeroTokens(address)
   [PASS] prove_MintZeroTokens(address)
[RUNNING] proveFail_TransferFromUnderBalancei(address,address,uint256)
   [PASS] proveFail_TransferFromUnderBalancei(address,address,uint256)
[RUNNING] prove_TransferZeroAmount(address,address)
   [PASS] prove_TransferZeroAmount(address,address)
[RUNNING] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address)
   [PASS] prove_TokenReceiverCanTransferFromTotalBalanceZero(address,address,address)
[RUNNING] prove_AllowanceUpdatedAfterBurn(address,address,uint256)
   [PASS] prove_AllowanceUpdatedAfterBurn(address,address,uint256)
[RUNNING] prove_Approve(address,uint256)
   [PASS] prove_Approve(address,uint256)
[RUNNING] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256)
   [PASS] prove_SelfApproveAndTransferFromOwnAccount(address,address,uint256)
[RUNNING] prove_SelfTransferZeroAmountAllowed(address)
   [PASS] prove_SelfTransferZeroAmountAllowed(address)
[RUNNING] prove_TransferFromDecreasesAllowance(address,address,address,uint256)
   [PASS] prove_TransferFromDecreasesAllowance(address,address,address,uint256)
[RUNNING] prove_BurnSameAccount(address,uint256)
   [PASS] prove_BurnSameAccount(address,uint256)
[RUNNING] prove_TransferFrom(address,address,uint256,uint256)
   [PASS] prove_TransferFrom(address,address,uint256,uint256)
[RUNNING] prove_TransferFromZeroAmount(address,address,address)
   [PASS] prove_TransferFromZeroAmount(address,address,address)
[RUNNING] proveFail_TransferFromZeroAddress(address,address,uint256)
   [PASS] proveFail_TransferFromZeroAddress(address,address,uint256)
[RUNNING] prove_SelfTransferPositiveAmountAllowed(address,uint256)
   [PASS] prove_SelfTransferPositiveAmountAllowed(address,uint256)
[RUNNING] proveFail_BurnUnderBalance(address,uint256)
   [PASS] proveFail_BurnUnderBalance(address,uint256)
[RUNNING] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256)
   [PASS] proveFail_TransferFromAllowanceReachesZero(address,address,address,uint256,uint256)
[RUNNING] prove_MultipleTransfersAllowed(address,address,uint256,uint256)
   [PASS] prove_MultipleTransfersAllowed(address,address,uint256,uint256)
[RUNNING] proveFail_MintToZeroAddress(uint256)
   [FAIL] proveFail_MintToZeroAddress(uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_MintToZeroAddress(112777989180875142641012667662881322846184324395630932477102348584379903997143)
[RUNNING] prove_ApproveNonZeroAmount(address,address,uint256)
   [PASS] prove_ApproveNonZeroAmount(address,address,uint256)
[RUNNING] prove_SelfApprovePositiveAmount(address,uint256)
   [PASS] prove_SelfApprovePositiveAmount(address,uint256)
[RUNNING] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256)
   [PASS] prove_TransferFromDoesNotUpdateOtherBalances(address,address,address,address,uint256)
[RUNNING] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256)
   [FAIL] proveFail_TransferFromZeroAddressForMSGSender(address,address,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_TransferFromZeroAddressForMSGSender(0x1000000001000000000000000000000000004000,0x0000000000000000000000000000000000000040,0)
[RUNNING] prove_MsgSenderCanRetrieveOtherBalance(address,uint256)
   [PASS] prove_MsgSenderCanRetrieveOtherBalance(address,uint256)
[RUNNING] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address)
   [PASS] prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed(address,address)
[RUNNING] prove_Mint(address,uint256)
   [PASS] prove_Mint(address,uint256)
[RUNNING] proveFail_ApproveZeroAddress(address,uint256)
   [FAIL] proveFail_ApproveZeroAddress(address,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_ApproveZeroAddress(0x0000000000000000000000000000000000000000,0)
[RUNNING] proveFail_TransferToZeroAddress(address,uint256)
   [FAIL] proveFail_TransferToZeroAddress(address,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_TransferToZeroAddress(0x8000000000000000000000000000000000000000,57896044618658097711785492504343953926634992332820282019728792003956564819968)
[RUNNING] proveFail_BurnUnderSupply(address,uint256)
   [PASS] proveFail_BurnUnderSupply(address,uint256)
[RUNNING] proveFail_ApproveFromZeroAddress(address,uint256)
   [FAIL] proveFail_ApproveFromZeroAddress(address,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_ApproveFromZeroAddress(0x8000000000000000000000000000000000000000,57896044618658097711785492504343953926634992332820282019728792003956564819968)
[RUNNING] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8)
   [PASS] prove_MultipleTransfersOfZeroAmountAllowed(address,address,uint8)
[RUNNING] proveFail_ApproveZeroAddressForMSGSender(address,uint256)
   [FAIL] proveFail_ApproveZeroAddressForMSGSender(address,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_ApproveZeroAddressForMSGSender(0x8000000000000000000000000000000000000000,0)
[RUNNING] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256)
   [PASS] prove_TransferDoesNotUpdateOtherBalances(address,address,address,uint256)
[RUNNING] prove_BurnZeroTokens(address)
   [PASS] prove_BurnZeroTokens(address)
[RUNNING] prove_SelfApproveZeroAmountAllowed(address)
   [PASS] prove_SelfApproveZeroAmountAllowed(address)
[RUNNING] prove_MsgSenderCanRetrieveOwnBalance(uint256)
   [PASS] prove_MsgSenderCanRetrieveOwnBalance(uint256)
[RUNNING] prove_MsgSenderCanTransferTotalBalance(address,address,uint256)
   [PASS] prove_MsgSenderCanTransferTotalBalance(address,address,uint256)
[RUNNING] prove_BurnDifferentAccount(address,uint256,address,uint256)
   [PASS] prove_BurnDifferentAccount(address,uint256,address,uint256)
[RUNNING] prove_MsgSenderCanTransferTotalBalanceZero(address,address)
   [PASS] prove_MsgSenderCanTransferTotalBalanceZero(address,address)
[RUNNING] proveFail_TransferFromUnderBalance(address,address,uint256)
   [PASS] proveFail_TransferFromUnderBalance(address,address,uint256)
[RUNNING] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256)
   [PASS] prove_ConsecutiveApprovePositiveToPositive(address,address,uint256,uint256)
[RUNNING] proveFail_BurnFromZeroAddress(uint256)
   [PASS] proveFail_BurnFromZeroAddress(uint256)
[RUNNING] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256)
   [PASS] prove_MultipleTransferFromAllowed(address,address,address,uint256,uint256)
[RUNNING] proveFail_TransferFromZeroAddress(address,uint256)
   [PASS] proveFail_TransferFromZeroAddress(address,uint256)
[RUNNING] proveFail_TransferUnderBalance(address,uint256)
   [PASS] proveFail_TransferUnderBalance(address,uint256)
[RUNNING] prove_Transfer(address,uint256,uint256)
   [PASS] prove_Transfer(address,uint256,uint256)
[RUNNING] prove_IncreaseAllowance(address,uint256)
   [PASS] prove_IncreaseAllowance(address,uint256)
[RUNNING] prove_BalanceUpdatedAfterBurn(address,address,uint256)
   [PASS] prove_BalanceUpdatedAfterBurn(address,address,uint256)
[RUNNING] prove_ApproveZeroAmount(address,address)
   [PASS] prove_ApproveZeroAmount(address,address)
[RUNNING] proveFail_TransferZeroAmountToZeroAddressReverts(address)
   [FAIL] proveFail_TransferZeroAmountToZeroAddressReverts(address)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_TransferZeroAmountToZeroAddressReverts(0x8000000000000000000000000000000000000000)
[RUNNING] proveFail_TransferFromToZeroAddress33(address,address,uint256)
   [FAIL] proveFail_TransferFromToZeroAddress33(address,address,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_TransferFromToZeroAddress33(0x000000000000000000000000000000000000ACAb,0x2000000000000000020002C02000000084000000,115792089237316195423570985008687907853269984665640564039457584007913129639935)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_TransferFromToZeroAddress33(0x000000000000000000000000000000000000ACAb,0x080000000100000000000000080000809E00649E,1809251394333065553493296640763603055933037797083688848518798347828176355328)
[RUNNING] prove_DecreaseAllowance(address,uint256)
   [PASS] prove_DecreaseAllowance(address,uint256)
[RUNNING] prove_ApproveMaxAmount(address,address)
   [PASS] prove_ApproveMaxAmount(address,address)
[RUNNING] prove_BurnFromNonZeroAddress(address,uint256)
   [PASS] prove_BurnFromNonZeroAddress(address,uint256)
[RUNNING] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address)
   [FAIL] proveFail_TransferFromZeroAmountToZeroAddressReverts(address,address)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_TransferFromZeroAmountToZeroAddressReverts(0x0208000080008000008000000200000000120000,0x0400FffF00Ff20A7200210Ff6f1B20FD11eC30C4)
[RUNNING] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8)
   [PASS] prove_MultipleTransferFromsOfZeroAmountAllowed(address,address,address,uint8)
[RUNNING] proveFail_MintOverflow(address)
   [PASS] proveFail_MintOverflow(address)
[RUNNING] proveFail_ApproveToZeroAddress(address,uint256)
   [FAIL] proveFail_ApproveToZeroAddress(address,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_ApproveToZeroAddress(0x8000000000000000000000000000000000000000,57896044618658097711785492504343953926634992332820282019728792003956564819968)
"""

# Gerando a tabela em Markdown considerando 'PASS' e 'FAIL'
tabela = gerar_tabela_markdown_pass_fail(entrada)
print(tabela)
