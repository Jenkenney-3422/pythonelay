"""
 syntax of error handling

 try:
 # risky code
except SomeError :
# handling error
else:
# if code does'nt have any error
finally:
# code that aways run
"""
"""
try:
    result =10/0
except ZeroDivisionError as d:
    print(f"code fail execution cause {d}") 
    """
"""

try:
    f =open("server.log")
    with open('server.log',mode ='r') as file:
        for row in file:
           rows =file.read()
           print(rows) 
except FileNotFoundError as e:
    print(f"file not found error{e}")

finally:
    f.close()
    print(f"filee has closed")     
"""
"""
try:
    x =int(input("enter a integer val :"))
    if x%2 ==0:
        print("value is even")
except ValueError as e:
    print("entered odd or invalid input as x")
finally:
    print("entered value is: ",x)  
"""

"""
def get_integer_input():
    while True:
        try:
            user_input = int(input("enter a valid integer: "))
            return user_input
        except ValueError :
            print("Error : Invalid integer value.please try again.")     
def withdraw(val):
    if val >1000:
        raise ValueError("Entered amount exceeded current balance !")
   

try:
    valid_integer =get_integer_input()
    print("valid integer entered: ", valid_integer)
    withdraw(valid_integer)
except ValueError as e:
    print("An error occurred: ",str(e))
    #print(f"Error : {e}")    


"""

"""
import logging

# 1. Create a logger object
logger = logging.getLogger('MyLogger')
logger.setLevel(logging.DEBUG)

# 2. Create a FileHandler (writes to file)
file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.DEBUG)

# 3. Create a custom Formatter
custom_formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')

# 4. Attach formatter to file handler
file_handler.setFormatter(custom_formatter)

# 5. Attach handler to logger
logger.addHandler(file_handler)

# 6. Example logs
logger.info("App started")
logger.warning("Low memory")
logger.error("Service failed to respond")

# Setup basic logging config
logging.basicConfig(
    filename='errors.log',          # Log file name
    level=logging.ERROR,            # Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Example error logging
try:
    1 / 0
except ZeroDivisionError as e:
    logging.error("Error occurred: %s", e)
    
"""
"""
import subprocess
import logging

logging.basicConfig(filename='deploy.log', level=logging.INFO)

def deploy_app():
    try:
        subprocess.run(['kubectl', 'apply', '-f', 'deployment.yaml'], check=True)
        logging.info("✅ Deployment succeeded.")
    except subprocess.CalledProcessError as e:
        logging.error(f"❌ Deployment failed: {e}")
        rollback()
    finally:
        cleanup()

def rollback():
    subprocess.run(['kubectl', 'rollout', 'undo', 'deployment/my-app'])
    logging.info("🔄 Rolled back deployment.")

def cleanup():
    logging.info("🧹 Cleanup complete.")

deploy_app()
"""
# VIM COMMANDS TO EDIT OR MAKING FILES
# 🛠️ Basic Commands
"""
Action	Command
Open a file	vim filename.txt
Enter Insert Mode	i
Save file	:w
Quit Vim	:q
Save and quit	:wq or ZZ
Quit without saving	:q!
Delete a line	dd
Undo	u
Redo	Ctrl + r
Search	/pattern then n/N
Replace	:%s/old/new/g
 """
