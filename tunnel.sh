#!/bin/sh

echo "USEAGE:"
echo "ssh user@localhost:41070"
echo "http://localhost:41078"

ssh \
  -L 41070:cs410.cs.ualberta.ca:41070 ohaton.cs.ualberta.ca \
  -L 41078:cs410.cs.ualberta.ca:41078 ohaton.cs.ualberta.ca \
-l user
