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
     calldata: prove_safeTransferFrom(0x1000000000000000000000000000000000000000,0)
   Counterexample:
     result:   Revert: 0x4e487b710000000000000000000000000000000000000000000000000000000000000001
     calldata: prove_safeTransferFrom(0x0000020800000000000000401800000000001000,7237447289098456910489210153605429003754138173869686222113041559658740842496)
[RUNNING] prove_MintWhenToIsAddressZeroReverts(address,uint256)
   [PASS] prove_MintWhenToIsAddressZeroReverts(address,uint256)
[RUNNING] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256)
   [PASS] prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender(address,uint256)
[RUNNING] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256)
   [PASS] prove_transferFromWhenToIsAddressZeroReverts(address,address,uint256)
[RUNNING] prove_Burn(uint256)
   [PASS] prove_Burn(uint256)
[RUNNING] prove_BurnReverts(uint256)
   [PASS] prove_BurnReverts(uint256)
[RUNNING] prove_Mint(address,uint256)
   [PASS] prove_Mint(address,uint256)
[RUNNING] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256)
   [FAIL] prove_ApproveWhenIdHasNotAnOwnerReverts(address,uint256)
   Counterexample:
     result:   Revert: 0x4e487b710000000000000000000000000000000000000000000000000000000000000001
     calldata: prove_ApproveWhenIdHasNotAnOwnerReverts(0x0000000000000000000000000000000000001312,0)
[RUNNING] prove_setApprovalForAllReverts(address,address,bool)
   [FAIL] prove_setApprovalForAllReverts(address,address,bool)
   Counterexample:
     result:   Revert: 0x4e487b710000000000000000000000000000000000000000000000000000000000000001
     calldata: prove_setApprovalForAllReverts(0xFFfFfFffFFfffFFfFFfFFFFFffFFFffffFfFFFfF,0x0000000000000000000000000000000000001312,false)
[RUNNING] prove_setApprovalForAll(address,bool)
   [PASS] prove_setApprovalForAll(address,bool)
[RUNNING] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256)
   [PASS] prove_ApproveWhenIsNotApprovedForAllReverts(address,address,uint256)
[RUNNING] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256)
   [PASS] prove_transferFromWhenFromIsNotTheOwnerReverts(address,address,uint256)
[RUNNING] prove_transferFrom(address,address,uint256)
   [PASS] prove_transferFrom(address,address,uint256)
[RUNNING] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256)
   [PASS] prove_ApproveWhenOwnerEqualsMSGSender(address,uint256)
"""

# Gerando a tabela em Markdown considerando 'PASS' e 'FAIL'
tabela = gerar_tabela_markdown_pass_fail(entrada)
print(tabela)
