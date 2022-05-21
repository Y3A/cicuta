import pyfiglet
from termcolor import colored

def show():
    title = pyfiglet.figlet_format("CICUTA SERVER")
    print(colored(title, "blue"))