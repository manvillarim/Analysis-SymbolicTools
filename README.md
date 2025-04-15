# COMPARATIVE ANALYSIS OF SYMBOLIC TESTING TOOLS FOR SMART CONTRACTS
<br>

<br>

**CONFIGURATION: INTEL CORE I5 12500h 16gb RAM**

**OS: Fedora**

**Versions**

> Halmos: 0.2.0

> Hevm: 0.53.0

> Kontrol: 1.0.34

<br>

<br>

# ERC20 OPEN ZEPPELIN
<br>

<br>

## HALMOS

| Function | Status | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Average (s) | Standard Deviation (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---  |
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

**Total Tests Done:** 61
**Total Tests Passed:** 61
**Total Failed Tests** 0


**TOTAL TIME**

|             | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Average | Standard Deviation |
|-------------|---------|---------|---------|---------|---------|---------|---------|---------|---------|----------|-------|---------------|
| **Real**    | 9,409s   | 9,538s   | 9,110s   | 9,078s   | 9,429s   | 9,389s   | 9,169s   | 9,055s   | 9,063s   | 9,562s    | 9,280s | 0,203s         |
| **User**    | 8,991s   | 9,189s   | 8,811s   | 8,732s   | 9,034s   | 8,997s   | 8,799s   | 8,741s   | 8,734s   | 9,179s    | 8,920s | 0,172s         |
| **Sys**     | 0,416s   | 0,412s   | 0,376s  | 0,423s   | 0,400s   | 0,392s   | 0,401s   | 0,397s   | 0,405s   | 0,450s    | 0,407s | 0,021s         |

<br>

<br>

## HEVM


| Function | Status |
|--------|--------|
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

**Total Tests Done:** 61
**Total Tests Passed:** 61
**Total Failed Tests:** 0

**TOTAL TIME**

|             | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Average | Standard Deviation |
|-------------|----------|----------|----------|----------|----------|----------|----------|----------|----------|----------|---------|---------------|
| **Real**    | 21m56,452s | 21m14,008s | 21m38,340s | 21m30,129s | 21m17,406s | 21m15,757s | 21m7,386s | 21m7,321s | 21m6,827s | 21m7,269s | 21m27,289s | 0,314s     |
| **User**    | 30m14,772s | 31m9,159s  | 30m7,216s  | 39m6,208s  | 25m44,806s | 38m50,550s | 35m58,286s | 30m31,676s | 37m39,034s | 30m23,078s | 32m45,979s | 4,53s     |
| **Sys**     | 1m42,760s  | 1m46,750s  | 1m49,017s  | 1m43,876s  | 1m47,127s  | 1m50,225s  | 1m47,730s  | 1m49,681s  | 1m49,200s  | 1m48,921s  | 1m47,429s | 0,027s     |

<br>

<br>

## KONTROL

| Function | Status |
|--------|--------|
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

**Total Tests Done:** 61
**Total Tests Passed:** 2
**Total Failed Tests:** 59

**TOTAL TIME**

|             | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Average | Standard Deviation |
|-------------|--------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|--------------|---------|---------------|
| **Real**    | 65m15,047s   | 49m51,999s  | 50m27,520s  | 51m52,399s  | 54m28,138s  | 56m53,043s  | 59m42,752s  | 55m3,567s   | 55m7,429s    | 55m29s | 5.22s         |
| **User**    | 69m41,402s   | 53m6,263s   | 53m40,101s  | 55m16,569s  | 57m36,731s  | 61m3,788s   | 63m58,455s  | 58m47,940s  | 58m52,374s   | 58m43s | 4.76s         |
| **Sys**     | 2m33,459s    | 2m9,561s    | 2m5,479s    | 2m10,533s   | 2m16,575s   | 2m22,532s   | 2m29,200s   | 2m10,641s   | 2m15,386s    | 2m17s  | 0.56s         |


<br>

<br>

## GENERAL COMPARISION

| Function | HEVM Status | Kontrol Status | Halmos Status |
|--------|-------------|----------------|---------------|
| proveFail_TransferUnderBalancej | PASS | FAIL | PASS |
| prove_ZeroAddressHasNoToken | PASS | PASS | PASS |
| prove_TokenReceiverCanTransferFromTotalBalance | PASS | FAIL | PASS |
| prove_TransferFromNoFees | PASS | FAIL | PASS |
| prove_MintZeroTokens | PASS | FAIL | PASS |
| proveFail_TransferFromUnderBalancei | PASS | FAIL | PASS |
| prove_TransferZeroAmount | PASS | FAIL | PASS |
| prove_TokenReceiverCanTransferFromTotalBalanceZero | PASS | FAIL | PASS |
| prove_AllowanceUpdatedAfterBurn | PASS | FAIL | PASS |
| prove_Approve | PASS | FAIL | PASS |
| prove_SelfApproveAndTransferFromOwnAccount | PASS | FAIL | PASS |
| prove_SelfTransferZeroAmountAllowed | PASS | FAIL | PASS |
| prove_TransferFromDecreasesAllowance | PASS | FAIL | PASS |
| prove_BurnSameAccount | PASS | FAIL | PASS |
| prove_TransferFrom | PASS | FAIL | PASS |
| prove_TransferFromZeroAmount | PASS | FAIL | PASS |
| proveFail_TransferFromZeroAddress | PASS | FAIL | PASS |
| prove_SelfTransferPositiveAmountAllowed | PASS | FAIL | PASS |
| proveFail_BurnUnderBalance | PASS | FAIL | PASS |
| proveFail_TransferFromAllowanceReachesZero | PASS | FAIL | PASS |
| prove_MultipleTransfersAllowed | PASS | FAIL | PASS |
| proveFail_MintToZeroAddress | PASS | FAIL | PASS |
| prove_ApproveNonZeroAmount | PASS | FAIL | PASS |
| prove_SelfApprovePositiveAmount | PASS | FAIL | PASS |
| prove_TransferFromDoesNotUpdateOtherBalances | PASS | FAIL | PASS |
| proveFail_TransferFromZeroAddressForMSGSender | PASS | FAIL | PASS |
| prove_MsgSenderCanRetrieveOtherBalance | PASS | FAIL | PASS |
| prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed | PASS | FAIL | PASS |
| prove_Mint | PASS | FAIL | PASS |
| proveFail_ApproveZeroAddress | PASS | FAIL | PASS |
| proveFail_TransferToZeroAddress | PASS | FAIL | PASS |
| proveFail_BurnUnderSupply | PASS | FAIL | PASS |
| proveFail_ApproveFromZeroAddress | PASS | FAIL | PASS |
| prove_MultipleTransfersOfZeroAmountAllowed | PASS | FAIL | PASS |
| proveFail_ApproveZeroAddressForMSGSender | PASS | FAIL | PASS |
| prove_TransferDoesNotUpdateOtherBalances | PASS | PASS | PASS |
| prove_BurnZeroTokens | PASS | FAIL | PASS |
| prove_SelfApproveZeroAmountAllowed | PASS | FAIL | PASS |
| prove_MsgSenderCanRetrieveOwnBalance | PASS | FAIL | PASS |
| prove_MsgSenderCanTransferTotalBalance | PASS | FAIL | PASS |
| prove_BurnDifferentAccount | PASS | FAIL | PASS |
| prove_MsgSenderCanTransferTotalBalanceZero | PASS | FAIL | PASS |
| proveFail_TransferFromUnderBalance | PASS | FAIL | PASS |
| prove_ConsecutiveApprovePositiveToPositive | PASS | FAIL | PASS |
| proveFail_BurnFromZeroAddress | PASS | FAIL | PASS |
| prove_MultipleTransferFromAllowed | PASS | FAIL | PASS |
| proveFail_TransferUnderBalance | PASS | FAIL | PASS |
| prove_Transfer | PASS | FAIL | PASS |
| prove_IncreaseAllowance | PASS | FAIL | PASS |
| prove_BalanceUpdatedAfterBurn | PASS | FAIL | PASS |
| prove_ApproveZeroAmount | PASS | FAIL | PASS |
| proveFail_TransferZeroAmountToZeroAddressReverts | PASS | FAIL | PASS |
| proveFail_TransferFromToZeroAddress33 | PASS | FAIL | PASS |
| prove_DecreaseAllowance | PASS | FAIL | PASS |
| prove_ApproveMaxAmount | PASS | FAIL | PASS |
| prove_BurnFromNonZeroAddress | PASS | FAIL | PASS |
| proveFail_TransferFromZeroAmountToZeroAddressReverts | PASS | FAIL | PASS |
| prove_MultipleTransferFromsOfZeroAmountAllowed | PASS | FAIL | PASS |
| proveFail_MintOverflow | PASS | FAIL | PASS |
| proveFail_ApproveToZeroAddress | PASS | FAIL | PASS |



|             | HEVM | KONTROL | HALMOS |
|-------------|---------|---------|---------|
| **Real**    | 21m27s   | 55m29s   | 9,280s  
| **User**    | 32m46s   | 58m43s   | 8,920s 
| **Sys**     | 1m47s   | 2m17s   | 0,407s

---
<br>



<br>

# ERC20 SOLMATE
<br>

[Contract](https://github.com/transmissions11/solmate/blob/main/src/tokens/ERC20.sol)

<br>

## HALMOS

| Function | Status | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Average (s) | Standard Deviation (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| proveFail_ApproveFromZeroAddress | FAIL | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.06 | 0.05 | 0.06 | 0.05 | 0.0 |
| proveFail_ApproveToZeroAddress | FAIL | 0.05 | 0.04 | 0.05 | 0.04 | 0.04 | 0.05 | 0.04 | 0.05 | 0.05 | 0.05 | 0.05 | 0.01 |
| proveFail_ApproveZeroAddress | FAIL | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_ApproveZeroAddressForMSGSender | FAIL | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.05 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| proveFail_BurnFromZeroAddress | PASS | 0.02 | 0.02 | 0.03 | 0.02 | 0.03 | 0.03 | 0.02 | 0.02 | 0.03 | 0.02 | 0.02 | 0.01 |
| proveFail_BurnUnderBalance | PASS | 0.06 | 0.05 | 0.06 | 0.05 | 0.06 | 0.06 | 0.06 | 0.05 | 0.05 | 0.05 | 0.06 | 0.01 |
| proveFail_BurnUnderSupply | PASS | 0.04 | 0.04 | 0.03 | 0.03 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.03 | 0.04 | 0.0 |
| proveFail_MintOverflow | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_MintToZeroAddress | FAIL | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_TransferFromAllowanceReachesZero | PASS | 0.2 | 0.24 | 0.24 | 0.2 | 0.21 | 0.26 | 0.2 | 0.2 | 0.21 | 0.2 | 0.22 | 0.02 |
| proveFail_TransferFromToZeroAddress33 | FAIL | 0.17 | 0.18 | 0.19 | 0.17 | 0.18 | 0.22 | 0.17 | 0.18 | 0.17 | 0.17 | 0.18 | 0.02 |
| proveFail_TransferFromUnderBalance | PASS | 0.09 | 0.09 | 0.09 | 0.08 | 0.09 | 0.1 | 0.1 | 0.09 | 0.1 | 0.09 | 0.09 | 0.01 |
| proveFail_TransferFromUnderBalancei | PASS | 0.06 | 0.06 | 0.06 | 0.06 | 0.07 | 0.07 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |
| proveFail_TransferFromZeroAddress | PASS | 0.04 | 0.03 | 0.04 | 0.03 | 0.04 | 0.03 | 0.04 | 0.03 | 0.04 | 0.03 | 0.04 | 0.01 |
| proveFail_TransferFromZeroAddressForMSGSender | FAIL | 0.21 | 0.22 | 0.21 | 0.21 | 0.22 | 0.23 | 0.22 | 0.22 | 0.22 | 0.21 | 0.22 | 0.01 |
| proveFail_TransferFromZeroAmountToZeroAddressReverts | FAIL | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.11 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.0 |
| proveFail_TransferToZeroAddress | FAIL | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |
| proveFail_TransferUnderBalance | PASS | 0.04 | 0.04 | 0.05 | 0.04 | 0.04 | 0.05 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| proveFail_TransferUnderBalancej | PASS | 0.03 | 0.03 | 0.04 | 0.03 | 0.03 | 0.04 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_TransferZeroAmountToZeroAddressReverts | FAIL | 0.04 | 0.03 | 0.04 | 0.04 | 0.03 | 0.04 | 0.04 | 0.04 | 0.03 | 0.04 | 0.04 | 0.0 |
| prove_AllowanceUpdatedAfterBurn | PASS | 0.06 | 0.07 | 0.07 | 0.06 | 0.07 | 0.07 | 0.07 | 0.06 | 0.07 | 0.07 | 0.07 | 0.0 |
| prove_Approve | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| prove_ApproveMaxAmount | PASS | 0.04 | 0.04 | 0.06 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.01 |
| prove_ApproveNonZeroAmount | PASS | 0.04 | 0.04 | 0.05 | 0.04 | 0.04 | 0.05 | 0.04 | 0.05 | 0.04 | 0.05 | 0.04 | 0.01 |
| prove_ApproveZeroAmount | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_BalanceUpdatedAfterBurn | PASS | 0.12 | 0.11 | 0.12 | 0.12 | 0.11 | 0.13 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.01 |
| prove_BurnDifferentAccount | PASS | 0.11 | 0.11 | 0.12 | 0.12 | 0.11 | 0.13 | 0.11 | 0.11 | 0.12 | 0.11 | 0.12 | 0.01 |
| prove_BurnFromNonZeroAddress | PASS | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.0 |
| prove_BurnSameAccount | PASS | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |
| prove_BurnZeroTokens | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.04 | 0.03 | 0.03 | 0.0 |
| prove_ConsecutiveApprovePositiveToPositive | PASS | 0.05 | 0.05 | 0.06 | 0.05 | 0.06 | 0.05 | 0.05 | 0.05 | 0.06 | 0.05 | 0.05 | 0.0 |
| prove_DecreaseAllowance | PASS | 0.08 | 0.08 | 0.09 | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 | 0.08 | 0.0 |
| prove_IncreaseAllowance | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.08 | 0.09 | 0.07 | 0.08 | 0.07 | 0.07 | 0.07 | 0.01 |
| prove_Mint | PASS | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.06 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.0 |
| prove_MintZeroTokens | PASS | 0.03 | 0.03 | 0.04 | 0.03 | 0.04 | 0.04 | 0.04 | 0.03 | 0.03 | 0.03 | 0.03 | 0.01 |
| prove_MsgSenderCanRetrieveOtherBalance | PASS | 0.05 | 0.03 | 0.04 | 0.03 | 0.04 | 0.04 | 0.04 | 0.03 | 0.04 | 0.03 | 0.04 | 0.01 |
| prove_MsgSenderCanRetrieveOwnBalance | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| prove_MsgSenderCanTransferTotalBalance | PASS | 0.21 | 0.19 | 0.14 | 0.14 | 0.15 | 0.17 | 0.21 | 0.2 | 0.15 | 0.19 | 0.17 | 0.03 |
| prove_MsgSenderCanTransferTotalBalanceZero | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.08 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| prove_MultipleTransferFromAllowed | PASS | 0.25 | 0.24 | 0.3 | 0.31 | 0.32 | 0.39 | 0.25 | 0.24 | 0.31 | 0.24 | 0.28 | 0.05 |
| prove_MultipleTransferFromsOfZeroAmountAllowed | PASS | 0.27 | 0.25 | 0.25 | 0.25 | 0.26 | 0.26 | 0.26 | 0.25 | 0.26 | 0.25 | 0.26 | 0.01 |
| prove_MultipleTransfersAllowed | PASS | 0.21 | 0.2 | 0.2 | 0.2 | 0.23 | 0.21 | 0.2 | 0.2 | 0.21 | 0.2 | 0.21 | 0.01 |
| prove_MultipleTransfersOfZeroAmountAllowed | PASS | 0.14 | 0.14 | 0.14 | 0.14 | 0.15 | 0.15 | 0.14 | 0.14 | 0.14 | 0.14 | 0.14 | 0.0 |
| prove_SelfApproveAndTransferFromOwnAccount | PASS | 0.16 | 0.16 | 0.16 | 0.17 | 0.17 | 0.18 | 0.16 | 0.17 | 0.17 | 0.16 | 0.17 | 0.01 |
| prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed | PASS | 0.12 | 0.11 | 0.11 | 0.11 | 0.11 | 0.12 | 0.11 | 0.11 | 0.11 | 0.12 | 0.11 | 0.0 |
| prove_SelfApprovePositiveAmount | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_SelfApproveZeroAmountAllowed | PASS | 0.04 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.04 | 0.03 | 0.0 |
| prove_SelfTransferPositiveAmountAllowed | PASS | 0.06 | 0.06 | 0.06 | 0.05 | 0.05 | 0.05 | 0.05 | 0.06 | 0.06 | 0.05 | 0.06 | 0.01 |
| prove_SelfTransferZeroAmountAllowed | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_TokenReceiverCanTransferFromTotalBalance | PASS | 0.18 | 0.18 | 0.18 | 0.17 | 0.17 | 0.18 | 0.17 | 0.18 | 0.18 | 0.17 | 0.18 | 0.01 |
| prove_TokenReceiverCanTransferFromTotalBalanceZero | PASS | 0.13 | 0.12 | 0.12 | 0.13 | 0.13 | 0.14 | 0.12 | 0.12 | 0.14 | 0.13 | 0.13 | 0.01 |
| prove_Transfer | PASS | 0.19 | 0.18 | 0.18 | 0.19 | 0.19 | 0.2 | 0.18 | 0.19 | 0.21 | 0.18 | 0.19 | 0.01 |
| prove_TransferDoesNotUpdateOtherBalances | PASS | 0.17 | 0.16 | 0.16 | 0.18 | 0.18 | 0.17 | 0.16 | 0.16 | 0.17 | 0.17 | 0.17 | 0.01 |
| prove_TransferFrom | PASS | 0.16 | 0.15 | 0.15 | 0.16 | 0.16 | 0.16 | 0.15 | 0.15 | 0.16 | 0.17 | 0.16 | 0.01 |
| prove_TransferFromDecreasesAllowance | PASS | 0.16 | 0.14 | 0.15 | 0.15 | 0.14 | 0.15 | 0.15 | 0.14 | 0.16 | 0.15 | 0.15 | 0.01 |
| prove_TransferFromDoesNotUpdateOtherBalances | PASS | 0.21 | 0.21 | 0.21 | 0.21 | 0.21 | 0.19 | 0.2 | 0.2 | 0.2 | 0.21 | 0.2 | 0.01 |
| prove_TransferFromNoFees | PASS | 0.17 | 0.19 | 0.17 | 0.18 | 0.18 | 0.17 | 0.18 | 0.18 | 0.18 | 0.17 | 0.18 | 0.01 |
| prove_TransferFromZeroAmount | PASS | 0.08 | 0.09 | 0.08 | 0.08 | 0.09 | 0.09 | 0.08 | 0.09 | 0.09 | 0.08 | 0.08 | 0.01 |
| prove_TransferZeroAmount | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| prove_ZeroAddressHasNoToken | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |


**Total Tests Done:** 61
**Total Tests Passed:** 51
**Total Failed Tests** 10

**TOTAL TIME**

|             | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Average | Standard Deviation |
|-------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|------------|---------|---------------|
| **Real**    | 0m6,645s   | 0m6,601s   | 0m6,601s   | 0m6,519s   | 0m6,660s   | 0m7,007s   | 0m6,472s   | 0m6,553s   | 0m6,673s   | 0m6,487s   | 6,652s  | 0,164s        |
| **User**    | 0m6,998s   | 0m7,061s   | 0m7,061s   | 0m6,968s   | 0m7,154s   | 0m7,460s   | 0m6,929s   | 0m6,993s   | 0m7,150s   | 0m6,918s   | 7,069s  | 0,154s        |
| **Sys**     | 0m0,351s   | 0m0,309s   | 0m0,309s   | 0m0,308s   | 0m0,295s   | 0m0,327s   | 0m0,283s   | 0m0,301s   | 0m0,324s   | 0m0,321s   | 0,313s  | 0,018s        |


<br>

<br>

## HEVM

| Function | Status |
|--------|--------|
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
| proveFail_MintToZeroAddress | FAIL |
| prove_ApproveNonZeroAmount | PASS |
| prove_SelfApprovePositiveAmount | PASS |
| prove_TransferFromDoesNotUpdateOtherBalances | PASS |
| proveFail_TransferFromZeroAddressForMSGSender | FAIL |
| prove_MsgSenderCanRetrieveOtherBalance | PASS |
| prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed | PASS |
| prove_Mint | PASS |
| proveFail_ApproveZeroAddress | FAIL |
| proveFail_TransferToZeroAddress | FAIL |
| proveFail_BurnUnderSupply | PASS |
| proveFail_ApproveFromZeroAddress | FAIL |
| prove_MultipleTransfersOfZeroAmountAllowed | PASS |
| proveFail_ApproveZeroAddressForMSGSender | FAIL |
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
| proveFail_TransferZeroAmountToZeroAddressReverts | FAIL |
| proveFail_TransferFromToZeroAddress33 | FAIL |
| prove_DecreaseAllowance | PASS |
| prove_ApproveMaxAmount | PASS |
| prove_BurnFromNonZeroAddress | PASS |
| proveFail_TransferFromZeroAmountToZeroAddressReverts | FAIL |
| prove_MultipleTransferFromsOfZeroAmountAllowed | PASS |
| proveFail_MintOverflow | PASS |
| proveFail_ApproveToZeroAddress | FAIL |

**Total Tests Done:** 61
**Total Tests Passed:** 51
**Total Failed Tests** 10


**TOTAL TIME**
|             | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Average | Standard Deviation |
|-------------|--------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|-------------|----------|---------------|
| **Real**    | 21m38,592s   | 23m0,848s   | 22m8,266s   | 21m37,697s  | 21m34,877s  | 21m37,330s  | 21m42,767s  | 21m34,641s  | 21m34,435s  | 21m38,335s  | 21m47,079s | 0,611s        |
| **User**    | 25m45,521s   | 27m9,238s   | 26m31,884s  | 25m49,557s  | 25m35,977s  | 25m43,637s  | 25m51,187s  | 25m35,093s  | 25m39,768s  | 25m43,650s  | 25m52,451s | 0,632s        |
| **Sys**     | 1m51,120s    | 1m53,997s   | 1m50,339s   | 1m55,508s   | 1m50,636s   | 1m47,435s   | 1m50,812s   | 1m47,138s   | 1m48,226s   | 1m48,253s   | 1m50,546s | 0,462s        |

<br>

<br>

## KONTROL


| Function | Status |
|--------|--------|
| prove_MultipleTransferFromsOfZeroAmountAllowed | FAIL |
| prove_MsgSenderCanTransferTotalBalance | FAIL |
| prove_TransferDoesNotUpdateOtherBalances | PASS |
| proveFail_TransferFromUnderBalancei | FAIL |
| proveFail_TransferFromZeroAddress | FAIL |
| prove_Approve | FAIL |
| prove_ApproveMaxAmount | FAIL |
| prove_TransferFromDecreasesAllowance | FAIL |
| proveFail_ApproveFromZeroAddress | PASS |
| proveFail_BurnFromZeroAddress | FAIL |
| proveFail_ApproveZeroAddress | PASS |
| prove_BalanceUpdatedAfterBurn | FAIL |
| proveFail_BurnUnderBalance | FAIL |
| prove_TokenReceiverCanTransferFromTotalBalance | FAIL |
| prove_TransferFromZeroAmount | FAIL |
| prove_DecreaseAllowance | FAIL |
| prove_SelfApproveZeroAmountAllowed | FAIL |
| prove_ConsecutiveApprovePositiveToPositive | FAIL |
| prove_TransferFromNoFees | FAIL |
| prove_ZeroAddressHasNoToken | PASS |
| prove_MultipleTransferFromAllowed | FAIL |
| prove_SelfApprovePositiveAmount | FAIL |
| prove_SelfTransferPositiveAmountAllowed | FAIL |
| prove_BurnDifferentAccount | FAIL |
| prove_Mint | FAIL |
| prove_IncreaseAllowance | FAIL |
| prove_MsgSenderCanTransferTotalBalanceZero | FAIL |
| prove_Transfer | FAIL |
| proveFail_TransferFromZeroAddressForMSGSender | FAIL |
| proveFail_TransferFromZeroAmountToZeroAddressReverts | PASS |
| proveFail_TransferFromUnderBalance | FAIL |
| prove_AllowanceUpdatedAfterBurn | FAIL |
| prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed | FAIL |
| proveFail_TransferUnderBalance | FAIL |
| prove_BurnSameAccount | FAIL |
| prove_MsgSenderCanRetrieveOwnBalance | PASS |
| prove_SelfTransferZeroAmountAllowed | FAIL |
| proveFail_MintToZeroAddress | PASS |
| prove_MultipleTransfersAllowed | FAIL |
| proveFail_TransferFromZeroAddress | FAIL |
| proveFail_TransferZeroAmountToZeroAddressReverts | PASS |
| prove_TransferFromDoesNotUpdateOtherBalances | FAIL |
| prove_BurnFromNonZeroAddress | FAIL |
| proveFail_TransferUnderBalancej | FAIL |
| proveFail_ApproveZeroAddressForMSGSender | PASS |
| prove_ApproveNonZeroAmount | FAIL |
| proveFail_TransferFromToZeroAddress33 | FAIL |
| prove_ApproveZeroAmount | FAIL |
| prove_MintZeroTokens | FAIL |
| proveFail_BurnUnderSupply | FAIL |
| proveFail_MintOverflow | FAIL |
| prove_MultipleTransfersOfZeroAmountAllowed | FAIL |
| prove_BurnZeroTokens | FAIL |
| proveFail_TransferFromAllowanceReachesZero | FAIL |
| prove_MsgSenderCanRetrieveOtherBalance | FAIL |
| prove_SelfApproveAndTransferFromOwnAccount | FAIL |
| prove_TokenReceiverCanTransferFromTotalBalanceZero | FAIL |
| prove_TransferFrom | FAIL |
| proveFail_TransferToZeroAddress | PASS |
| prove_TransferZeroAmount | FAIL |
| proveFail_ApproveToZeroAddress | PASS |

**Total Tests Done:** 61
**Total Tests Passed:** 11
**Total Failed Tests:** 50

**TOTAL TIME**
|             | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Average | Standard Deviation |
|-------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|--------------|-------------|---------------|
| **Real**    | 42m15,179s   | 43m0,117s    | 43m19,468s   | 44m53,700s   | 45m7,123s    | 46m24,987s   | 42m44,101s   | 46m11,672s   | 43m48,280s   | 44m5,625s   | 1m27,442s     |
| **User**    | 45m15,201s   | 46m10,402s   | 46m10,077s   | 47m59,965s   | 48m15,282s   | 49m49,290s   | 45m44,038s   | 49m20,384s   | 46m41,195s   | 47m27,203s  | 1m43,523s     |
| **Sys**     | 1m23,158s    | 1m24,728s    | 1m25,929s    | 1m30,122s    | 1m32,102s    | 1m33,077s    | 1m24,698s    | 1m30,315s    | 1m26,756s    | 1m27,764s   | 0m3,553s      |

<br>

<br>

## GENERAL COMPARISION

| Function | HEVM Status | Kontrol Status | Halmos Status |
|--------|-------------|----------------|---------------|
| proveFail_TransferUnderBalancej | PASS | FAIL | PASS |
| prove_ZeroAddressHasNoToken | PASS | PASS | PASS |
| prove_TokenReceiverCanTransferFromTotalBalance | PASS | FAIL | PASS |
| prove_TransferFromNoFees | PASS | FAIL | PASS |
| prove_MintZeroTokens | PASS | FAIL | PASS |
| proveFail_TransferFromUnderBalancei | PASS | FAIL | PASS |
| prove_TransferZeroAmount | PASS | FAIL | PASS |
| prove_TokenReceiverCanTransferFromTotalBalanceZero | PASS | FAIL | PASS |
| prove_AllowanceUpdatedAfterBurn | PASS | FAIL | PASS |
| prove_Approve | PASS | FAIL | PASS |
| prove_SelfApproveAndTransferFromOwnAccount | PASS | FAIL | PASS |
| prove_SelfTransferZeroAmountAllowed | PASS | FAIL | PASS |
| prove_TransferFromDecreasesAllowance | PASS | FAIL | PASS |
| prove_BurnSameAccount | PASS | FAIL | PASS |
| prove_TransferFrom | PASS | FAIL | PASS |
| prove_TransferFromZeroAmount | PASS | FAIL | PASS |
| proveFail_TransferFromZeroAddress | PASS | FAIL | PASS |
| prove_SelfTransferPositiveAmountAllowed | PASS | FAIL | PASS |
| proveFail_BurnUnderBalance | PASS | FAIL | PASS |
| proveFail_TransferFromAllowanceReachesZero | PASS | FAIL | PASS |
| prove_MultipleTransfersAllowed | PASS | FAIL | PASS |
| proveFail_MintToZeroAddress | FAIL | PASS | FAIL |
| prove_ApproveNonZeroAmount | PASS | FAIL | PASS |
| prove_SelfApprovePositiveAmount | PASS | FAIL | PASS |
| prove_TransferFromDoesNotUpdateOtherBalances | PASS | FAIL | PASS |
| proveFail_TransferFromZeroAddressForMSGSender | FAIL | FAIL | FAIL |
| prove_MsgSenderCanRetrieveOtherBalance | PASS | FAIL | PASS |
| prove_SelfApproveAndTransferFromOwnAccountZeroAmountAllowed | PASS | FAIL | PASS |
| prove_Mint | PASS | FAIL | PASS |
| proveFail_ApproveZeroAddress | FAIL | PASS | FAIL |
| proveFail_TransferToZeroAddress | FAIL | PASS | FAIL |
| proveFail_BurnUnderSupply | PASS | FAIL | PASS |
| proveFail_ApproveFromZeroAddress | FAIL | PASS | FAIL |
| prove_MultipleTransfersOfZeroAmountAllowed | PASS | FAIL | PASS |
| proveFail_ApproveZeroAddressForMSGSender | FAIL | PASS | FAIL |
| prove_TransferDoesNotUpdateOtherBalances | PASS | PASS | PASS |
| prove_BurnZeroTokens | PASS | FAIL | PASS |
| prove_SelfApproveZeroAmountAllowed | PASS | FAIL | PASS |
| prove_MsgSenderCanRetrieveOwnBalance | PASS | PASS | PASS |
| prove_MsgSenderCanTransferTotalBalance | PASS | FAIL | PASS |
| prove_BurnDifferentAccount | PASS | FAIL | PASS |
| prove_MsgSenderCanTransferTotalBalanceZero | PASS | FAIL | PASS |
| proveFail_TransferFromUnderBalance | PASS | FAIL | PASS |
| prove_ConsecutiveApprovePositiveToPositive | PASS | FAIL | PASS |
| proveFail_BurnFromZeroAddress | PASS | FAIL | PASS |
| prove_MultipleTransferFromAllowed | PASS | FAIL | PASS |
| proveFail_TransferUnderBalance | PASS | FAIL | PASS |
| prove_Transfer | PASS | FAIL | PASS |
| prove_IncreaseAllowance | PASS | FAIL | PASS |
| prove_BalanceUpdatedAfterBurn | PASS | FAIL | PASS |
| prove_ApproveZeroAmount | PASS | FAIL | PASS |
| proveFail_TransferZeroAmountToZeroAddressReverts | FAIL | PASS | FAIL |
| proveFail_TransferFromToZeroAddress33 | FAIL | FAIL | FAIL |
| prove_DecreaseAllowance | PASS | FAIL | PASS |
| prove_ApproveMaxAmount | PASS | FAIL | PASS |
| prove_BurnFromNonZeroAddress | PASS | FAIL | PASS |
| proveFail_TransferFromZeroAmountToZeroAddressReverts | FAIL | PASS | FAIL |
| prove_MultipleTransferFromsOfZeroAmountAllowed | PASS | FAIL | PASS |
| proveFail_MintOverflow | PASS | FAIL | PASS |
| proveFail_ApproveToZeroAddress | FAIL | PASS | FAIL |

|             | HEVM | KONTROL | HALMOS |
|-------------|---------|---------|---------|
| **Real**    | 21m47s | 44m50s   | 6,652s 
| **User**    | 25m52s  | 47m27s   | 7,069s 
| **Sys**     | 1m51s   | 1m27s   | 0,313s
<br>

<br>

**ATTENTION**

After using the halmos and hevm counterexamples in tests to check the reliability of the answers, 9 of the 10 failed tests turned out to be actually wrong. The test that passed actually has the vulnerability detected by the tools, however, when applying the test, underflow occurs and the test reverts, which was missed.


    Encountered 9 failing tests in test/verifyresults.t.sol:ERC20SymbolicProperties
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xe41cadce00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0]] testproveFail_ApproveFromZeroAddress(address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0x0b609fcb00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0]] testproveFail_ApproveToZeroAddress(address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xa56a12e400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0]] testproveFail_ApproveZeroAddress(address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0x7b9f0c0e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0]] testproveFail_ApproveZeroAddressForMSGSender(address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xeee61faa0000000000000000000000000000000000000000000000000000000000000000 args=[0]] testproveFail_MintToZeroAddress(uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xb664c1be000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0x0000000000000000000000000000000000000000, 0]] testproveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xdb4ad5a500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0x0000000000000000000000000000000000000000]] testproveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xfe544ff200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0]] testproveFail_TransferToZeroAddress(address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0x5264851c0000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000]] testproveFail_TransferZeroAmountToZeroAddressReverts(address) (runs: 0, μ: 0, ~: 0)

    Encountered a total of 9 failing tests, 1 tests succeeded
