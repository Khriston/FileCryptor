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
    
def decrypt(arg,password):
    if ".crypted" not in arg:
        print("Wrong filetype. Needs to be <.crypted>.")
        return 0
    m = hashlib.sha1()
    g = open(arg[:-8],"at",encoding="utf-8")
    with open(arg,encoding="utf-8") as f:
        flag = 1
        for line in f:   
            if flag:
                original = line
                flag = 0
            else:
                i = 0
                newText = ''
                for char in line:
                    newChar = ord(char) - ord(password[ i % len(password)]) #vezi cerinta pt detalii
                    if newChar < 0: #tratez cazul in care diff<0
                        newChar = 255 + newChar
                    newText += str(chr(newChar))
                    i =+ 1 #index pentru caracterul curent
                m.update(newText.encode('utf-8'))
                g.write(newText)
    f.close()
    g.close()
    if str(m.hexdigest()).strip() == str(original).strip():
        print("Done decrypting.")
    else:
        print("Wrong password.")
        
def command(arg):
    if arg=="encrypt":
        encrypt(sys.argv[2],sys.argv[3])
    elif arg=="decrypt":
        decrypt(sys.argv[2],sys.argv[3])
    else:
        print('Wrong command. Use "encrypt" or "decrypt".')
    return 0
    
command(sys.argv[1])
