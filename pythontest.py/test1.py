print("hello")

#variables
num =3
decimal =3.14
name ="jhon"
is_student = True
sets ={1,23,4,4}
print(sets)
list =[1,2,3,4,4,4,5]
print(list)
tuple =(1,2,3,4,4,5)
print(tuple)
dict ={"name":"devashish","age":23}
print("name" in dict)
print(dict["name"])
print(tuple[0:3:1])
"""
This is
a multiline
comment
"""
servers = ["sever1","server2","server3"]
for server in servers:
  print(server)
  print(f"found {server}")
     
  break
  """if(server =="server2"):
      print("found server2")
      break """

count_retry =3
attempt =0
while attempt < count_retry :
  print("Connecting...")
  attempt+=1


cpu_threshold =80
if(cpu_threshold>=80):
  print("cpu is overloaded")
elif(cpu_threshold>=60):
  print("cpu is underloaded")
else:
  print("cpu is normal")


is_secure =True
for serving in servers:
  if is_secure:
     print(f"connecting to {serving}")
  else:
    print(f"connecting to {serving} without security")

def greet(name):
  print(f"hello {name}")

#def square(element):
 # val =lambda x:x*x
  #return val(element)


namels =["devashish","jhon","doe","jane","joddy"]
for name in namels:
  greet(name)

def multiplier(factor):
  return lambda x:x*factor

def square(element):
  squareva = lambda x: x * x
  return squareva(element)

element =7
print(square(element))

value=multiplier(element)
#print(value(8))
print(multiplier(7)(8))

def deploy(server ="local host",port =30):
  return f"Deploy to{server}:{port}"

print(deploy())
  
def y_compo(xcompo):
  value2 =lambda y:y*xcompo
  return value2(xcompo)

def graph(x_acxis):
  value1= lambda x:x*x_acxis
  return y_compo(value(x_acxis))

print(graph(element))

log_content = """
INFO Server started at 2025-07-19 10:00:00
INFO Listening on port 8080
WARNING Disk space at 80%
INFO Connection established from 192.168.1.100
ERROR Failed to connect to database
INFO Health check passed
WARNING High memory usage detected
ERROR Disk quota exceeded
INFO Scheduled backup completed
INFO Server shutting down at 2025-07-19 18:00:00
INFO Starting server
WARNING High CPU usage
ERROR Database failure
INFO Connection accepted
ERROR Disk full
WARNING Memory usage warning
INFO Shutdown complete
"""

with open("server.log", "w") as file:
    file.write(log_content.strip())

print("Sample server.log file has been generated.")