<br>

<br>

When commenting this line: `if (allowed != type(uint256).max) allowance[from][msg.sender] = allowed - amount`, the results are confirmed:

    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xe41cadce00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0]] testproveFail_ApproveFromZeroAddress(address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0x0b609fcb00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0]] testproveFail_ApproveToZeroAddress(address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xa56a12e400000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0]] testproveFail_ApproveZeroAddress(address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0x7b9f0c0e00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0]] testproveFail_ApproveZeroAddressForMSGSender(address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xeee61faa0000000000000000000000000000000000000000000000000000000000000000 args=[0]] testproveFail_MintToZeroAddress(uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0x50c4269d000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0x0000000000000000000000000000000000000000, 0]] testproveFail_TransferFromToZeroAddress33(address,address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xb664c1be000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0x0000000000000000000000000000000000000000, 0]] testproveFail_TransferFromZeroAddressForMSGSender(address,address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xdb4ad5a500000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0x0000000000000000000000000000000000000000]] testproveFail_TransferFromZeroAmountToZeroAddressReverts(address,address) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0xfe544ff200000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0]] testproveFail_TransferToZeroAddress(address,uint256) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0x5264851c0000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000]] testproveFail_TransferZeroAmountToZeroAddressReverts(address) (runs: 0, μ: 0, ~: 0)

    Encountered a total of 10 failing tests, 0 tests succeeded