"""
devops-pipeline-project/
├── Jenkinsfile               # Pipeline definition
├── deploy.py                 # Your deployment automation script
├── requirements.txt          # Python dependencies
├── Dockerfile                # Container build instructions
├── deployment.yaml           # Kubernetes manifest
└── README.md                 # Optional: docs about setup and usage

"""
# deploy,py
"""
import subprocess
import logging
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.text import Text

# Rich console setup
console = Console()

# Load environment variables from .env
load_dotenv()

# Configurable constants from .env
IMAGE_NAME = os.getenv('IMAGE_NAME', 'default-image')
TAG = os.getenv('TAG', 'latest')
DOCKERFILE = os.getenv('DOCKERFILE', 'Dockerfile')
DEPLOYMENT_YAML = os.getenv('DEPLOYMENT_YAML', 'deployment.yaml')

# Rich logger
def rich_log(message, style="bold cyan"):
    console.print(Text(message, style=style))

def run_command(command, check=True):
    rich_log(f"🔧 Executing: {command}", style="yellow")
    result = subprocess.run(command, shell=True)
    if check and result.returncode != 0:
        console.log(f"❌ Command failed: {command}", style="bold red")
        exit(1)

def build_docker_image():
    rich_log(f"🐳 Building Docker image {IMAGE_NAME}:{TAG}", style="bold green")
    run_command(f'docker build -t {IMAGE_NAME}:{TAG} -f {DOCKERFILE} .')

def push_docker_image():
    rich_log("📤 Pushing Docker image...", style="bold magenta")
    run_command(f'docker push {IMAGE_NAME}:{TAG}')

def apply_kubernetes_manifest():
    rich_log(f"☸️ Applying Kubernetes manifest: {DEPLOYMENT_YAML}", style="bold blue")
    run_command(f'kubectl apply -f {DEPLOYMENT_YAML}')

def main():
    rich_log("🚀 Starting deployment automation...", style="bold white")
    build_docker_image()
    # push_docker_image()  # Uncomment if pushing is needed
    apply_kubernetes_manifest()
    rich_log("✅ Deployment completed successfully!", style="bold green")

if __name__ == '__main__':
    main()

"""
# make sure you Also add
"""
.env
__pycache__/
*.log
"""
# Dockerfile
"""
# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY deploy.py .
COPY deployment.yaml .
COPY .env .

# Optional: environment variables (can also be loaded via .env)
ENV PYTHONUNBUFFERED=1

# Entry point (if you want to run deploy.py directly when container starts)
CMD ["python", "deploy.py"]

-------------------------------------------
# 1. Specify the base image (a minimal Python OS here)
FROM python:3.10-slim

# 2. Set a working directory inside the container
WORKDIR /app

# 3. Copy your dependency file first (to leverage layer caching)
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your project files into the container
COPY . .

# 6. Set environment variables (can be skipped if using .env + python-dotenv)
ENV PYTHONUNBUFFERED=1

# 7. Define the default command to run
CMD ["python", "deploy.py"]


"""
# deploy.yaml
"""
# 1. Specify the base image (a minimal Python OS here)
FROM python:3.10-slim

# 2. Set a working directory inside the container
WORKDIR /app

# 3. Copy your dependency file first (to leverage layer caching)
COPY requirements.txt .

# 4. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy your project files into the container
COPY . .

# 6. Set environment variables (can be skipped if using .env + python-dotenv)
ENV PYTHONUNBUFFERED=1

# 7. Define the default command to run
CMD ["python", "deploy.py"]

"""
# .gitignore
"""
# 🐍 Python artifacts
__pycache__/
*.py[cod]
*.log

# 🚀 Environment config
.env

# 📦 Package-related
*.egg
*.egg-info/
dist/
build/
*.whl

# 📚 Dependency folders
*.db
*.sqlite3

# 🐳 Docker artifacts
docker-compose.override.yml
*.tar
*.gz

# 🧪 Testing artifacts
htmlcov/
coverage.xml
.pytest_cache/
nosetests.xml

# 🧰 IDE/editor stuff
.vscode/
.idea/
*.swp
*.sublime-project
*.sublime-workspace

# 🔧 OS files
.DS_Store
Thumbs.db

# 🐘 Kubernetes runtime files
*.kube/
*.conf
*.yaml~  # Backup versions

"""
"""
tol,x,y =input("enter the total no of student ,girls,boys").split() 
print(f"total number of student: ",tol)
print("\n")
print(f"the number of girls: {y}\n")
print(f"the number of boys: {x}\n")

print(tol,y,x)
"""
"""
def total__bill(quantity ,price):
    return quantity*price
flower =input("name of flower ?")
quantity =int(input("amount or number of flower :"))
price =float(input("price of single flower !"))
Bill =total__bill(quantity,price)
print("TOtal Cost: ${:.2f}".format(Bill))
print("single rose price :${:.3f}".format(price))
print(f"type of flower :{flower},quant :{quantity},price :{price}")
print(type(flower))
print(type(Bill))
print(type(price))
print(type(quantity))
"""
"""
print("devash" , "nnd" ,end ='@'"\n")
print("09","1","27" ,sep ='-')
print("geeks","for","Geeks",end ="@gmail.com",sep ='-')
tupple =("lay","Bahri","Frog")
lists =["kuch","bhi","bhai"]
dicts ={"posgrey_SQL":3.5,"my_SQL":4.2,"MOngo_DB":3.87}
print("\n")
print(dicts["posgrey_SQL"])

intnum =int(input("enter a number: "))
sum= intnum + 5
print("num  is %d",sum)
"""
"""
set1 =set(["Geeks","for","leeks","freaks","Geeks"])
print(set1)
for i in set1:
    print(set[i])

print("Geeks" in set1)  
set2 =set("seeksGheeksSheepsmeaps")
print(set2)
set3 =set(["Geeks","for","Geeks"])
print(set3)
"""
"""
set1 = set(["Geeks", "For", "Geeks"])
print(set1)

# loop through set
for i in set1:
    print(i, end=" ")
    
# check if item exist in set    
print("Geeks" in set1)

d ={2:"geeks", 4:"heeks",5:"leaks","mango": 23}
d1 =dict(d)
print(d1.get(5))
print(d1["mango"])

fruits =["mango","apple","banana","chiku","grapes","pineapple"]
fruits.append("pomogranade")
print(fruits)
fruits.remove("mango")
print(fruits)
print("Mango" not in fruits)
if("apple" is not fruits):
   print("Apple is not here")
else:
    print("apple is here")

if("apple" not in fruits):
   print("Apple is not here")
else:
    print("apple is here")
       
co_ordinate =(3,5)
print(co_ordinate)
print("X-cordinate:",co_ordinate[0])
print("Y-cordinate:",co_ordinate[1])
print(co_ordinate)
val =34
val /=2
print(val)
x =7
print(x << 2)
a,b =19,18
min =a if a < b else b
print(min)

expr =10 + 20*30
name ="alex"
age =0
if name=="jhon" and name =="alex" and age<=0:
   print("not welcome")
else:
   print("welcome")
   """
