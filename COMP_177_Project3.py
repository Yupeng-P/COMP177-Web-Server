#!/bin/env python3

from socket import *
import sys
import threading
import time
import ctypes


# Fucntion check for validation of user and password
def auth():
  username = input('Please enter a username: ')
  password = input('Please enter a password: ')

	# Send the username and password to server to check for validation
  msg = "AUTH:" + username + ":" + password

  s.send(msg.encode())
	# Check for server's reply
  returnMsg1 = s.recv(1024)
  returnMsg1 = returnMsg1.decode()
  # If username and/or password is not validated
  if (returnMsg1 == "AUTHNO\n"):
    print("Incorrect username and/or password\n")
	# If username and password is validated
    auth()
  else:
    print("You are now authenticated\n")
    main()

    
# Function for receieving message
def worker(event1):    # flag
  try:
    # If flag is not set, then receive message from server
    while not event1.is_set():
        receMsg = s.recv(1024)
        receMsg = receMsg.decode()
        # Put the receMsg into the list 
        my_list.append(receMsg)
        # Formatting receieving messages 
        if "FROM" in receMsg:
          print("Incoming message", receMsg)
        elif receMsg.startswith("SIGN", 0, 7):
          print("Update:",receMsg)
        else:
          print("Online user:",receMsg)
  except OSError:
    return


# Main function
def main():
    # Create a thread
    thread = threading.Thread(target=worker, args=(event1,))
    thread.start()
    sending()
    thread.join()

# Function for user's option
def sending():
            ans = input("""
		    Choose an option:
		    1. List online users
		    2. Send someone a message
		    3. Sign off
		    """)
            # If user input == 1
            if ans == "1":
                cmd1 = 'LIST'    # Send LIST to server
                s.send(cmd1.encode())
                sending()
                return
            # If user input == 2
            elif ans == "2":
                # Enter who you want to message
                mesUser = input('User you would like to message: ')
                # If user is online 
                if any(mesUser in i for i in my_list):
                    cmd2 = input('Message: ')
                    message = 'TO:' + mesUser + ':' + cmd2
                    s.send(message.encode())
                    print('Message sent')
                    sending()
                    return
                  # If user is not online 
                else:
                    print("User is not online, please choose again")
                    sending()
            # If user input is 3
            elif ans == "3":
                # Send goodbye to the server
                cmd3 = "BYE"
                s.send(cmd3.encode())
                event1.set()
                s.close()
            # If user input is not those 3 above
            else:
                print("Not Valid Choice Try again")
                sending()
                return

# A list to store messages from server
my_list = []
ip = 'localhost' 	#input('Please enter the server address: ')
port = 13001 #int(input('Please enter the server port number: '))
event1 = threading.Event()
event1.clear()


# Assign ip addr and port to addr
addr = (ip, port)

# Create socket
s = socket(AF_INET, SOCK_STREAM)
s.connect(addr)

# Send a greeting message to the server
string_unicode = "HELLO"
raw_bytes = bytes(string_unicode, 'ascii')
s.send(raw_bytes)

# Recieve the reply from server
receMsg1 = s.recv(1024)
receMsg1 = receMsg1.decode()
auth()


