
"""server_log =("192.168.1.12",20)

def process_log(log_file):
    info_count =0
    warning_count =0
    error_count =0
    
    with open(log_file ,"r")as file:
        log =file.readlines()

    error_log =list(filter(lambda line: "ERROR" in line,log))
    warning_log =list(filter(lambda line: "WARNING" in line,log))
    info_log =list(filter(lambda line: "INFO" in line,log))

    error_count =len(error_log)
    info_count =len(info_log)
    warning_count =len(warning_log)
    
    return {
        "server": server_log,
        "ERROR" : error_count,
        "INFO" : info_count,
        "WARNING": warning_count
    }

def export_summary(summary,output_file):
    with open(output_file,"w") as file:
        file.write(f"summary of {summary['server'][0]}:{summary['server'][1]}\n")
        file.write(f"=======================")
        file.write(f"{summary['ERROR']}\n")
        file.write(f"{summary['INFO']}\n")
        file.write(f"{summary['WARNING']}\n")
    print(f"summary exported to {output_file}")



if __name__ == "__main__":

    log_file ="server.log"
    output_file ="summary.txt"

    summary = process_log(log_file)
    print(summary)

    export_summary(summary,output_file)
"""
"""
# 1️⃣ Fixed Configuration with TUPLE (IP, PORT) - Immutable
server_config = ("192.168.1.10", 22)

def process_logs(file_path):
    # 2️⃣ Local Scope Counters
    error_count = 0
    warning_count = 0
    info_count = 0
    
    with open(file_path, "r") as file:
        logs = file.readlines()

    # 3️⃣ Use Lambda for Quick Filtering
    error_logs = list(filter(lambda line: "ERROR" in line, logs))  
    warning_logs = list(filter(lambda line: "WARNING" in line, logs))
    info_logs = list(filter(lambda line: "INFO" in line, logs))
    
    # Local scope updating counts
    error_count = len(error_logs)
    warning_count = len(warning_logs)
    info_count = len(info_logs)
    
    # Returning summary as dict
    return {
        "Server": server_config,
        "ERROR": error_count,
        "WARNING": warning_count,
        "INFO": info_count
    }


def export_summary(summary, output_file):
    # Writing summary to output file
    with open(output_file, "w") as file:
        file.write(f"Summary for Server {summary['Server'][0]}:{summary['Server'][1]}\n")
        file.write("=======================================\n")
        file.write(f"ERROR: {summary['ERROR']}\n")
        file.write(f"WARNING: {summary['WARNING']}\n")
        file.write(f"INFO: {summary['INFO']}\n")
    print(f"Summary exported to {output_file}")


if __name__ == "__main__":
    # Global scope file paths
    log_file = "server.log"
    output_file = "summary.txt"
    
    # Process logs & export
    summary = process_logs(log_file)
    print(summary)
    export_summary(summary, output_file)
"""
"""
server_log =("192.168.1.64",8080)

def process_log(log_file):

    info_count =0
    error_count =0
    warning_count =0

    with open(log_file,"r") as file:
        log =file.readlines()

        info_log =list(filter(lambda line: "INFO" in line ,log))
        error_log =list(filter(lambda line : "ERROR" in line ,log))
        warning_log =list(filter(lambda line: "WARNING" in line ,log))

        info_count =len(info_log)
        error_count =len(error_log)
        warning_count =len(warning_log)

        return {
            "Server" : server_log,
            "ERROR" : error_count,
            "INFO" : info_count,
            "WARNING" : warning_count
        }

def export_summary(summary,output_file):
    with open(output_file, "w") as file:
      file.write(f" summary of server {summary ['Server'][0]} : {summary ['Server'][1]}\n")
      file.write(f" {summary ['INFO']} \n")
      file.write(f" { summary ['ERROR']}\n")
      file.write(f" { summary ['WARNING']}\n")
    print(f" summary of server has been written in {output_file} file\n")  


if __name__ == "__main__":
    log_file ="server.log"
    output_file ="summary.txt"

    summary =process_log(log_file)
    print(summary)
    export_summary(summary,output_file)
"""
"""
pip uninstall numpy
pip uninstall python-dateutil
pip uninstall pytz

"""
"""
import csv

log_summary =[
    {"Server" :"192.168.13.3" ,"ERROR" :3,"INFO": 41,"WARNING" :13},
    {"Server" :"192.168.13.3" ,"ERROR" :6,"INFO": 17,"WARNING" :21}
]

with open('summary.csv' ,mode="w", newline='') as file:
    writer =csv.DictReader(file ,fieldnames =["Server" ,"ERROR","INFO","WARNING"])
    writer.writeheader()
    writer.writerows(log_summary)

    print(f"sucessfully printed summary.csv file !")
    """
