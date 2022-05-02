import json

def load_abi(filename):
    with open(filename, 'r') as f:
        abi = json.load(f)
    return abi
