#!/usr/bin/python

import socket
from termcolor import colored

# states
# server is -1, positive integer represents agent id
STATE_SERVER = -1

class State:
    def __init__(self):
        self.state = STATE_SERVER
    
    def get(self):
        return self.state

    def update(self, state):
        self.state = state
        return

state = State()

# contexts
CTX_CCT = "cct_"
CTX_INTERACT = "interact_"

cct_commands = [
    "help", "exit", "agents", "listeners"
    ]

cct_interact_commands = [
    "help", "back", "clear", "shell",
    "download", "upload", "sleep", "tasks"
    ]

def completer(text, state):
    options = [i for i in cct_commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def completer_interact(text, state):
    options = [i for i in cct_interact_commands if i.startswith(text)]
    if state < len(options):
        return options[state]
    else:
        return None

def prompt(text, color):
    return input(colored(text, color))

def warn(text):
    print(colored(text, "red"))

def normal(text):
    print(colored(text, "white"))

def success(text):
    print(colored(text, "green"))

def check_port(port):
    with socket.socket() as s:
        return s.connect_ex(("localhost", port)) != 0

class Queue:
    def __init__(self):
        self.buf = []
    
    def enqueue(self, data):
        self.buf.append(data)

    def dequeue(self):
        return self.buf.pop(0)

    def is_empty(self):
        return not len(self.buf)

    def get_buf(self):
        return self.buf