"""
import csv

# Sample data: Logs summary
log_summary = [
    {"Server": "192.168.1.1", "ERROR": 4, "WARNING": 24, "INFO": 15},
    {"Server": "192.168.1.21", "ERROR": 9, "WARNING": 11, "INFO": 20}
]

with open('summary.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Server", "ERROR", "WARNING", "INFO"])
    writer.writeheader()  # Writes the header row
    writer.writerows(log_summary)  # Writes all data rows at once

with open('summary.csv', mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Server", "ERROR", "WARNING", "INFO"])
    writer.writeheader()  # Writes the header row
    writer.writerows(log_summary)
   

print("CSV file written successfully.")
with  open('summary.csv' ,mode="r") as file:
    reader =csv.DictReader(file)
    for row in file:
        print(row)

import pandas as pd

DATA ={
    "server" : ["192.168.1.10" ,"192.168.1.11"],
    "ERROR" : [4,5],
    "INFO" : [12,16],
    "WARNING" : [5,6]
}

df =pd.DataFrame(DATA)

df.to_csv("pd_summary.csv", index =False)
df_read =pd.read_csv("pd_summary.csv")

print(df_read)

"""
"""
with open('Payroll.csv',mode="w", newline='' ) as file:
    writer =csv.DictWriter(file ,fieldnames =["Name","AGE","CITY","SALARY"])
"""
"""
import csv

emp_data =[
    {"Name" : "JHON","AGE" :22,"CITY" :"FRANCE","SALARY" : 30000},
    {"Name" : "MONTY","AGE" :32,"CITY" :"GERMANY","SALARY" : 35000},
    {"Name" : "DENNIS","AGE" :31,"CITY" :"ITALY","SALARY" : 39000},
    {"Name" : "QUAGMIRE","AGE" :30,"CITY" :"EDGYPT","SALARY" : 36000},
    {"Name" : "LIOUS","AGE" :30,"CITY" :"NIGERIA","SALARY" : 37000},
    {"Name" : "GRIFFIN","AGE" :32,"CITY" :"MOROCO","SALARY" : 34000},
    {"Name" : "DEVASHISH","AGE" :32,"CITY" :"LONDON","SALARY" : 34000},
    {"Name" : "XYZ","AGE" :33,"CITY" :"MOROCO","SALARY" : 34000},

]
with open('payroll.csv' ,mode='w', newline ='') as file:
    writer =csv.DictWriter(file ,fieldnames =["Name","AGE","CITY","SALARY"])
    writer.writeheader()
    writer.writerows(emp_data)


import pandas as pd

df =pd.read_csv('payroll.csv')

df =df[~((df['Name'] == "XYZ") | (df['CITY'] =="MOROCO") | (df['AGE'] <30))]

df.to_csv('payroll.csv', index =False)

print("deleted row where Name: XYZ and CITY :MOROCO")

with open('payroll.csv' ,mode ='r') as file:
    reader =csv.DictReader(file)
    for row in file:
        print(row)

df =pd.read_csv('payroll.csv')

df =df.drop([0,2])
df.to_csv('payroll.csv', index =False)

with open('payroll.csv' ,mode ='r') as file:
    reader =csv.DictReader(file)
    for row in file:
        print(row)
"""
"""
import json

with open('data.json','r') as file:
    dataframe =json.load(file)

print(dataframe['server'])
print(dataframe['matrics']['ERROR'])    

"""
"""
import json

# Example data
data = {
    "server": "192.168.1.10",
    "status": "running",
    "metrics": {
        "ERROR": 3,
        "WARNING": 2,
        "INFO": 5
    }
}

# Write to example.json
with open('example.json', 'w') as file:
    json.dump(data, file, indent=4)

print("example.json file created.")
"""
"""
from datetime import datetime
import json
#data ={'time' : datetime.now().isoformat()}
data = {

    'time' : datetime.now().isoformat(),
            "server" : "123.45.2.12",
            "status" : "Running",
            "Matrics" : {
                "INFO" : 99,
                "ERROR" : 108,
                "WARNING" : 121
            }
}

with open('data.json','w') as file:
    json.dump(data,file,indent =4)
    
    
print("Succesfully built data.json file") 

with open('data.json' ,'r') as file:
    line =json.load(file)

print("SERVER :",line['server'])
print("WARNING :",line['Matrics']['WARNING'])  

json_string ='{ "server" : "192.165.23.1" , "status": "Running"}'

json_formate =json.loads(json_string)
print(json_formate['status'])

python_dict ={ "server" : "192.165.24.1" ,"status": "Running", "MAtrics": { "info":3 ,"error" :4,"warnign":10}}
json_String =json.dumps(python_dict,indent =4)

print(json_String)

"""
"""
from datetime import datetime
import json
data = {
         
            "server" : "123.45.2.12",
            "status" : "Running",
            "Matrics" : {
                "INFO" : 99,
                "ERROR" : 108,
                "WARNING" : 121
            },
           "timestamp": datetime.now().isoformat()  
}

with open('data.json', 'w') as file:
    json.dump(data, file, indent=4)

with open('data.json' ,'r') as file:
    reader =json.load(file)
    print(reader)   
"""
"""
binary_data =b'\x42\x69\x6e\x61\x72\x79\x20\x44\x61\x74\x61'

with open('eample.bin' ,'wb') as file :
    file.write(binary_data)

print("Successfully binary file has been written !")

with open('eample.bin' , 'rb') as file:
    lines =file.readline()
    print(lines)

import os

textfile = 'hello koniee chiwaa my name is torism  i am from trotroo it is beautiful place inside japan it is widely popular for toorism'    

binaryconvert =textfile.encode('utf-8')
with open('largefile.bin','wb') as file:
    file.write(binaryconvert)

print("sucessfully largefile has bin created")
chunk_size =10
with open('largefile.bin' ,'rb') as sourcefile,open('copyfile.bin' ,'wb') as copyfile:
    while chunk := sourcefile.read(chunk_size):
       copyfile.write(chunk)

print("from sourrce file copy file has been created !")

with open('copyfile.bin' , 'rb') as file:
    while chunks := file.read(chunk_size):
        print("\nchunk _>\n")
        print(chunks.decode('utf-8') ,end ='')
"""
"""
import numpy as np
TWODarray =np.array([[1,2,3,21,4],[4,3,12,5,6],[7,6,17,8,9],[12,3,4,3,6],[3,8,9,5,0]])
print("print 2d array :\n",TWODarray)
row_sum =np.sum(TWODarray,axis =1)
print("Row_sums are:",row_sum)
colum_wise =np.sum(TWODarray,axis =0)
print(f"Column wise sums are:{colum_wise}")

max_row =np.argmax(row_sum)
print("row with max val:",max_row)
print("max val row",TWODarray[max_row])
print("row with maximum sum:",row_sum[max_row])
"""

