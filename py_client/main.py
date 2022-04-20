from threading import Thread

from serial import Serial
from serial.tools.list_ports import comports

from contacts import add_contact, list_contacts, remove_contact
from read import *
from send import *
from util import parse, warning

ports = comports()
for port, desc, hwid in sorted(ports):
    print("{}: {} [{}]".format(port, desc, hwid))

SER_PORT = input("PORT: ")
SER_BAUDRATE = 115200

ser = Serial(SER_PORT, SER_BAUDRATE, timeout=5)

thread_running = True

def read_loop():
    global thread_running

    while thread_running:
        if ser.in_waiting:
            read_messages(1, ser=ser)
            line = ser.readline()
            print("INCOMING:", line)
        sleep(1)

def user_loop():
    while True:
        inp = input("> ")
        args = parse(inp)
        cmd = args.pop(0).lower()

        if cmd in COMMANDS.keys():
            COMMANDS[cmd](*args, ser=ser)
        elif cmd == "exit":
            exit()
        else:
            warning("That command was not found. Use \"help\" to see all commands.")

# def read_messages(*args, **kwargs):
#     pass

# def list_commands(*args, **kwargs):
#     pass

# def exit_loop(*args, **kwargs):
#     print("ehj")
#     thread_running = False

COMMANDS = {
    "send": send_message,
    "read": read_messages,
    "list": list_contacts,
    "cadd": add_contact,
    "crmv": remove_contact,
    # "help": list_commands,
    # "stop": exit_loop 
}

if __name__ == "__main__":    
    t1 = Thread(target=read_loop)
    t2 = Thread(target=user_loop)

    t1.start()
    t2.start()

    t2.join()  # interpreter will wait until your process get completed or terminated
    thread_running = False
    print('The end')


    