This demonstrates the difference in behavior between Formal Verification and unit testing/fuzzing.

---
<br>



<br>

# ERC721 FOUNDRY

<br>

Foundry's standard implementation of ERC721

<br>


## HALMOS

| Function | Status | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Average (s) | Standard Deviation (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| proveFail_ApproveWhenIdHasNotAnOwner | PASS | 0.04 | 0.04 | 0.05 | 0.04 | 0.03 | 0.03 | 0.04 | 0.04 | 0.04 | 0.03 | 0.04 | 0.01 |
| prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| proveFail_ApproveWhenIsNotApprovedForAll | PASS | 0.07 | 0.07 | 0.08 | 0.07 | 0.07 | 0.07 | 0.08 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| prove_ApproveWhenOwnerEqualsMSGSender | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_Burn | PASS | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.06 | 0.05 | 0.05 | 0.05 | 0.0 |
| proveFail_Burn | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| prove_Mint | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| proveFail_MintWhenToIsAddressZero | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| prove_safeTransferFrom | FAIL | 0.12 | 0.1 | 0.11 | 0.1 | 0.11 | 0.1 | 0.11 | 0.1 | 0.1 | 0.1 | 0.11 | 0.01 |
| prove_setApprovalForAll | PASS | 0.02 | 0.03 | 0.03 | 0.03 | 0.02 | 0.02 | 0.02 | 0.03 | 0.02 | 0.03 | 0.03 | 0.01 |
| proveFail_setApprovalForAll | FAIL | 0.03 | 0.04 | 0.04 | 0.03 | 0.03 | 0.03 | 0.04 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| prove_transferFrom | PASS | 0.12 | 0.12 | 0.13 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.0 |
| proveFail_transferFromWhenFromIsNotTheOwner | PASS | 0.02 | 0.03 | 0.03 | 0.03 | 0.02 | 0.02 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_transferFromWhenToIsAddressZero | PASS | 0.06 | 0.06 | 0.07 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |

**Total Tests Done:** 14
**Total Tests Passed:** 12
**Total Failed Tests:** 2

<br>

<br>

## HEVM

| Function | Status |
|--------|--------|
| prove_safeTransferFrom | FAIL |
| proveFail_MintWhenToIsAddressZero | PASS |
| prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender | PASS |
| proveFail_transferFromWhenToIsAddressZero | PASS |
| prove_Burn | PASS |
| proveFail_Burn | PASS |
| prove_Mint | PASS |
| proveFail_ApproveWhenIdHasNotAnOwner | FAIL |
| proveFail_setApprovalForAll | FAIL |
| prove_setApprovalForAll | PASS |
| proveFail_ApproveWhenIsNotApprovedForAll | PASS |
| proveFail_transferFromWhenFromIsNotTheOwner | PASS |
| prove_transferFrom | PASS |
| prove_ApproveWhenOwnerEqualsMSGSender | PASS |

**Total Tests Done:** 14
**Total Tests Passed:** 11
**Total Failed Tests:** 3

<br>

<br>

## GENERAL COMPARISION

| Function | HEVM Status | Halmos Status |
|--------|-------------|---------------|
| prove_safeTransferFrom | FAIL | FAIL |
| proveFail_MintWhenToIsAddressZero | PASS | PASS |
| prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender | PASS | PASS |
| proveFail_transferFromWhenToIsAddressZero | PASS | PASS |
| prove_Burn | PASS | PASS |
| proveFail_Burn | PASS | PASS |
| prove_Mint | PASS | PASS |
| proveFail_ApproveWhenIdHasNotAnOwner | FAIL | PASS |
| proveFail_setApprovalForAll | FAIL | FAIL |
| prove_setApprovalForAll | PASS | PASS |
| proveFail_ApproveWhenIsNotApprovedForAll | PASS | PASS |
| proveFail_transferFromWhenFromIsNotTheOwner | PASS | PASS |
| prove_transferFrom | PASS | PASS |
| prove_ApproveWhenOwnerEqualsMSGSender | PASS | PASS |
<br>

<br>

**ATTENTION**

By using the counterexamples of halmos and hevm on the failed tests, interesting results are obtained. Both tests that failed on both Hevm and Halmos actually demonstrate failure. However, Hevm was wrong to demonstrate failure in the `proveFail_ApproveWhenIdHasNotAnOwner` test, which, at least by counterexample, the test does not revert.

    [PASS] testproveFail_ApproveWhenIdHasNotAnOwner() (gas: 13399)
    [FAIL. Reason: call did not revert as expected; counterexample: calldata=0x467c6291000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000 args=[0x0000000000000000000000000000000000000000, 0x0000000000000000000000000000000000000000, false]] testproveFail_setApprovalForAllFuzz(address,address,bool) (runs: 0, μ: 0, ~: 0)
    [FAIL. Reason: panic: assertion failed (0x01); counterexample: calldata=0x298636950000000000000000000000001804c8ab1f12e6bbf3894d4083f33e07309d1f380000000000000000000000000000000000000000000000000000000000001aaa args=[0x1804c8AB1F12E6bbf3894d4083f33e07309d1f38, 6826]] testprove_safeTransferFromFuzz(address,uint256) (runs: 0, μ: 0, ~: 0)
    Suite result: FAILED. 1 passed; 2 failed; 0 skipped; finished in 26.17ms (46.99ms CPU time)

---
<br>



<br>

# ERC721 SOLMATE

<br>

<br>

## HALMOS

| Function | Status | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Time 11 | Average (s) | Standard Deviation (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| proveFail_ApproveWhenIdHasNotAnOwner | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| proveFail_ApproveWhenIsNotApprovedForAll | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.08 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.0 |
| proveFail_BurnReverts | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| proveFail_MintWhenToIsAddressZero | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| proveFail_setApprovalForAll | FAIL | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| proveFail_transferFromWhenFromIsNotTheOwner | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |
| proveFail_transferFromWhenToIsAddressZero | PASS | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |
| prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender | PASS | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.07 | 0.08 | 0.07 | 0.0 |
| prove_ApproveWhenOwnerEqualsMSGSender | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_Burn | PASS | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.0 |
| prove_Mint | PASS | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_safeTransferFrom | FAIL | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.0 |
| prove_setApprovalForAll | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| prove_transferFrom | PASS | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.12 | 0.0 |

**Total Tests Done:** 14
**Total Tests Passed:** 12
**Total Failed Tests:** 2

<br>

<br>

## HEVM

| Function | Status |
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

**Total Tests Done:** 14
**Total Tests Passed:** 10
**Total Failed Tests:** 4
<br>

<br>

## GENERAL COMPARISION

| Função | HEVM Status | Halmos Status |
|--------|-------------|---------------|
| prove_safeTransferFrom | FAIL | FAIL |
| prove_ApproveWhenIsApprovedForAllOnwerDifferentFromMSGSender | PASS | PASS |
| proveFail_transferFromWhenFromIsNotTheOwner | FAIL | PASS |
| proveFail_ApproveWhenIdHasNotAnOwner | FAIL | PASS |
| prove_Burn | PASS | PASS |
| proveFail_ApproveWhenIsNotApprovedForAll | PASS | PASS |
| proveFail_setApprovalForAll | FAIL | FAIL |
| prove_Mint | PASS | PASS |
| proveFail_transferFromWhenToIsAddressZero | PASS | PASS |
| proveFail_MintWhenToIsAddressZero | PASS | PASS |
| proveFail_Burn | PASS | PASS |
| prove_setApprovalForAll | PASS | PASS |
| prove_transferFrom | PASS | PASS |
| prove_ApproveWhenOwnerEqualsMSGSender | PASS | PASS |

---
<br>



<br>

# ERC1155 OPEN ZEPPELIN

<br>

<br>

## HALMOS

| Function | Status | Time 1 | Time 2 | Time 3 | Time 4 | Time 5 | Time 6 | Time 7 | Time 8 | Time 9 | Time 10 | Time 11 | Time 12 | Time 13 | Average (s) | Standard Deviation (s) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| proveFail_burnBalanceLessThanAmount | PASS | 0.05 | 0.05 | 0.05 | 0.05 | 0.06 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.05 | 0.06 | 0.05 | 0.05 | 0.0 |
| proveFail_burnZeroAddress | PASS | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| proveFail_mintZeroAddress | PASS | 0.01 | 0.01 | 0.02 | 0.02 | 0.01 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01 | 0.0 |
| proveFail_safeTransferFromBalanceLessThanAmount | PASS | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.07 | 0.07 | 0.06 | 0.06 | 0.06 | 0.0 |
| proveFail_safeTransferFromWhenSenderIsNotApprovedForAll | PASS | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.05 | 0.06 | 0.06 | 0.06 | 0.0 |
| proveFail_safeTransferFromWhenSenderIsNotMSGSender | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| proveFail_safeTransferFromZeroAddressForFrom | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| proveFail_safeTransferFromZeroAddressForTo | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| proveFail_setApprovalForAllSenderEqualsOperator | PASS | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.0 |
| prove_burn | PASS | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.0 |
| prove_mint | PASS | 0.05 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.04 | 0.0 |
| prove_safeBatchTransferFrom | PASS | 0.37 | 0.37 | 0.37 | 0.38 | 1.57 | 0.37 | 0.37 | 0.37 | 0.39 | 0.37 | 0.38 | 0.37 | 1.4 | 0.54 | 0.42 |
| prove_safeTransferFrom | PASS | 0.11 | 0.11 | 0.1 | 0.11 | 0.11 | 0.1 | 0.11 | 0.11 | 0.11 | 0.11 | 0.11 | 0.11 | 0.11 | 0.11 | 0.0 |
| prove_setApprovalForAll | PASS | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.03 | 0.0 |

**Total Tests Done:** 14
**Total Tests Passed:** 14
**Total Failed Tests:** 0
<br>

<br>

## HEVM
| Function | Status |
|--------|--------|
| proveFail_burnZeroAddress | PASS |
| proveFail_setApprovalForAllSenderEqualsOperator | PASS |
| proveFail_mintZeroAddress | PASS |
| proveFail_burnBalanceLessThanAmount | ERROR |
| proveFail_safeTransferFromWhenSenderIsNotMSGSender | FAIL |
| prove_mint | ERROR |
| proveFail_safeTransferFromWhenSenderIsNotApprovedForAll | PASS |
| prove_safeBatchTransferFrom | ERROR |
| prove_safeTransferFrom | PASS |
| prove_burn | PASS |
| proveFail_safeTransferFromBalanceLessThanAmount | ERROR |
| proveFail_safeTransferFromZeroAddressForTo | PASS |
| prove_setApprovalForAll | PASS |
| proveFail_safeTransferFromZeroAddressForFrom | PASS |

**Total Tests Done:** 14
**Total Tests Passed:** 9
**Total Failed Tests:** 1

Hevm was unable to complete some tests, the ram memory exceeded its limit during execution and the program crashed.

<br>

<br>

# ERC1155 SOLMATE
<br>

[Contract](https://github.com/transmissions11/solmate/blob/main/src/tokens/ERC1155.sol)

<br>

## HALMOS

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

**Total Tests Done:** 14
**Total Tests Passed:** 12
**Total Failed Tests:** 2

<br>

<br>

## HEVM

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

**Total Tests Done:** 14
**Total Tests Passed:** 10
**Total Failed Tests:** 3

Hevm was unable to complete all the tests. The program crashed during `prove_safeBatchTransferFrom` test

    hevm: Internal Error: TODO: symbolic abi encoding for uint256[] -- CallStack (from HasCallStack):
    internalError, called at src/EVM/SymExec.hs:140:8 in hevm-0.53.0-BdoApfgEeNQEfgvlRGZ9gm:EVM.SymExec
    CallStack (from HasCallStack):
    error, called at src/EVM/Types.hs:1356:19 in hevm-0.53.0-BdoApfgEeNQEfgvlRGZ9gm:EVM.Types
    internalError, called at src/EVM/SymExec.hs:140:8 in hevm-0.53.0-BdoApfgEeNQEfgvlRGZ9gm:EVM.SymExec

<br>

<br>

## GENERAL COMPARISION

| Function | HEVM Status | Halmos Status |
|--------|-------------|---------------|
| proveFail_burnZeroAddress | FAIL | FAIL |
| proveFail_setApprovalForAllSenderEqualsOperator | FAIL | FAIL |
| proveFail_mintZeroAddress | PASS | PASS |
| proveFail_burnBalanceLessThanAmount | PASS | PASS |
| proveFail_safeTransferFromWhenSenderIsNotMSGSender | FAIL | PASS |
| prove_mint | PASS | PASS |
| proveFail_safeTransferFromWhenSenderIsNotApprovedForAll | PASS | PASS |
| prove_safeTransferFrom | PASS | PASS |
| prove_burn | PASS | PASS |
| proveFail_safeTransferFromBalanceLessThanAmount | PASS | PASS |
| proveFail_safeTransferFromZeroAddressForTo | PASS | PASS |
| prove_setApprovalForAll | PASS | PASS |
| proveFail_safeTransferFromZeroAddressForFrom | PASS | PASS |
| prove_safeBatchTransferFrom | ERROR | PASS |

---
<br>

<br>

# ERC4626
<br>

In both solmate and open zeppelin contracts, neither tool was able to complete the tests. Probably due to non-linear arithmetic, which z3 is bad with.

<br>