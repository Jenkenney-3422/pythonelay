#print("testing proogrmam work !!")
#x=40
#y=20
#z=x/y
#print(z)
#name="bro"
#print(name)
#first_name ="Devashish"
#last_name ="Namdeo"
#full_name =first_name+" "+last_name
#print("pro python programmer Dr."+full_name)
"""
age = 18
age+=2
height =170.12
human =True
print("your age is :"+str(age)+" years old")
print(type(age))
print("your height is: "+str(height)+"cm")
print("are you a smarty human which has IQ of 190"+str(human)+" totally true")
"""
"LUDO Game in python(pre mature)"
"""
import random
token =int(random.randint(1,6))
print(type(token))
print(token)
chance =5
while(1<=chance):
 chance-=1
 digit =int(input("throw the dice !!"))
 if(digit==token):
    print("you win the game !!"+" and left remaining chances are :"+str(chance))
    break
 elif(chance==0):
    print("you are lose !! GAME OVER!!")
 elif(digit!=token):
    print("you lose !! but your Remaining chance are:"+str(chance))
 else:
    print("you lose!!"+"youur remaining chance are:"+str(chance))
"""

#chance=3
#while(chance>=1):
#    digit =int(input("throw the dice !!"))
#    chance-=1
"""
n =int(input("enter the number :"))
count =0
for i in range(1,n+1):
 if(n%i==0):
   print(i)
   count+=1

print("the number of factors are:"+str(count))  
"""
# actual LUDO GAME IN PYTHON
"""
num1 =0b01
num2= 0b01
num1 =num1+num2
num3 =int(num1)
print(num3)
print("the number in bary: "+str(num1))
"""
"""
import random
n =int(input("enter the timer endsat:"))
for i in range(1,n+1):
   bin =0b00
   while(1):
      counter =0b00
      if(counter==0b00):
         num1 =int(input("enter1 for play and 0 for quit"))
         if(num1==1):
            rand =random.randint(1,6)
            print(rand)

         #else:
         #   break   
         #print("userone")
       
      elif(counter ==0b01):
         print("user2")

      elif(counter ==0b11):
         print("user3")

      else:
         print("user 4")

      counter+=0b01          
   """ 


""""""
import random

player1_position = 0
player2_position = 0


while(1):
   finalscore =35
   
   print("playing turn of player 1 !! press 1 for continue and 0 for leave")
   feedback =int(input("enter the feedback: "))
   dice =random.randint(1,6)
   if(player1_position+dice<finalscore and feedback==1):
      player1_position+=dice
      
      #if(player1_position+dice==finalscore):
      #   print("the player one is the winner scored:"+str())
      print("the player one scored :"+str(player1_position)+"and icremented by: "+str(dice))

   elif(player1_position+dice==finalscore):
      player1_position+=dice
      
      print("the player 1 scored :"+str(player1_position)+"and icremented by: "+str(dice))
      print("player 1 is winner ")
      break   

   elif(feedback==0):
      print("you leaved the game!!")
      break   

   else:
      print(" ")
   
   
   print("playing turn of player 2: a press 1 for continue and 0 for leave")
   feedback =int(input("enter the feedback: "))
   dice =random.randint(1,6)
   if(player2_position+dice<finalscore and feedback==1):
      player2_position+=dice
      print("the player 2 scored :"+str(player2_position)+"and icremented by: "+str(dice))

   elif(player2_position+dice==finalscore and feedback==1):
      player2_position+=dice
      print("the player 2 scored :"+str(player2_position)+"and icremented by: "+str(dice))
      print("player 2 is winner ")
      break   

   elif(feedback==0):
      print("YOU LEAVED the GAME!!")
      break   

   else:
      print(" ")

   
"""
import random

player1_position = 0
player2_position = 0

while(1):
   finalscore =15
   
   print("playing turn of player 1 !! press 1 for continue and 0 for leave")
   feedback =int(input("enter the feedback: "))
   dice =random.randint(1,6)
   if(player1_position+dice<finalscore and feedback==1):

      player1_position+=dice
      if(player1_position+dice==finalscore):
         print("the player 1 is winner by scoring :"+str(player1_position)+"and icremented by: "+str(dice))
         break
      
      print("the player 1 scored :"+str(player1_position)+"and icremented by: "+str(dice))

   else:
      if(player1_position+dice>finalscore):
         break      


   print("playing turn of player 2 !! press 1 for continue and 0 for leave")
   feedback =int(input("enter the feedback: "))
   dice =random.randint(1,6)
   if(player2_position+dice<=finalscore and feedback==1):

      player2_position+=dice
      if(player2_position+dice==finalscore):
         print("the player 2 is winner by scoring :"+str(player2_position)+"and icremented by: "+str(dice))
         break
      
      print("the player 2 scored :"+str(player2_position)+"and icremented by: "+str(dice))

   else:
      if(player2_position+dice>finalscore):
         break      
"""
"""
import random
player1_position =0
player2_position =0

while(1):
   finalscore =25
   print("playing turn of player 1 !! press 1 for continue and 0 for leave")
   feedback =int(input("enter the feedback: "))
   dice =random.randint(1,6)
   if(player1_position+dice<finalscore and feedback==1):
      player1_position+=dice
      print("the player 1 scored :"+str(player1_position)+"and icremented by: "+str(dice))

   elif(feedback==0):
      break   

   else:
      if(player1_position+dice==finalscore):
         print("the player 1 is winner by scoring :"+str(player1_position+dice)+"and icremented by: "+str(dice))
         break

      else:
         print(" ")
         

   print("playing turn of player 2 !! press 1 for continue and 0 for leave")
   feedback =int(input("enter the feedback: "))
   dice =random.randint(1,6)
   if(player2_position+dice<finalscore and feedback==1):
      player2_position+=dice
      print("the player 2 scored :"+str(player2_position)+"and icremented by: "+str(dice))
   
   elif(feedback==0):
      break

   else:
      if(player1_position+dice==finalscore):
         print("the player 2 is winner by scoring :"+str(player2_position+dice)+"and icremented by: "+str(dice))
         break

      else:
         print(" ")   
"""
"""
6265652928
9074270757
hn 390 , Zone:06 , Ward :30, Greencity ,Madhotal , Jabalpur, MP
hn 390 , Zone:06 , Ward :30, Greencity ,Madhotal , Jabalpur, MP
Near Narayan Kirana Store ,Near Roads : Karmeta , Rivjha

"""
