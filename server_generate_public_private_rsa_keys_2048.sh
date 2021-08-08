#!/bin/bash
openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out serverpriv.txt
openssl pkey -in serverpriv.txt -out serverpub.txt -pubout
### Check if a directory does not exist ###
if [ ! -d "./serverkeys" ]
then
    mkdir serverkeys
fi
mv serverpriv.txt ./serverkeys
mv serverpub.txt ./serverkeys
