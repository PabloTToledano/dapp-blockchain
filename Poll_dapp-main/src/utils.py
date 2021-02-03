from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

SERVER_HOST = 'http://localhost:8545'
web3_socket = Web3(HTTPProvider(SERVER_HOST))
web3_socket.middleware_onion.inject(geth_poa_middleware, layer=0)

def clean_error_message(message):
    return str(message).replace("execution reverted: VM Exception while processing transaction: revert ", "")
