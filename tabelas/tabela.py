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


entrada = """[RUNNING] prove_safeTransferFrom(address,uint256)
   [FAIL] prove_safeTransferFrom(address,uint256)
   Counterexample:
     result:   Revert: 0x4e487b710000000000000000000000000000000000000000000000000000000000000001
     calldata: prove_safeTransferFrom(0x8000000000000000000000000000000000000000,0)
   Counterexample:
     result:   Revert: 0x4e487b710000000000000000000000000000000000000000000000000000000000000001
     calldata: prove_safeTransferFrom(0x4000000000000000000000000000001000000008,904625697587781949748551155407301487001297912094481461086239042680565792769)
[RUNNING] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256)
   [PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256)
[RUNNING] proveFail_transferFromWhenFromIsNotTheOwner(address,address,uint256)
   [FAIL] proveFail_transferFromWhenFromIsNotTheOwner(address,address,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_transferFromWhenFromIsNotTheOwner(0x0000000000000000000000000000000000000000,0x8000000000000000000000000000000000000000,0)
[RUNNING] proveFail_ApproveWhenIdHasNotAnOwner(address,uint256)
   [FAIL] proveFail_ApproveWhenIdHasNotAnOwner(address,uint256)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_ApproveWhenIdHasNotAnOwner(0x0000000000000000000000000000000000001312,0)
[RUNNING] prove_Burn(uint256)
   [PASS] prove_Burn(uint256)
[RUNNING] proveFail_ApproveWhenIsNotApprovedForAll(address,address,uint256)
   [PASS] proveFail_ApproveWhenIsNotApprovedForAll(address,address,uint256)
[RUNNING] proveFail_setApprovalForAll(address,address,bool)
   [FAIL] proveFail_setApprovalForAll(address,address,bool)
   Counterexample:
     result:   Successful execution
     calldata: proveFail_setApprovalForAll(0x8040000000000000000080000000000000000002,0x0000000000000000000000000000000000000000,false)
[RUNNING] prove_Mint(address,uint256)
   [PASS] prove_Mint(address,uint256)
[RUNNING] proveFail_transferFromWhenToIsAddressZero(address,address,uint256)
   [PASS] proveFail_transferFromWhenToIsAddressZero(address,address,uint256)
[RUNNING] proveFail_MintWhenToIsAddressZero(address,uint256)
   [PASS] proveFail_MintWhenToIsAddressZero(address,uint256)
[RUNNING] proveFail_Burn(uint256)
   [PASS] proveFail_Burn(uint256)
[RUNNING] prove_setApprovalForAll(address,bool)
   [PASS] prove_setApprovalForAll(address,bool)
[RUNNING] prove_transferFrom(address,address,uint256)
   [PASS] prove_transferFrom(address,address,uint256)
[RUNNING] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256)
   [PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256)
"""

# Gerando a tabela em Markdown considerando 'PASS' e 'FAIL'
tabela = gerar_tabela_markdown_pass_fail(entrada)
print(tabela)
