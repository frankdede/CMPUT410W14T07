#!/bin/bash
_username=""
echo -e "USEAGE:"
echo -e "ssh user@localhost -p 41070"
echo -n "Enter your username:"
read _username
echo "http://localhost:41078"

ssh \
  -L 41070:cs410.cs.ualberta.ca:41070 \
  -L 41078:cs410.cs.ualberta.ca:41078 \
$_username@ohaton.cs.ualberta.ca
