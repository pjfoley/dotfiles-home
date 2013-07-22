#!/usr/bin/env python
# encoding: utf-8

import argparse, string, random, crypt
from collections import namedtuple

# Tuple == (Hash Method, Salt Length, Magic String, Hashed Password Length)
hash_fields = namedtuple('hash_fields', ['len_salt', 'hash_sig', 'passwd_len'])

supported_hashes = {
    "crypt": hash_fields(2,'',13), 
    "md5": hash_fields(8,'$1$',22), 
    "sha256": hash_fields(16,'$5$',43), 
    "sha512": hash_fields(16,'$6$',86)
}

parser = argparse.ArgumentParser(description='Generate an encrypted password.')
parser.add_argument('--hash', default='sha512', choices=supported_hashes, help='Which Hash function to use')
parser.add_argument('-s', '--salt', help='Salt to use with Password')
parser.add_argument('-d', '--debug', action='store_true', help='Output some useful Debug Information')
parser.add_argument('password')

# Get command arguments
args = parser.parse_args()
# Get crypt hash arguments
l_crypt_hash = supported_hashes[args.hash]

# Valid Character set to choose from for Random Salt, remove dollar sign which has special meaning to the hashing function
set_rand_values = string.letters + string.digits + string.punctuation.replace("$","")

if not args.salt:
    salt_word = ''.join((random.choice(set_rand_values)) for x in range(l_crypt_hash.len_salt))
else:
    if len(args.salt) > l_crypt_hash.len_salt:
      print "Salt is too long, will only use the first", l_crypt_hash.len_salt, "characters."
      salt_word = args.salt[:l_crypt_hash.len_salt]
    elif len(args.salt) < l_crypt_hash.len_salt:
      print "Your salt is too short, will pad your salt with", l_crypt_hash.len_salt - len(args.salt), "random characters."
      salt_word = args.salt + ''.join((random.choice(set_rand_values)) for x in range(l_crypt_hash.len_salt - len(args.salt)))
    else:
      salt_word = args.salt

hashed_pwd = crypt.crypt(args.password, "".join((l_crypt_hash.hash_sig, salt_word)))

if args.debug:
  print ""
  print "Debug Information:"
  print "    - Command Arguments      :", args
  print "    - Random char set        :", set_rand_values
  print "    - Crypt"
  print "       - Type                :", args.hash
  print "       - Hash Signal         :", l_crypt_hash.hash_sig
  print "    - Salt"
  print "       - Passed              :", args.salt
  print "       - Length Needed       :", l_crypt_hash.len_salt
  print "       - Length Passed       :", len(args.salt) if args.salt else 0
  print "       - Salt to use         :", salt_word
  print "    - Password"
  print "       - Required Hashed len :", l_crypt_hash.passwd_len
  print "       - Hashed Password len :", len(hashed_pwd) - len(salt_word) - len(l_crypt_hash.hash_sig) - 1 # Remove extra $ added as part of Hash Function
  print ""
else:
  print "Salt Used:"
  print salt_word
  print ""

print "Hashed Password:"
print hashed_pwd