"""
age =32
men ="teenager" if(age>=18) else "kid"
print(men)

is_member =True
if age >= 35:
    if(is_member):
        print("Eligible for discount 30%")
    else:
        print("Eligible for discount 20%")
else:
    print("Not eligible for any discount")

if age ==18:
    print("teenager")
elif ( age >=18 and age <20):
    print("young adult")
elif (age>20 and age<=35):
    print("PRIME !!")
else:
    if(age>35):
        print("OLD PRIME")
    else:
        print("kid optimus prime") 

number =0.5
match number:
    case 1 | 0.5:
        print("number 0.5 or one!")
    case 2 | 3:
        print("number two or three")
    case _:
        print("other number")   


a=int(input())
b=int(input())
#code here
p = (a and b)
#Do a or b below
q = (a or b)
#Do not a below
r =(not a) 
#The code below prints the output. Don't change it!
print(p,q,r)         
"""
"""
def checkOddEven(x):
    if (x % 2 == 0):
        return "Even"

    else:
        return "Odd" 
X =5
print(checkOddEven(X))
"""
#class Solution:
#   def checkStatus(self, a, b, flag):
"""
class Solution:
    def checkStatus(self, a, b, flag):
        if (((a<0) ^ (b>0)) ^ (not (flag))):
            return 1
        else:
            return 0    

flag = False
sol = Solution()
result = bool(sol.checkStatus(-1, 1, flag)) # ✅ Correct function call
print(result)  
"""
"""
class Solution:
    def checkStatus(self, a, b, flag):
        if(((a<0) ^ (b>0)) ^ (not(flag))):
            return 1
        else:
            return 0
"""
"""            
class Solution:
    def checkStatus(self, a, b, flag):
        # XOR logic as in your code
        if ((a < 0) ^ (b > 0)) ^ (not flag):
            return 1
        else:
            return 0

# ✅ Take input from user
user_input = input("Enter values like: a = 1, b = -1, flag = False\n")

# ✅ Parse the input
# Example input: a = 1, b = -1, flag = False
parts = user_input.replace(" ", "").split(",")
a = int(parts[0].split("=")[1])
b = int(parts[1].split("=")[1])
flag_str = parts[2].split("=")[1].lower()
flag = flag_str == "true"  # Convert string to boolean

# ✅ Create object and call method
sol = Solution()
result = bool(sol.checkStatus(a, b, flag))
print(result)
del a,b,flag_str,flag
"""
"""
n =4
for i in range(0,n):
    print(i)
   
del n
li =["mango" ,"papaya","grapes"]
for iter in li:
    print(iter)
tup =("mango" ,"papaya","grapes")
for i in tup:
    print(i)
sets ={"mango" ,"papaya","grapes","jammun","pinetaplle"}        
for it in sets:
    print(it)
dic =dict({'A':123 ,'B':543})
for i in dic:
    #print("%s %d", i ,dic[i])    
    print(f"{i} {dic[i]}")
"""
"""
li =["Geeks","for","Geeks"]
for i in range(len(li)):
    print(li[i])
else:
    print("you are inside else box")

del li,i
listcom =["Tata","Consultency","Services","Vowskwagon","BMW"]
recur =-2
while recur < 3:
    print(listcom[recur])
    recur +=1
else:
    print("you are in else block")

del listcom,recur    


for i in range(1, 5):
    for j in range(i):
        print(i,end =' ')
    print()

for letter in 'Geeksforgeeks':
    if(letter =='e' or letter =='s'):
        continue
    else: print("Current letter:",letter)

for letter in 'Geeksforgeeks':
    pass

print("last letter:",letter)

fruits =["Tata","Consultency","Services","Vowskwagon","BMW","banana","grapes"]
iter_obj =iter(fruits)
for fruit in fruits:
    while True:
        try:
            fruit =next(iter_obj)
            print(fruit)
        except StopIteration:
            break
        else:
            print("lay")
        finally:
            print(fruit) 

del fruits,iter_obj,fruit
"""
"""
n = int(input())

# Your code here
for i in range(1,11):
    print(n*i)

del n
"""
"""
items =input("enter the list of items seperated by commas").split(",")
for item in items:
    print(f"Buy:{item.strip()}")
"""
"""
number =int(input("enter the num:"))
for n in range(1,number+1):
    print(f"{n} of square:{n**2}")
    """
