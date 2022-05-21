#!/usr/bin/python

from core.utils import *
from core.listener import *
import time

agent_id = 0

class Agent:
    def __init__(self, ip):
        global agent_id

        self.agent_id = agent_id
        agent_id += 1
        self.ip = ip
        self.task_queue = Queue()
        self.res_queue = Queue()
        self.callback = 60
        self.lastcall = time.time()

    def add_task(self, cmd):
        self.task_queue.enqueue(cmd)

    def get_task(self):
        return self.task_queue.dequeue()

    def get_task_queue(self):
        return self.task_queue.get_buf()

    def no_tasks(self):
        return self.task_queue.is_empty()

    def add_res(self, res):
        self.res_queue.enqueue(res)

    def get_res(self):
        return self.res_queue.dequeue()
    
    def no_res(self):
        return self.res_queue.is_empty()

    def shutdown(self):
        pass

    def set_callback(self, callback):
        self.callback = callback

    def set_lastcall(self, lastcall):
        self.lastcall = lastcall

class Http_Agent(Agent):
    def __init__(self, ip):
        super().__init__(ip)
        self.agent_type = "http"
        self.get_task_path = ""
        self.res_path = ""

    def shutdown(self):
        pass