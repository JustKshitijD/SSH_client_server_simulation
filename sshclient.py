# first of all import the socket library
import socket
import os
import shutil
import time
import base64
import random
import subprocess
from Crypto.Cipher import AES

passphrase="1234567891234566"    # make passphrase as 16 bytes. This will be key of 00...0 to generate password.
salt_2=""

s2 = socket.socket()   # FOR SERVER

print ("Socket successfully created")

server_port=0
server_ip="127.0.0.1"              # localhost by default

flag=False
Ks=""

while True:
    val = input()
    #print("val: ",val)
    x=val

    if x[:3]=="ssh":
        l=[]
        for i in range(0,len(x)):
            if x[i]==" ":
                l.append(i)
        print("l: ",l)
        if len(l)==2:
            server_port=int(x[l[0]+1:l[1]])
            username=x[l[1]+1:]
            print("Server's IP: ",server_ip)
            print("Server's port: ",server_port)
            # connect to the server on local computer
            s2.connect((server_ip, int(server_port)))

            xx=s2.recv(1024)
            xx=xx.decode()

            salt_2=xx[-16:]
            server_public_key=xx[:-16]

            with open('server_pub.txt',"w") as fd:            # stored in base64 format
                fd.write(server_public_key)

            key_bytes = server_public_key.encode('ascii')
            base64_bytes = base64.b64decode(key_bytes)
            pub_key = base64_bytes.decode('ascii')

            with open('server_pub_non_base64.txt',"w") as fd:            # stored in base64 format
                fd.write(pub_key)

            Ks=""
            for i in range(0,32):                                        # generate Ks
                Ks+=str(random.randint(0,9))

            print("Secret Key: ",Ks)

            msg_for_server=""
            msg_for_server+=username
            msg_for_server+=passphrase
            msg_for_server+=Ks

            with open('in.txt',"w") as fd:            # stored in base64 format
                fd.write(msg_for_server)

            encoded_msg_for_server="".encode("latin1")
            subprocess.run(['./rsa_encrypt_client_message'])

            with open("rsa_encrypted_message_for_server","rb") as fd:
                encoded_msg_for_server=fd.read()

            #print("encoded_msg_for_server: ",encoded_msg_for_server)
            print("Username+Passphrase+Secret_Key encoded message to be sent to server: ",msg_for_server)

            s2.send(encoded_msg_for_server)

            ok_msg=s2.recv(1024)                                   # get OK or NOK fromm server
            ok_msg=ok_msg.decode()
            if ok_msg=="NOK":
                print("NOK....")   #INVALID (USERNAME,PASSWORD)
                print("Exiting....")
                s2.close()
                break
            elif ok_msg=="OK":
                print("OK...")
                flag=True
                continue


        elif len(l)==3:
            server_ip=x[l[0]+1:l[1]]
            server_port=x[l[1]+1:l[2]]
            username=x[l[2]+1:]
            # connect to the server on local computer
            print("Server's IP: ",server_ip)
            print("Server's port: ",server_port)
            s2.connect((server_ip, int(server_port)))
            server_public_key=s2.recv(1024)
            server_public_key=server_public_key.decode()
            with open('server_pub.txt',"w") as fd:            # stored in base64 format
                fd.write(server_public_key)

            key_bytes = server_public_key.encode('ascii')
            base64_bytes = base64.b64decode(key_bytes)
            pub_key = base64_bytes.decode('ascii')

            with open('server_pub_non_base64.txt',"w") as fd:            # stored in base64 format
                fd.write(pub_key)

            Ks=""
            for i in range(0,32):
                Ks+=str(random.randint(0,9))

            print("Secret Key: ",Ks)

            msg_for_server=""
            msg_for_server+=username
            msg_for_server+=passphrase
            msg_for_server+=Ks

            #print("msg_for_server: ",msg_for_server)

            with open('in.txt',"w") as fd:            # stored in base64 format
                fd.write(msg_for_server)

            encoded_msg_for_server="".encode("latin1")

            subprocess.run(['./rsa_encrypt_client_message'])
            with open("rsa_encrypted_message_for_server","rb") as fd:
                encoded_msg_for_server=fd.read()

            print("Username+Passphrase+Secret_Key encoded message to be sent to server: ",msg_for_server)

            s2.send(encoded_msg_for_server)

            ok_msg=s2.recv(1024)
            ok_msg=ok_msg.decode()
            if ok_msg=="NOK":
                print("NOK....")   #INVALID (USERNAME,PASSWORD)
                print("Exiting....")
                s2.close()
                break
            elif ok_msg=="OK":
                flag=True
                print("OK")
                continue

    elif x=="listfiles":
        if flag==False:
            print("Not authenticated with server yet...")
            break
        else:
            Ks_2=Ks.encode()
            cipher = AES.new(Ks_2, AES.MODE_EAX)
            data="ls".encode()
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(data)
            xx=nonce+ciphertext+tag
            print("Msg_for_server: ",xx)
            s2.send(xx)
            x=s2.recv(1024)
            nonce=x[:16]
            tag=x[-16:]
            ciphertext=x[16:-16]

            key = Ks.encode()
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
            plaintext=plaintext.decode()

            print(plaintext)
            print("")


    elif x=="cwd":
        if flag==False:
            print("Not authenticated with server yet...")
            break
        else:
            data="pwd".encode()
            Ks_2=Ks.encode()
            cipher = AES.new(Ks_2, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(data)
            xx=nonce+ciphertext+tag
            print("Msg_for_server: ",xx)
            s2.send(xx)
            x=s2.recv(1024)
            nonce=x[:16]
            tag=x[-16:]
            ciphertext=x[16:-16]

            key = Ks.encode()
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)
            plaintext=plaintext.decode()
            print(plaintext)
            print("")

    elif x[:5]=="chgir":
        if flag==False:
            print("Not authenticated with server yet...")
            break
        else:
            y=x[6:]
            x="cd "+y
            data=x.encode()
            Ks_2=Ks.encode()
            cipher = AES.new(Ks_2, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(data)
            xx=nonce+ciphertext+tag
            print("Msg_for_server: ",xx)
            s2.send(xx)
            x=s2.recv(1024)
            nonce=x[:16]
            tag=x[-16:]
            ciphertext=x[16:-16]

            key = Ks.encode()
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)

            plaintext=plaintext.decode()
            #print(plaintext)
            print("")

    elif x[:2]=="cp":
        if flag==False:
            print("Not authenticated with server yet...")
            break
        else:
            l=[]
            for i in range(0,len(x)):
                if x[i]==" ":
                    l.append(i)

            y1=x[l[0]+1:l[1]]             # path of source file
            y2=x[l[1]+1:]                 # path of destination file

            x="cp "+y1+" "+y2
            data=x.encode()
            Ks_2=Ks.encode()
            cipher = AES.new(Ks_2, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(data)
            xx=nonce+ciphertext+tag
            print("Msg_for_server: ",xx)
            s2.send(xx)
            x=s2.recv(1024)
            nonce=x[:16]
            tag=x[-16:]
            ciphertext=x[16:-16]

            key = Ks.encode()
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)

            plaintext=plaintext.decode()
            #print(plaintext)
            print("")

    elif x[:2]=="mv":
        if flag==False:
            print("Not authenticated with server yet...")
            break
        else:
            l=[]
            for i in range(0,len(x)):
                if x[i]==" ":
                    l.append(i)
            print("l: ",l)

            y1=x[l[0]+1:l[1]]    # file
            y2=x[l[1]+1:l[2]]    # source directory having file
            y3=x[l[2]+1:]        # destination directory

            # print("y1: ",y1)
            # print("y2: ",y2)
            # print("y3: ",y3)

            x="mv "+y1+" "+y2+" "+y3
            data=x.encode()
            Ks_2=Ks.encode()
            cipher = AES.new(Ks_2, AES.MODE_EAX)
            nonce = cipher.nonce
            ciphertext, tag = cipher.encrypt_and_digest(data)
            xx=nonce+ciphertext+tag
            print("Msg_for_server: ",xx)
            s2.send(xx)
            x=s2.recv(1024)
            nonce=x[:16]
            tag=x[-16:]
            ciphertext=x[16:-16]

            key = Ks.encode()
            cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
            plaintext = cipher.decrypt(ciphertext)

            plaintext=plaintext.decode()
            #print(plaintext)
            print("")

    elif x=="logout":
        print("Exiting...")
        data=x.encode()
        Ks_2=Ks.encode()
        cipher = AES.new(Ks_2, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        xx=nonce+ciphertext+tag
        s2.send(xx)
        break
