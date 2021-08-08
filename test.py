import os
import shutil
import subprocess
import shutil
from Crypto.Cipher import AES

print(os.getcwd())
print(os.listdir())

# x="cp /home/sayukta/Desktop/IITM_Courses_4th_year_2nd_sem/Network_Security/Assgns/assgn_deadlines.png /home/sayukta/Desktop/IITM_Courses_4th_year_2nd_sem/Network_Security/Assgns/Assgn4/assgn_deadlines.png"
#
# l=[]
# for i in range(0,len(x)):
#     if x[i]==" ":
#         l.append(i)
#
# y1=x[l[0]+1:l[1]]
# y2=x[l[1]+1:]
#
# shutil.copyfile(y1,y2)

# msg="".encode('latin1')
# with open("rsa_encrypted_message_for_server","rb") as fd:
#     msg=fd.read()
# print(msg)
# print("--------")
# print(msg.decode('latin1'))

# from Crypto.Cipher import AES
# key = b'12345678912345678912345678912345'
#
# cipher = AES.new(key, AES.MODE_EAX)
#
# data="HELLODY"
# data=data.encode()
# print(data)
#
# nonce = cipher.nonce
# ciphertext, tag = cipher.encrypt_and_digest(data)
#
# print("nonce: ",nonce)
# print("ciphertext: ",ciphertext)
# print("tag: ",tag)
# print("len(nonce): ",len(nonce))
# print("len(ciphertext): ",len(ciphertext))
# print("len(tag): ",len(tag))
# print(nonce+ciphertext+tag)
# print("-------")
#
#
# key = b'12345678912345678912345678912345'
# cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
# plaintext = cipher.decrypt(ciphertext)
#
# print("plaintext: ",plaintext)


shutil.copyfile("serverkeys/serverpub.txt","serverpub.txt")
