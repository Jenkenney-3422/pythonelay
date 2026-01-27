"""
try:
    a =10/0
except ZeroDivisionError as e:
    print(f"Error has occured as : {e}")
else: 
    print("No error occured")
finally: 
    print("this block is always executed ")
"""

import pandas as pd
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import numpy as np

X_origin , y_origin =make_classification(n_samples =1000, n_features= 5, n_clusters_per_class=1,weights=[0.9,0.1])
df = pd.DataFrame(X_origin,columns=[f'Feature_{i}' for i in range(5)])
df['Target'] =y_origin

print("origin class Distribution")
print(df['Target'].value_counts(normalize=True))
X_train_u,X_test_u,y_train_u,y_test_u =train_test_split(df.drop('Target',axis=1),df['Target'],test_size=0.2 ,random_state =1)
X_train_s, X_test_s, y_train_s, y_test_s =train_test_split(df.drop('Target',axis=1),df['Target'],test_size =0.2 ,stratify=df['Target'],random_state =42)
print("without stratify class Distribution")
print(y_train_u.value_counts(normalize=True))
print("with stratify class Distribution")
print(y_train_s.value_counts(normalize=True))
model =RandomForestClassifier(n_estimators=100,random_state=42)
model.fit(X_train_s,y_train_s)
y_pred =model.predict(X_test_s)
print("Classification Report:")
print(classification_report(y_test_s,y_pred))

try:
    import newpactisepacket
except ImportError as e:
    print(f"Failed to import newpactisepacket: {e}")    

try:
    f =open('server.log')
    with open('server.log' , mode='r') as file:
     for row in file:
        rows =f.read()
        print(f"{rows}")
except FileNotFoundError as e:
   print(f"file does not Exist: {e}")
else:
   print("everything is ok!!")
finally:
   print("closing file now !")
   f.close
"""
"""
try:
    x =int(input("Enter the number :"))
    if x%2!=0:
        print("the number is odd!")
except ValueError as e:
    print(f"Invalid input Zerodivision or value Error:{e} ")
else:
    print(f"No error occured num is :{x}")
finally:
    print("Execution completed.")

"""
def get_valid_ammount():
    while True:
        try:
            ammount = float(input("enter the ammount:"))
            return ammount
        except ValueError:
            print("INvalid input Error : please enter a numeric value.")
            

def with_drwal(ammount):
    balance =1000
    if ammount > balance: 
        print(f"Insufficient balance for : {ammount} having error current balance : {str(balance)}")
    elif ammount <=0:
        print(f"value should be greater than zero : entered ammount : {ammount} and balace is {balance}.")
    else:
        balance -= ammount
        print(f"Withdrawal successful. New balance is: {balance}")

try: 
    current_state =get_valid_ammount()
    with_drwal(current_state)
except ValueError as e :
    print(f"the error : {str(e)}")