"""
matrix = np.random.randint(0,101,size=(6,6))
print("matrix 6*6:\n",matrix)

max_sum_val =np.sum(matrix,axis=0)
max_col_sum =np.max(max_sum_val)
max_sum_idex =np.argmax(max_sum_val)
diagonal_sum =np.trace(matrix)
print(f"max val sum column wise: {max_sum_val}")
print(f"max val sum column: {max_col_sum}")
print(f"max val sum column index: {max_sum_idex}")
print(f"max val sum column wise: {diagonal_sum}")

del matrix,max_col_sum,max_sum_idex,max_sum_val,diagonal_sum

orders =np.random.randint(0,101,size =(7,5))
print(f"Matrix of 7days X 5Product\n: {orders}")

prices =np.array([121,345,23,54,77])
print(f"price array: {prices}")

prod_unit_sold =np.sum(orders,axis =1)
print(f"Number of unit sold per day: {prod_unit_sold}")
total_reven =np.sum(orders*prices,axis=1)
print(f"total revenue per product sold: {total_reven}")
peak_day_sold =np.max(total_reven)
atindex =np.argmax(total_reven)
peak_day_reven =np.max(total_reven[atindex])
print("peak day revenue(6=saturday): ",peak_day_reven)
print(f"max sold product:{peak_day_sold} at index {atindex}")
prod_sold_per =np.sum(orders,axis=0)
prod_per_index =np.argmax(prod_sold_per)
index_col =np.max(prod_sold_per[prod_per_index])
print(f"column of max sold: {index_col}")
print(f"most sold prod per its category(A):{prod_per_index}")
print(f"product sold per its category: {prod_sold_per}")
del orders,prices,prod_unit_sold,total_reven,peak_day_sold,atindex,peak_day_reven,prod_sold_per,prod_per_index,index_col
"""
"""
import numpy as np
import random
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Random weekly orders (7 days x 5 products)
np.random.seed(42)  # For reproducibility
orders = np.random.randint(0, 51, size=(7, 5))
prices = np.array([100, 200, 150, 120, 80])  # Prices for 5 products

# Calculate daily revenue
daily_revenue = np.sum(orders * prices, axis=1)
product_sales = np.sum(orders, axis=0)

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
products = ["A", "B", "C", "D", "E"]

plt.figure(figsize=(10,5))
sns.lineplot(x=days, y=daily_revenue, marker='o', linewidth=2, color='blue')

# Highlight peak day
peak_day_idx = np.argmax(daily_revenue)
plt.scatter(days[peak_day_idx], daily_revenue[peak_day_idx], color='red', s=100, label='Peak Day')

plt.title("Blinkit - Daily Revenue Trend", fontsize=16)
plt.xlabel("Day of Week")
plt.ylabel("Revenue (₹)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

plt.figure(figsize=(8,5))
sns.barplot(x=products, y=product_sales, palette="viridis")

plt.title("Blinkit - Total Units Sold per Product", fontsize=16)
plt.xlabel("Product")
plt.ylabel("Total Units Sold")
plt.show()

"""
"""
import numpy as np
import random 
import matplotlib.pyplot as plt
import seaborn as sns

np.random.seed(42)
orders =np.random.randint(0,51,size =(7,5))
prices =np.array([100,200,50,220,85])
prod_soldtol =np.sum(orders,axis =1)
dialy_reven =np.sum(orders*prices,axis=1)
product_sales =np.sum(orders,axis =0)

days =["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
products =["A","B","C","D","E"]

plt.figure(figsize =(10,5))
sns.lineplot(x=days,y =dialy_reven,marker='o',linewidth=2,color ='blue')

peak_day_idx =np.argmax(dialy_reven)
plt.scatter(days[peak_day_idx],dialy_reven[peak_day_idx] ,color='red',s =100,label ='Peak_Day')

plt.title("blinkit - Dialy Revenue Trend", fontsize=16)
plt.xlabel("day of week")
plt.ylabel("Revenue (₹)")
plt.legend()
plt.grid(True,alpha =0.3)
plt.show()

plt.figure(figsize =(8,5))
sns.barplot(x =products ,y =product_sales,palette="viridis")
plt.title("blinkit -Total units sold per product: ",fontsize =17)
plt.xlabel("product")
plt.ylabel("total unit sold")
plt.show()
"""
"""
import matplotlib.pyplot as plt
import numpy as np
x =np.arange(1,6)
y=x**2
plt.plot(x,y,marker='o')
plt.title("Simple graph!")
plt.show()
"""
"""
import pandas as pd
data ={
    "Fruits":["apple","banana","pineapple","lemon","tofu","Milk","flour"],
    "Price":[100,40,120,75,45,60,130],
    "Quantity":[92,12,15,53,62,18,19]
}
df =pd.DataFrame(data)
print(df)
#print(f"peak top three line data:\n {df.head(3)}")
#print(f"summarize data by:\n {df.describe()}")
#print(f"Total cal revenue by\n :{df["price"]*df["quantity"]}")
print("\nFirst 3 rows:\n", df.head(3))
print("\nSummary:\n", df.describe())
print("\nTotal Revenue per Product:\n", df["Price"] * df["Quantity"])
"""
"""
import numpy as np
import pandas as pd

data ={
    "OrdersId" : range(1,21),
    "City": np.random.choice(["Mumbai","rajesthan","Madhya pradesh","noida","hydrabad","himachal"],20),
    "Product":np.random.choice(["Apple","banana","eggs","milk","bread","dates","tofu"],20),
    "Price": np.random.choice([100,40,134,34,685,453,909,78,123],20),
    "Quantity": np.random.randint(10,23,size =20),    
    "Dates": pd.date_range(start ="2025-07-21",periods =20,freq ='D')

}
df =pd.DataFrame(data)
df.to_csv("blinkit_orders.csv",index =False)
print("Sample csv created:blinkit_orders.csv created !")

df =pd.read_csv("blinkit_orders.csv")
print("Pead top head:",df.head())
print("\n Info of csv :\n",df.info())
print("\n summary of data Satistics :",df.describe())
print("\nMissing Values:\n", df.isnull().sum())

# If duplicates exist
df = df.drop_duplicates()
# Total revenue column
df["Revenue"] = df["Price"] * df["Quantity"]

# Top 3 products by revenue
top_products = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(3)
print("\nTop 3 Products by Revenue:\n", top_products)

# City with highest revenue
top_city = df.groupby("City")["Revenue"].sum().sort_values(ascending=False)
print("\nRevenue by City:\n", top_city)
import matplotlib.pyplot as plt
import seaborn as sns

# Bar chart for top products
plt.figure(figsize=(8,5))
sns.barplot(x=top_products.index, y=top_products.values, palette="viridis")
plt.title("Top 3 Products by Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.show()

# Bar chart for revenue by city
plt.figure(figsize=(8,5))
sns.barplot(x=top_city.index, y=top_city.values, palette="magma")
plt.title("Revenue by City")
plt.xlabel("City")
plt.ylabel("Revenue (₹)")
plt.show()
"""
"""
print("\n If missing value value: \n",df.isnull.sum())
print(sum)
df =df.drop_duplicates()
"""
"""
import numpy as np
import pandas as pd

data ={
    "OrdersId" : range(1,21),
    "City": np.random.choice(["Mumbai","rajesthan","Madhya pradesh","noida","hydrabad","himachal"],20),
    "Product":np.random.choice(["Apple","banana","eggs","milk","bread","dates","tofu"],20),
    "Price": np.random.choice([100,40,134,34,685,453,909,78,123],20),
    "Quantity": np.random.randint(10,23,size =20),    
    "Dates": pd.date_range(start ="2025-07-21",periods =20,freq ='D')

}
df =pd.DataFrame(data)
df.to_csv("blinkit_orders.csv",index =False)
print("Sample csv created:blinkit_orders.csv created !")

df =pd.read_csv("blinkit_orders.csv")
print("Pead top head:",df.head())
print("\n Info of csv :\n",df.info())
print("\n summary of data Satistics :",df.describe())
print("\n Missing value handled !\n",df.isnull().sum())
df =df.drop_duplicates()

df["Revenue"] =df["Price"]*df["Quantity"]
top_products =df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(7)
print("\n Top three products by Revenue: ",top_products)

top_city =df.groupby("City")["Revenue"].sum().sort_values(ascending =False).head(7)
print(f"\n TOp cities by revenue : \n{top_city}")

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(7,7))
sns.barplot(x =top_products.index,y =top_products.values,palette ="viridis")
plt.title("Top 3 products by revenue")
plt.xlabel("products")
plt.ylabel("Revenue in (₹)")
plt.show()

plt.figure(figsize =(7,7))
sns.barplot(x =top_city.index, y=top_city.values ,palette ="magma")
plt.title(f" Top 3 cities by Revenue :")
plt.xlabel("Cities")
plt.ylabel(" Revenue ($)")
plt.show()
"""
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# create dataset
data ={
    "OrdersId" : range(1,21),
    "City": np.random.choice(["Mumbai","rajesthan","Madhya pradesh","noida","hydrabad","himachal"],20),
    "Product":np.random.choice(["Apple","banana","eggs","milk","bread","dates","tofu"],20),
    "Price": np.random.choice([100,40,134,34,685,453,909,78,123],20),
    "Quantity": np.random.randint(10,23,size =20),    
    "OrderDates": pd.date_range(start ="2025-07-21",periods =20,freq ='D')

}
df =pd.DataFrame(data)
df.to_csv("blinkit_orders1.csv",index =False)
print("Sample csv created:blinkit_orders1.csv created !")


