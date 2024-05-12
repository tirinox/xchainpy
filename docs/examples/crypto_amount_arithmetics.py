from xchainpy2_utils.amount import CryptoAmount
from xchainpy2_utils.asset import AssetRUNE, AssetETH

amount1 = CryptoAmount.automatic(100, AssetRUNE)
amount2 = CryptoAmount.automatic(200, AssetRUNE)

# Addition
result = amount1 + amount2
print(result.amount)  # 300

# Subtraction
result = amount2 - amount1
print(result.amount)  # 100

# Multiplication
result = amount1 * 2
print(result.amount)  # 200

# Division
result = amount2 / 2
print(result.amount)  # 100

# Comparison
print(amount1 == amount2)  # False
print(amount1 < amount2)  # True
print(amount1 > amount2)  # False

amount_bnb = CryptoAmount.automatic(100, AssetETH)
try:
    result = amount1 + amount_bnb
except ValueError as e:
    print(e)
