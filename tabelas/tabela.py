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


entrada = """[RUNNING] proveFail_burnZeroAddress(uint256,uint256)
   [FAIL] proveFail_burnZeroAddress(uint256,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_burnZeroAddress(158369282369516421886509056,0)
[RUNNING] proveFail_setApprovalForAllSenderEqualsOperator(address,bool)
   [FAIL] proveFail_setApprovalForAllSenderEqualsOperator(address,bool)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_setApprovalForAllSenderEqualsOperator(0x0000000000000000000000000000000000000000,false)
[RUNNING] proveFail_mintZeroAddress(uint256,uint256)
   [PASS] proveFail_mintZeroAddress(uint256,uint256)
[RUNNING] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256)
   [PASS] proveFail_burnBalanceLessThanAmount(uint256,uint256,uint256)
[RUNNING] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256)
   [FAIL] proveFail_safeTransferFromWhenSenderIsNotMSGSender(uint256,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_safeTransferFromWhenSenderIsNotMSGSender(0,0)
[RUNNING] prove_mint(uint256,uint256)
   [PASS] prove_mint(uint256,uint256)
[RUNNING] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256)
   [PASS] proveFail_safeTransferFromWhenSenderIsNotApprovedForAll(uint256,uint256)
[RUNNING] prove_safeTransferFrom(uint256,uint256,uint256)
   [PASS] prove_safeTransferFrom(uint256,uint256,uint256)
[RUNNING] prove_burn(uint256,uint256)
   [PASS] prove_burn(uint256,uint256)
[RUNNING] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256)
   [PASS] proveFail_safeTransferFromBalanceLessThanAmount(uint256,uint256,uint256)
[RUNNING] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256)
   [PASS] proveFail_safeTransferFromZeroAddressForTo(uint256,uint256)
[RUNNING] prove_setApprovalForAll(address,bool)
   [PASS] prove_setApprovalForAll(address,bool)
[RUNNING] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256)
   [PASS] proveFail_safeTransferFromZeroAddressForFrom(uint256,uint256)
"""

# Gerando a tabela em Markdown considerando 'PASS' e 'FAIL'
tabela = gerar_tabela_markdown_pass_fail(entrada)
print(tabela)