# Load dataset
df = pd.read_csv("blinkit_orders1.csv")
df["OrderDates"] =pd.to_datetime(df["OrderDates"])
# Compute Revenue
df["Revenue"] = df["Price"] * df["Quantity"]

print(df.head())
# Daily revenue trend
daily_revenue = df.groupby("OrderDates")["Revenue"].sum()

# Top products by revenue
top_products = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)

# Revenue by city
city_revenue = df.groupby("City")["Revenue"].sum().sort_values(ascending=False)
plt.figure(figsize=(8,8))

# 1️⃣ Daily Revenue Trend
plt.subplot(2,2,1)
sns.lineplot(x=daily_revenue.index, y=daily_revenue.values, marker='o', color='blue')
plt.title("Daily Revenue Trend")
plt.xticks(rotation=45)
plt.ylabel("Revenue (₹)")

# 2️⃣ Top Products by Revenue
plt.subplot(2, 2, 2)
sns.barplot(x=top_products.index, y=top_products.values, palette="viridis")
plt.title("Top Products by Revenue")
plt.ylabel("Revenue (₹)")

# 3️⃣ Revenue by City
plt.subplot(2, 2, 3)
sns.barplot(x=city_revenue.index, y=city_revenue.values, palette="magma")
plt.title("Revenue by City")
plt.ylabel("Revenue (₹)")


