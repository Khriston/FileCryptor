import sys
import hashlib
import os

def encrypt(arg,password):
    g = open((arg+".crypted"),"at")  
    m = hashlib.sha1()
    f = open(arg,"rb")
    while True:
        data = f.read(4096)
        if len(data)==0: break
        m.update(data)
    f.close()
    has=m.hexdigest()
    #print(has)
    g.write(has)
    g.close()
    g = open((arg+".crypted"),"ab")
    with open(arg, "rb") as f:
        i = 0  
        limit = len(password)
        byte = f.read(1)
        while byte:
            #print(byte)
            newChar = ord(byte) + ord(password[ i % limit])
            if newChar > 255: #tratez cazul in care suma >255; trunchiez sirul la primii 8 biti
                newChar = newChar & 255
            #print(str(byte)+" " + str(ord(byte))+" "+ str(newChar))
            i += 1 #index pentru caracterul curent
            g.write(newChar.to_bytes(1,'little'))
            byte = f.read(1)
    g.close()
    print("Done encrypting.")

def decrypt(arg,password):
    if ".crypted" not in arg:
        print("Wrong filetype. Needs to be <.crypted>.")
        return 0
    m = hashlib.sha1()
    g = open(arg[:-8],"ab")
    f = open(arg,"rb")
    i=40
    original = ""
    while i>0:
        original += chr(ord(f.read(1)))
        i = i - 1
    limit = len(password)
    i = 0 
    byte = f.read(1)
    while byte:
        newChar = ord(byte) - ord(password[ i % limit])
        if newChar < 0: #tratez cazul in care diff<0
            newChar = 256 + newChar 
        #print(chr(newChar)+" "+str(newChar))#+" "+str(prevChar))
        i += 1 #index pentru caracterul curent
        #print(str(byte)+" " + str(ord(byte))+" " + str(newChar)+" "+str(newChar.to_bytes(1,'big')))
        m.update(newChar.to_bytes(1,'big'))
        g.write(newChar.to_bytes(1,'big'))
        #print(newChar.to_bytes(2,'little'))
        byte = f.read(1)
    f.close()
    g.close()
    #print(str(m.hexdigest()).strip()+" "+str(original).strip())
    if str(m.hexdigest()).strip() == str(original).strip():
        print("Done decrypting.")
    else:
        print("Wrong password.")
        #os.remove(arg[:-8])

def command(arg):
    if arg=="encrypt":
        encrypt(sys.argv[2],sys.argv[3])
    elif arg=="decrypt":
        decrypt(sys.argv[2],sys.argv[3])
    else:
        print('Wrong command. Use "encrypt" or "decrypt".')
    return 0
    
command(sys.argv[1])
