#!/usr/bin/python
import socket
import sys

print(sys.argv)

if (len(sys.argv) != 2 or not sys.argv[1].isdigit()):
  print ('Usage: listen <port>',)
  exit()

p = int(sys.argv[1])
l = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', p))
s.listen(1)
while 1:
  (c, a) = s.accept()
  l.append(c)
  print ('%d: connection from %s') % (len(l), a) 