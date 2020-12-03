import sys
import hashlib

def encrypt(arg,password):
    g = open((arg+".crypted"),"at",encoding="utf-8")  
    m = hashlib.sha1()
    f = open(arg,"rb")
    while True:
        data = f.read(4096)
        if len(data)==0: break
        m.update(data)
    f.close()
    has=m.hexdigest()
    print(has)
    g.write(str(has) + '\n')
    with open(arg,encoding="utf-8") as f:
        for line in f:   
            i = 0
            newText = ''
            for char in line:
                newChar = ord(char) + ord(password[ i % len(password)]) #vezi cerinta pt detalii
                if newChar > 255: #tratez cazul in care suma >255; trunchiez sirul la primii 8 biti
                    binary = bin(newChar)
                    binary = binary[:len(binary)] 
                    newChar = int(binary,2)
                newText = newText + chr(newChar)
                i =+ 1 #index pentru caracterul curent
            g.write(newText)
    g.close()
    f.close()
    print("Done encrypting.")
