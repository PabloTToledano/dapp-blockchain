from web3 import Web3, HTTPProvider

SERVER_HOST = 'http://localhost:8545'
web3_socket = Web3(HTTPProvider(SERVER_HOST))

def clean_error_message(message):
    return str(message).replace("execution reverted: VM Exception while processing transaction: revert ", "")
