#!/usr/bin/python

from tabulate import tabulate
import time

supported_listeners = ["http"]
listener_id = 0

class Pool:
    def __init__(self):
        self.buf = []

    def add(self, obj):
        self.buf.append(obj)
    
    def remove(self, obj):
        self.buf.remove(obj)

    def get_pool(self):
        return self.buf

class Listeners_Pool(Pool):
    def __init__(self):
        super().__init__()

    def get_listener_by_id(self, listener_id):
        listener_obj = None
        for listener in self.get_pool():
            if int(listener.listener_id) == int(listener_id):
                listener_obj = listener
                break
        return listener_obj

    def add_agent_by_listener_id(self, listener_id, agent):
        for listener in self.get_pool():
            if int(listener.listener_id) == int(listener_id):
                listener.connected_agents.add(agent)

    def get_id_by_port(self, port):
        for listener in self.get_pool():
            if int(listener.port) == int(port):
                return listener.listener_id

class Agents_Pool(Pool):
    def __init__(self):
        super().__init__()

listeners_pool = Listeners_Pool()

class Listener:
    def __init__(self, name):
        global listener_id

        self.name = name
        self.thread = None
        self.listener_id = listener_id
        listener_id += 1
        listeners_pool.add(self)

        self.connected_agents = Agents_Pool()

    def shutdown(self):
        listeners_pool.remove(self)

class Http_Listener(Listener):
    def __init__(self, host, port, name, run):
        super().__init__(name)
        self.listener_type = "http"
        self.port = port
        self.thread = run(host, port)

    def shutdown(self):
        for agent in self.connected_agents.get_pool():
            try:
                agent.shutdown()
            except Exception as e:
                print(e)

        if self.thread:
            try:
                self.thread.terminate()
                self.thread.join()
            except Exception as e:
                print(e)

def show_agents():
    display = []
    for listener in listeners_pool.get_pool():
        for agent in listener.connected_agents.get_pool():
            display.append([agent.agent_id, agent.agent_type, agent.ip, agent.callback, round(time.time() - agent.lastcall), listener.listener_id])
    print(("\n\n" + tabulate(display, ["ID", "Type", "IP", "Callback(s)", "Last Callback(s)", "Listener ID"], "simple") + "\n\n"))
    return

def show_listeners():
    display = []
    for listener in listeners_pool.get_pool():
        display.append([listener.listener_id, listener.listener_type, listener.name, listener.port, len(listener.connected_agents.get_pool())])
    print(("\n\n" + tabulate(display, ["ID", "Type", "Name", "Port", "Connected Agents"], "simple") + "\n\n"))
    return

def kill_listener(listener_id):
    for listener in listeners_pool.get_pool():
        if int(listener.listener_id) == int(listener_id):
            listener.shutdown()
            listeners_pool.remove(listener)
            return True
    return False

def kill_agent(agent_id):
    for listener in listeners_pool.get_pool():
        for agent in listener.connected_agents.get_pool():
            if int(agent.agent_id) == int(agent_id):
                agent.shutdown()
                listener.connected_agents.remove(agent)
                return True
    return False

def kill_all_agents():
    for listener in listeners_pool.get_pool():
        while len(listener.connected_agents.get_pool()):
            for agent in listener.connected_agents.get_pool():
                agent.shutdown()
                listener.connected_agents.remove(agent)
    return True

def kill_all_listeners():
    for listener in listeners_pool.get_pool():
        listener.shutdown()
    return
