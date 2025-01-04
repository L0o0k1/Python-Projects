print("Welcome to My Quiz!")
play= input("Do U want 2 Play ? (yes/no) ")
if play.lower() != "yes": 
    quit()
print("Ok! Let's Play :)! ")
#========================
## Score System:
ply_score = 0 

# => 1
answer= input("What Does CPU Stand For? ")
if answer.lower() == "central proccessing unit":
    print('Correct!')
    ply_score += 1
else: 
    print("Incorrect!!")
#============================
# => 2
answer = input("What Does GPU Stand For? ")
if answer.lower() == "graphics proccessing unit":
    print('Correct!')
    ply_score += 1
else: 
    print("Incorrect!!")
#============================
# => 3
answer= input("What Does RAM Stand For? ")
if answer.lower() == "random access memory":
    print('Correct!')
    ply_score += 1
else: 
    print("Incorrect!!")
#============================
# => 4
answer = input("What Does PSU Stand For? ")
if answer.lower() == "power supply unit":
    print('Correct!')
    ply_score += 1
else: 
    print("Incorrect!!")
#============================
#  => 5
answer= input("What Does BIOS Stand For? ")
if answer.lower() == "basic input output system":
    print('Correct!')
    ply_score += 1
else: 
    print("Incorrect!!")
#============================
# => 6
answer= input("What Does SSD Stand For? ")
if answer.lower() == "solid state drive":
    print('Correct!')
    ply_score += 1
else: 
    print("Incorrect!!")
#============================
# => 7
answer= input("What Does HDD Stand For? ")
if answer.lower() == "hard disk drive":
    print('Correct!')
    ply_score += 1
else: 
    print("Incorrect!!")
#============================
# => 8
answer= input("What Does USB Stand For? ")
if answer.lower() == "universal serial bus":
    print('Correct!')
    ply_score += 1
else: 
    print("Incorrect!!")
#============================
# => 9
answer= input("What Does LAN Stand For? ")
if answer.lower() == "local area network":
    print('Correct!')
    ply_score += 1
else: 
    print("Incorrect!!")
#============================
# => 10 
answer= input("What Does NIC Stand For? ")
if answer.lower() == "network interface card":
    print('Correct!')
    ply_score += 1
else: 
    print("Incorrect!!")
#============================
print("You Got " + str(ply_score) + "Question Correct!")
print("You Got " + str((ply_score / 4) * 100 ) + "%.")