
import socket
import os
import shutil
import time
import base64
import subprocess
import random
import sys
from Crypto.Cipher import AES

def encode_to_base64(s):
    key_bytes = s.encode('ascii')
    base64_bytes = base64.b64encode(key_bytes)
    pub_key = base64_bytes.decode('ascii')
    return pub_key

def decode_to_base64(s):
    key_bytes = s.encode('ascii')
    base64_bytes = base64.b64decode(key_bytes)
    pub_key = base64_bytes.decode('ascii')
    return pub_key


passphrase="1234567891234566"
username="kshitiji"                           # IN case of a new username, be sure to put that name here, and run program once, to put file in UserCredentials
salt="12341234"

salt_2=""
salt_2=salt+"00000000"

# subprocess.run(["rm","-r","UserCredentials"])
# subprocess.run(["mkdir","UserCredentials"])
with open("in.txt","w") as fd:
    fd.write("0000000000000000")
subprocess.run(["openssl","enc","-aes-128-cbc","-in","in.txt","-K",passphrase,"-iv",salt_2 ,"-out","encrypted_password"])
pswd="".encode('latin1')
with open("encrypted_password","rb") as fd:
    pswd+=fd.read()

os.chdir("./UserCredentials")
#print("pswd: ",pswd)
pswd2=pswd.decode('latin1')
#print("pswd2: ",pswd2)
with open(username,"w") as fd:
    fd.write(username+"\n")
    fd.write(encode_to_base64(salt)+"\n")
    fd.write(pswd2)
    fd.write("\n")


os.chdir("../")


s = socket.socket()
#print ("Socket successfully created")

port = sys.argv[1]
port=(int)(port)

s.bind(('', port))
print ("Server binded to %s" %(port))

s.listen(5)
#print ("socket is listening")

c, addr = s.accept()
print ('Server got connected to client- ', addr )

#subprocess.run(['cp','serverkeys/serverpub.txt','serverpub.txt'])
shutil.copyfile("serverkeys/serverpub.txt","serverpub.txt")
server_public_key=""                             # normal key
with open("serverpub.txt","r") as fd:
    server_public_key=fd.read()


key_bytes = server_public_key.encode('ascii')
base64_bytes = base64.b64encode(key_bytes)
pub_key = base64_bytes.decode('ascii')          # base64 encoded key

time.sleep(2)
xx=pub_key+salt_2
c.send(xx.encode())

x=c.recv(1024)
#x=x.decode('latin1')                   # msg sent by client to server shud always be encoded in latin1 format


with open("in.txt","wb") as fd:
    fd.write(x)

#print("x: ",x)

subprocess.run(['cp','serverkeys/serverpriv.txt','serverpriv.txt'])
subprocess.run(['./rsa_decrypt_client_message_at_server'])

client_msg=""
with open("client_message_at_server","r") as fd:
    client_msg=fd.read()

user_2=""
pass_2=""
Ks=""

# for i in range(0,len(client_msg)):
#     if (ord(client_msg[i])>ord('a') and ord(client_msg[i])>ord('z')) or (ord(client_msg[i])>ord('A') and ord(client_msg[i])>ord('Z')):
#         user_2+=client_msg[i]
#     else:
#         break
user_2=client_msg[:8]   # user_2 has 8 characters
Ks=client_msg[-32:]
pass_2=client_msg[8:-32]

print("Username got from client message: ",user_2)
print("Passphrase got from client message: ",pass_2)
print("Secret key got from client message: : ",Ks)

with open("in.txt","w") as fd:
    fd.write("0000000000000000")
subprocess.run(["openssl","enc","-aes-128-cbc","-in","in.txt","-K",pass_2,"-iv",salt_2 ,"-out","encrypted_password"])
ps="".encode('latin1')
with open("encrypted_password","rb") as fd:
    ps+=fd.read()
print("Password corresponding to passphrase of client message: ",ps.decode('latin1'))

if not(os.path.exists("./UserCredentials/"+user_2)):
    c.send("NOK".encode())
    exit()

with open("./UserCredentials/"+user_2,"r") as fd:
    lines=fd.readlines()
    user_3=lines[0]
    salt_3=lines[1]
    pswd3=""
    for i in range(2,len(lines)):
        pswd3+=lines[i]

    pswd3=pswd3[:len(pswd3)-1]
    #print("ps.decode('latin1'): ",ps.decode('latin1'))
    print("Password corresponding to passphrase of user specified by client ",pswd3)
    if pswd3==ps.decode('latin1'):
        #print("SAME!!!")
        print("Authenticated...")
        c.send("OK".encode())
    else:
        print("Not Valid...")
        # print("NOT SAME!!!")
        # pss=ps.decode('latin1')
        # print("len(pss): ",len(pss))
        # print("len(pswd3): ",len(pswd3))
        # for i in range(0,len(pss)):
        #     if pss[i]!=pswd3[i]:
        #         print("pss[i]: ",pss[i])
        #         print("pswd3[i]: ",pswd3[i])
        #         break
        c.send("NOK".encode())


# # a forever loop until we interrupt it or
# # an error occurs
while True:

    x=c.recv(1024)
    nonce=x[:16]
    tag=x[-16:]
    ciphertext=x[16:-16]

    key = Ks.encode()
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt(ciphertext)

    # print(plaintext)
    # print("")

    x=plaintext.decode()
    y=""
    print(x)                       # printing command from client
    print("")

    if x=="ls":
        yy=os.listdir()
        y+='['
        for xx in yy:
            y+="'"+xx+"', "
        y+=']'

    elif x=="pwd":
        y=os.getcwd()


    elif x[:2]=="cd":
        os.chdir(x[3:])
        y="NOTHING"

    elif x[:2]=="mv":
        l=[]
        for i in range(0,len(x)):
            if x[i]==" ":
                l.append(i)
        #print("l: ",l)

        y1=x[l[0]+1:l[1]]    # file
        y2=x[l[1]+1:l[2]]    # source directory having file
        y3=x[l[2]+1:]        # destination directory

        # print("y1: ",y1)
        # print("y2: ",y2)
        # print("y3: ",y3)

        shutil.move(y2+"/"+y1,y3)

        y="NOTHING"

    elif x[:2]=="cp":
        l=[]
        for i in range(0,len(x)):
            if x[i]==" ":
                l.append(i)

        y1=x[l[0]+1:l[1]]             # path of source file
        y2=x[l[1]+1:]                 # path of destination file

        shutil.copyfile(y1,y2)

        y="NOTHING"


    elif x=="logout":
        break


    data=y.encode()
    Ks_2=Ks.encode()
    cipher = AES.new(Ks_2, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(data)
    xx=nonce+ciphertext+tag
    c.send(xx)

# Close the connection with the client
print("Exiting...")
c.close()
