import pandas as pd

data_notebook = {
    "OrderID": [1, 2, 3, 4, 5],
    "Product": ["Apple", "Banana", "Milk", "Eggs", "Bread"],
    "Price": [100, 40, 50, 5, 30],
    "Quantity": [5, 10, 20, 50, 15]
}


df = pd.DataFrame(data_notebook)
print(df)
# Select row by label (index 2 → Milk)
print(df.loc[2])

# Select multiple rows
print(df.loc[[0, 3]])

# Select row & specific columns
print(df.loc[0:2, ["Product", "Price"]])
# Select first row
print(df.iloc[0])

# Select first 3 rows
print(df.iloc[0:3])

# Select first 2 rows & first 2 columns
print(df.iloc[0:2, 0:2])

# Select last row
print(df.iloc[-1])
# Filter rows where Quantity > 10
print(df.query("Quantity > 10"))

# Multiple conditions with AND (&) and OR (|)
print(df.query("Price > 30 & Quantity > 10"))

# OR condition
print(df.query("Product == 'Apple' | Product == 'Bread'"))
# Sort by Price (ascending)
print(df.sort_values(by="Price"))

# Sort by Quantity (descending)
print(df.sort_values(by="Quantity", ascending=False))
# Sort by Price ascending, then Quantity descending
print(df.sort_values(by=["Price", "Quantity"], ascending=[True, False]))
top_products = df.query("Quantity > 10").sort_values(by="Price", ascending=False).head(3)
print(top_products)


