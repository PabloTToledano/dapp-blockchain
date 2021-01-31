import json
from web3 import Web3
from web3.auto.gethdev import w3
from web3.middleware import geth_poa_middleware
from solc import compile_standard


w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
print(w3.isConnected())
print(w3.clientVersion)

compiled_sol = compile_standard({
    "language": "Solidity",
    "sources": {
        "Greeter.sol": {
            "content": '''
                    pragma solidity >=0.5.0;
   
                    contract Greeter {
                      string public greeting;
   
                      constructor() public {
                          greeting = 'Hello';
                      }
   
                      function setGreeting(string memory _greeting) public {
                          greeting = _greeting;
                      }
   
                      function greet() view public returns (string memory) {
                          return greeting;
                      }
                    }
                  '''
        }
    },
    "settings":{
        "outputSelection": {
            "*": {
                "*": [
                "metadata", "evm.bytecode"
                , "evm.bytecode.sourceMap"
                ]
            }
        }
    }
})


w3.eth.defaultAccount = w3.eth.accounts[0]
bytecode = compiled_sol['contracts']['Greeter.sol']['Greeter']['evm']['bytecode']['object']
abi = json.loads(compiled_sol['contracts']['Greeter.sol']['Greeter']['metadata'])['output']['abi']
Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Greeter.constructor().transact()
print(tx_hash)
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(tx_receipt)
