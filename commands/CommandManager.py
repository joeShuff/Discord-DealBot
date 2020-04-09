import os
import json

cwd = os.getcwd()

def load_commands_and_categories():
    with open(cwd + '/commands.json', 'r') as myfile:
        loaded_json = json.loads(myfile.read().replace('\n', ''))
        return loaded_json['commands'], loaded_json['categories']

def load_command_categories():
    with open(cwd + '/commands.json', 'r') as myfile:
        loaded_json = json.loads(myfile.read().replace('\n', ''))
        return loaded_json['categories']

def load_commands():
    with open(cwd + '/commands.json', 'r') as myfile:
        loaded_json = json.loads(myfile.read().replace('\n', ''))
        return loaded_json['commands']