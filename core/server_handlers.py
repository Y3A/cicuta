#!/usr/bin/python

import random
import string
from core.utils import *
from core.listener import *
from core.interact import *
from core.listeners.http import http_server

def cct_help(arg):
    normal("CCT Server Help")
    normal("    help: print this help message")
    normal("        help -- print help")
    normal("")
    normal("    exit: exit and shut down server")
    normal("        exit -- exit server")
    normal("")
    normal("    agents: interact/list/kill connected agents")
    normal("        agents -- list connected agents")
    normal("        agents -i ID -- interact with agent with agent id of ID")
    normal("        agents -k ID -- kill agent with agent id of ID")
    normal("        agents -k * -- kill all agents")
    normal("")
    normal("    listeners: create/list/kill listeners")
    normal("        listeners -- list listeners")
    normal("        listeners -t http -p PORT -- create http listener on port PORT")
    normal("        listeners -t http -p PORT -n test -h 127.0.0.1 -- create http listener on port PORT with name 'test' and bound to localhost")
    normal("        listeners -k ID -- kill listener with id of ID, including all connected agents")
    return

def cct_exit(arg):
    kill_all_listeners()
    return "exit"

def cct_agents(arg):
    if len(arg) == 0:
        show_agents()
        return
    
    if "-k" in arg and "-i" in arg:
        warn("[-] Check help menu, -k cannot be used with interact")
        cct_help("")
        return

    if "-k" in arg:
        # kill all agents
        tokill = arg[arg.index("-k") + 1]
        if tokill == "*":
            if kill_all_agents():
                success(f"[+] All agents have been shutdown")
            else:
                warn(f"[-] One or more agent shutdown unsuccessful")
            return

        # kill agent by id
        tokill = int(tokill)    
        if kill_agent(tokill):
            success(f"[+] Agent {tokill} has been shutdown")
        else:
            warn(f"[-] Agent {tokill} is not found or shutdown unsuccessful")
        return

    if "-i" in arg:
        tointeract = int(arg[arg.index("-i") + 1])
        agent_interact(tointeract)

    return

def cct_listeners(arg):

    if len(arg) == 0:
        # list listeners
        show_listeners()
        return

    if "-k" in arg and ("-p" in arg or "-t" in arg or "-n" in arg or "-h" in arg):
        warn("[-] Check help menu, -k cannot be used with creation arguments")
        cct_help("")
        return

    if "-k" in arg:
        # kill listener
        tokill = int(arg[arg.index("-k") + 1])
        if kill_listener(tokill):
            success(f"[+] Listener {tokill} has been shutdown")
        else:
            warn(f"[-] Listener {tokill} is not found or shutdown unsuccessful")
        return

    # creation
    if "-p" not in arg or "-t" not in arg:
        warn("[-] Required arguments to create listener: TYPE, PORT")
        return

    listener_type = arg[arg.index("-t") + 1].lower()
    if listener_type not in supported_listeners:
        warn(f"[-] {listener_type} listener not supported")
        warn("[*] Currently supported listeners: ")
        for i in supported_listeners:
            warn("  " + i)
        return

    port = int(arg[arg.index("-p") + 1])
    if not check_port(port):
        warn(f"[-] Port {port} is already bound to a listener!")
        return

    if "-n" in arg:
        name = arg[arg.index("-n") + 1]
    else:
        name = "".join(random.choices(string.ascii_letters + string.digits, k=8))
    if "-h" in arg:
        host = arg[arg.index("-h") + 1]
    else:
        host = "0.0.0.0"
    
    if listener_type == "http":
        cur = Http_Listener(host, port, name, http_server.run)
    else:
        return

    success(f"[+] {cur.listener_type} listener with id {cur.listener_id} created")

    return

jumptable = {}
jumptable["cct_help"] = cct_help
jumptable["cct_exit"] = cct_exit
jumptable["cct_agents"] = cct_agents
jumptable["cct_listeners"] = cct_listeners

def execute(cmd, arg):
    try:
        return jumptable[cmd](arg)
    except Exception as e:
        #print(e)
        #cct_help("")
        warn("[-] Invalid option, check help")
        return None