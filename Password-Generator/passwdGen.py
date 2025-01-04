import secrets
import string

def gen_passwd(min_len, num=True, spcChars=True):
    lett = string.ascii_letters
    digi = string.digits
    spec = string.punctuation
    
    chars = lett
    if num:
        chars += digi  
    if spcChars:
        chars += spec
        
    pwd = ""
    meetTheCrit = False
    has_num = False
    has_spec = False
    has_lett = False
    
    MAX_LENGTH = 128  # maximum length
    while (not meetTheCrit or len(pwd) < min_len) and len(pwd) < MAX_LENGTH:
        newChar = secrets.choice(chars)
        pwd += newChar
        
        if newChar in digi:
            has_num = True
        elif newChar in spec:
            has_spec = True
        elif newChar in lett:
            has_lett = True
            
        meetTheCrit = True
        if num:
            meetTheCrit = meetTheCrit and has_num
        if spcChars:
            meetTheCrit = meetTheCrit and has_spec
        meetTheCrit = meetTheCrit and has_lett
            
    return pwd

# Input validation. minimum length
while True:
    try:
        min_len = int(input("Enter the Minimum length: "))
        if min_len > 0:
            break
        else:
            print("Please enter a positive integer.")
    except ValueError:
        print("Invalid input. Please enter a number.")

has_num = input("Do you want to have Numbers? (y/n): ").lower() == "y"
has_spec = input("Do you want to have Special Characters? (y/n): ").lower() == "y"

pwd = gen_passwd(min_len, has_num, has_spec)
print("Your Password is:", pwd)