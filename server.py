#!/usr/bin/python

import signal
import readline
import os
import sys
from core import banner
from core.server_handlers import execute
from core.utils import *

# Disable ctrl-c
def ctrlc(sig, frame):
    pass
signal.signal(signal.SIGINT, ctrlc)

# Initialize history file
if not os.path.isfile(".cct_history"):
    open(".cct_history", "a").close()
else:
    readline.read_history_file(".cct_history")

readline.set_completer(completer)
readline.parse_and_bind("tab: complete")

# disable output buffering
class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def writelines(self, data):
        self.stream.writelines(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

sys.stdout = Unbuffered(sys.stdout)

# Print banner
banner.show()

# Main server
while True:
    context = CTX_CCT
    readline.set_completer(completer)
    readline.parse_and_bind("tab: complete")
    state.update(STATE_SERVER)
    buf = prompt("cct > ", "white")
    readline.write_history_file(".cct_history")
    buf = buf.strip()
    buf = buf.split()
    if len(buf) < 1:
        continue
    cmd = buf[0]
    arg = buf[1:]
    if execute(context + cmd, arg) == "exit":
        break