"""
import time
seconds =int(input("enter the number:"))
for i in range(seconds,0,-1):
    print("time left:",i)
    time.sleep(1.0)

print("times-up")  
while seconds>0:
    print("time left->",seconds)
    seconds-=1

print("times-up")  
"""

total =0
num=int(input("the number:"))
while num != 0:
    total +=num
    num=int(input("the number:"))

print(f"the sum total is:{total}")    
del num,total
bill =0
while True:
    pay =int(input("the num:"))
    if (pay!= 0):
        bill +=pay

    else: 
        print("{Pay bill for: ",bill)
        break     
del pay,bill    
"""
"""
tabnum =int(input())
for i in range(1,tabnum+1):
    for j in range(i):
        print(i ,end =' ')
    print()    

del tabnum,i,j

multe =int(input())
for i in range(1,multe+1):
    for j in range(i+1):
        print(i*j ,end=' ')
    print()

del multe,i,j

n=int(input("enter num:"))
for i in range(n):
    for j in range(n):
        if i==j:
            print("1" ,end=' ')
        else:
            print("0",end =' ')
    print()  
del n              

"""
2️⃣ Data Science & Analytics (For analytical/quantitative interest)
Roles:

Data Analyst (like Blinkit hires)

Business Analyst

Machine Learning Engineer

Data Scientist

Skills Needed:

Python/R, SQL

Statistics, Probability

PowerBI, Tableau

ML Libraries (Pandas, Numpy, Scikit-learn)

Best for: B.Tech CSE/IT, ECE (with coding), Mechanical/Civil (if skilled in data analytics)


"""
"""
1️⃣ Software & IT (Best for CSE / IT / ECE students)
Roles:

Software Developer / Software Engineer

Data Analyst / Business Analyst

Web Developer / App Developer

DevOps / Cloud Engineer

Cybersecurity Analyst / Network Engineer

Skills Needed:

Programming (Python, Java, C++), DSA

Databases (SQL, MongoDB)

Web/App Dev (HTML, CSS, JS, React, Node.js)

Cloud & DevOps (AWS, Azure, Docker, CI/CD)

Example Companies: TCS, Infosys, Amazon, Blinkit (for data roles), Zomato, Startups
"""
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
"""
num =int(input("enter num !:"))
for i in range(num+1):
    for j in range(i+1):
        print(i*j ,end =' ')
    print()    

del num    
num =int(input("enter num !:"))
for i in range(num):
    for j in range(num):
        if i==j:
            print("1",end=' ')
        else:
            print("0",end=' ')
    print()        

del num
"""
"""
a =[1.5,3.4,5.3,2.83,9.12]
from functools import reduce
def add(x: float,y : float) ->float:
    return x+y

res =reduce(add,a)
print(res)

del a,res
b =[1.5,3.4,5.3,2.83,9.12]
res1 =reduce(lambda x,y : (x%y),b)
print(res1)
del b,res1
from itertools import accumulate
from operator import add
als =[12,34,76,87,23,35,88,756]
res =accumulate(als,add)
print(list(res))
del res,als
als =[12,34,76,87,23,35,88,756]
import functools
import operator
print(functools.reduce(operator.add,als))
print(functools.reduce(operator.sub,als))
print(functools.reduce(operator.add,["gekks","for","Hekks"]))
del als
"""
def decorator(func):
    def wrapper(*args,**kwargs):
        print("before calling func!")
        result =func(*args,**kwargs)
        print("after calling func!")
        return result    
    return wrapper
    


@decorator

def add(x: int ,y: float)->float:
    print("the sum is :",2*(x+y))
    return (2*x + 2*y)

def greet():
    print("hell wiered")
a =5
b =7.8
print(add(a,b))
greet()