plt.tight_layout()
plt.show()
pivot = df.pivot_table(values="Revenue", index="City", columns="Product", aggfunc="sum", fill_value=0)

plt.figure(figsize=(7,5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("City vs Product Revenue Heatmap")
plt.show()

answer =bool(input("enter ans for quit: 1 else 0"))
if(answer ==True):
    del daily_revenue,top_products,city_revenue,df,data
"""   
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
# create dataset
data ={
    "OrdersId" : range(1,21),
    "City": np.random.choice(["Mumbai","rajesthan","Madhya pradesh","noida","hydrabad","himachal"],20),
    "Product":np.random.choice(["Apple","banana","eggs","milk","bread","dates","tofu"],20),
    "Price": np.random.choice([100,40,134,34,685,453,909,78,123],20),
    "Quantity": np.random.randint(10,23,size =20),    
    "OrderDates": pd.date_range(start ="2025-07-21",periods =20,freq ='D')

}
df =pd.DataFrame(data)
df.to_csv("blinkit_orders1.csv",index =False)
print("Sample csv created:blinkit_orders1.csv created !")


# Load dataset
df = pd.read_csv("blinkit_orders1.csv")
df["OrderDates"] =pd.to_datetime(df["OrderDates"])
# Compute Revenue
df["Revenue"] = df["Price"] * df["Quantity"]

print(df.head())
# Daily revenue trend
daily_revenue = df.groupby("OrderDates")["Revenue"].sum()

# Top products by revenue
top_products = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)

# Revenue by city
city_revenue = df.groupby("City")["Revenue"].sum().sort_values(ascending=False)
plt.figure(figsize=(8,8))

# 1️⃣ Daily Revenue Trend
plt.subplot(2,2,1)
sns.lineplot(x=daily_revenue.index, y=daily_revenue.values, marker='o', color='blue')
plt.title("Daily Revenue Trend")
plt.xticks(rotation=45)
plt.ylabel("Revenue (₹)")

# 2️⃣ Top Products by Revenue
plt.subplot(2, 2, 2)
sns.barplot(x=top_products.index, y=top_products.values, palette="viridis")
plt.title("Top Products by Revenue")
plt.ylabel("Revenue (₹)")

# 3️⃣ Revenue by City
plt.subplot(2, 2, 3)
sns.barplot(x=city_revenue.index, y=city_revenue.values, palette="magma")
plt.title("Revenue by City")
plt.ylabel("Revenue (₹)")
pivot = df.pivot_table(values="Revenue", index="City", columns="Product", aggfunc="sum", fill_value=0)
plt.subplot(2, 2, 4)
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("City vs Product Revenue Heatmap")
plt.tight_layout()
plt.show()


plt.figure(figsize=(7,5))
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("City vs Product Revenue Heatmap")
plt.show()

answer =bool(input("enter ans for quit: 1 else 0"))
if(answer ==True):
    del daily_revenue,top_products,city_revenue,df,data

plt.tight_layout()
plt.show()
pivot = df.pivot_table(values="Revenue", index="City", columns="Product", aggfunc="sum", fill_value=0)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import gc  # for memory cleanup

# 1️⃣ Create Dataset
data = {
    "OrdersId": range(1, 21),
    "City": np.random.choice(["Mumbai","Rajesthan","Madhya Pradesh","Noida","Hyderabad","Himachal"], 20),
    "Product": np.random.choice(["Apple","Banana","Eggs","Milk","Bread","Dates","Tofu"], 20),
    "Price": np.random.choice([100,40,134,34,685,453,909,78,123], 20),
    "Quantity": np.random.randint(10, 23, size=20),
    "OrderDates": pd.date_range(start="2025-07-21", periods=20, freq='D')
}
df = pd.DataFrame(data)
df["Revenue"] = df["Price"] * df["Quantity"]

# 2️⃣ Aggregations
daily_revenue = df.groupby("OrderDates")["Revenue"].sum()
top_products = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False)
city_revenue = df.groupby("City")["Revenue"].sum().sort_values(ascending=False)
pivot = df.pivot_table(values="Revenue", index="City", columns="Product", aggfunc="sum", fill_value=0)

# 3️⃣ Visualization
plt.figure(figsize=(10,8))

plt.subplot(2,2,1)
sns.lineplot(x=daily_revenue.index, y=daily_revenue.values, marker='o', color='blue')
plt.title("Daily Revenue Trend")
plt.xticks(rotation=45)
plt.ylabel("Revenue (₹)")

plt.subplot(2,2,2)
sns.barplot(x=top_products.index, y=top_products.values, palette="viridis")
plt.title("Top Products by Revenue")
plt.ylabel("Revenue (₹)")

plt.subplot(2,2,3)
sns.barplot(x=city_revenue.index, y=city_revenue.values, palette="magma")
plt.title("Revenue by City")
plt.ylabel("Revenue (₹)")

plt.subplot(2,2,4)
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title("City vs Product Revenue Heatmap")

plt.tight_layout()
plt.show(block=False)  # Show without blocking

# 4️⃣ 15-Second Live Countdown🤣
for i in range(5, 0, -1):
    print(f"⏳ Closing in {i} seconds...", end="\r")
    time.sleep(1)

plt.close('all')  # Close all figures

# 5️⃣ Memory Cleanup
del df, data, daily_revenue, top_products, city_revenue, pivot
gc.collect()

print("\n✅ Visualization closed and memory freed!")


"""
📅 30-Day Data Analyst Roadmap
Week 1 – Python Foundations for Data Analysis (Days 1–7)
Goal: Get comfortable with Python, Pandas, and basic data analysis.

Day	Topic & Practice Task
1	Install Python + Jupyter Notebook (via Anaconda). Practice Python basics: variables, loops, conditionals.
2	Work with lists, tuples, sets, dictionaries. Task: Count frequency of items in a list.
3	Learn NumPy basics: arrays, indexing, simple math. Task: Create 2D array and compute row sums.
4	Learn Pandas Series & DataFrame. Task: Load a CSV and explore .head(), .info(), .describe().
5	Data cleaning: handle missing values, duplicates, fillna, dropna.
6	Filtering & Sorting: loc[], iloc[], query(), sorting by multiple columns.
7	Mini Project: Analyze a small CSV dataset (like sales or Blinkit sample orders). Clean & compute KPIs (total revenue, avg order value).

✅ Deliverable: Cleaned dataset + Jupyter Notebook with insights.

Week 2 – SQL Mastery for Data Analysis (Days 8–14)
Goal: Be able to query any relational dataset and combine it with Python.

Day	Topic & Practice Task
8	Install SQLite or MySQL. Learn SELECT, WHERE, ORDER BY.
9	Learn Aggregations: SUM, AVG, COUNT, MAX, MIN. Task: Compute total orders per city.
10	Learn GROUP BY & HAVING. Task: Find top 3 products by revenue.
11	Learn JOINS (INNER, LEFT). Task: Combine Orders and Customers table to find city revenue.
12	Learn Subqueries & CTEs. Task: Find customers who placed more than 5 orders.
13	Learn Window Functions: ROW_NUMBER(), RANK(), OVER().
14	Mini Project: Analyze a sample Orders + Customers + Products database. Write 5–7 SQL queries for KPIs.

✅ Deliverable: SQL script file + screenshots of query results.

Week 3 – Python + SQL + Visualization (Days 15–21)
Goal: Connect Python to SQL and visualize your insights.

Day	Topic & Practice Task
15	Learn Python-Database connection using sqlite3 or SQLAlchemy. Fetch SQL data into Pandas.
16	Introduction to Matplotlib: line, bar, scatter plots. Task: Plot daily order trend.
17	Learn Seaborn: distribution plots, box plots, heatmaps.
18	Combine SQL + Python: Fetch orders from DB, analyze in Pandas, plot top 5 products.
19	Learn GroupBy in Pandas and create multiple KPIs (Revenue by City, Orders by Hour).
20	Learn Advanced Visualization: Multiple plots, subplot grids, annotations.
21	Mini Project: Blinkit-style Order Analysis Report with charts:
- Revenue by City
- Top 5 Products
- Orders by Hour
- Weekday vs Weekend Orders

✅ Deliverable: Jupyter Notebook + Plots (saved as images).

Week 4 – Portfolio Projects & Dashboarding (Days 22–30)
Goal: Build 2 real projects and create a portfolio.

Day	Task
22	Learn Power BI or Tableau Public basics (or continue with Python if preferred).
23	Project 1: E-Commerce Sales Analysis (SQL + Python + Visualization).
24–25	Continue Project 1 – Create dashboard or final report notebook.
26	Project 2: Delivery Performance Analysis (Blinkit/Swiggy style). KPIs: Avg Delivery Time, On-Time %, City Performance.
27–28	Continue Project 2 – Visualize trends & save plots.
29	Upload all projects to GitHub with clear README.md.
30	Polish LinkedIn profile & create a portfolio post with your key visualizations.

✅ Final Deliverable:

2 Complete Portfolio Projects

GitHub Repository with SQL & Python notebooks

Optional Dashboard link (Tableau / Power BI)

🎯 Bonus Tips for a Strong Portfolio
Use realistic datasets: Kaggle (Swiggy/Instacart/Flipkart datasets) or mock Blinkit orders.

Make your README explain your approach + insights, not just code.

Share 1–2 visual insights on LinkedIn to get visibility for job hunting.

If you want, I can provide ready-to-use datasets for:

Blinkit Orders & Products

Delivery Performance Analysis
so you can start your Week 1 & 2 projects immediately without hunting for data.

Do you want me to prepare and give you these datasets next?
Ask ChatGPT

"""

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

