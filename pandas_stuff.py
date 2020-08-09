import pandas as pd

data = {
    "header 1" : [3, 2, 0, 1],
    "header 2" : [0, 3, 7, 2]
}

purchases = pd.DataFrame(data, index=["June", "Robert", "Lily", "David"])

# locate order by name
June_order = purchases.loc["June"]
print(purchases)
print()
print(June_order)