#!/usr/bin/python

import readline
from core.listener import *
from core.utils import *
from core.interact_handlers import execute

def agent_interact(agent_id):
    agent_obj = None
    for listener in listeners_pool.get_pool():
        for agent in listener.connected_agents.get_pool():
            if agent.agent_id == agent_id:
                    agent_obj = agent
                    break
    
    if agent_obj:
        success(f"[+] Interacting with agent {agent_id}")
    else:
        warn(f"[-] Agent {agent_id} does not exist")
        return
    
    readline.set_completer(completer_interact)
    readline.parse_and_bind("tab: complete")

    context = CTX_INTERACT
    state.update(agent_id)

    while True:
        while not agent_obj.no_res():
            success("[+] Agent called back!")
            print(agent_obj.get_res())

        buf = prompt(f"agent {agent_id} > ", "white")
        readline.write_history_file(".cct_history")
        buf = buf.strip()
        buf = buf.split()
        if len(buf) < 1:
            continue
        cmd = buf[0]
        arg = buf[1:]
        if execute(context + cmd, arg, agent_obj) == "back":
            break