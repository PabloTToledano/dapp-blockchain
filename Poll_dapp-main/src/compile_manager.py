import json
from solc import compile_standard
from os import path

class CompileManager:

    @staticmethod
    def compile(contract_path, contract_poll, contract_ownable):
        """ It compiles the poll solidity file into a dict with the bytecode, the abi and the necessary data to deploy a poll contract

        Args:
            contract_poll (string): It contains the solidity poll contract name
            contract_ownable (string): It contains the solidity ownable contract name
            contract_path (string): The folder where the solidity file is

        Returns:
            [dict]:
        """
        contract_poll_path = path.join(contract_path, contract_poll)
        with open(contract_poll_path, "r") as contract_file:
            content_poll = contract_file.read()
        
        contract_ownable_path = path.join(contract_path, contract_ownable)
        with open(contract_ownable_path, "r") as contract_file:
            content_ownable = contract_file.read()

        dict_to_compile = {
            "language": "Solidity",
            "sources": {
                contract_ownable : {
                    "content" : content_ownable
                },
                contract_poll : {
                    "content" : content_poll
                }
            },   
            "settings" : {
                "outputSelection": {
                    "*": {
                        "*": [
                            "metadata", "evm.bytecode"
                            , "evm.bytecode.sourceMap"
                        ]
                    }
                }
            }
        }
        compiled_sol = compile_standard(dict_to_compile)
        return compiled_sol


    @staticmethod
    def get_ABI(contract_path, contract_poll, contract_ownable):
        try:
            compiled_sol = CompileManager.compile(contract_path, contract_poll, contract_ownable)
            abi = json.loads(compiled_sol['contracts'][contract_poll][contract_poll[:-4]]['metadata'])['output']['abi']
            return abi
        except Exception:
            raise RuntimeError('ABI not generated correctly')
        

    @staticmethod
    def get_bytecode(contract_path, contract_poll, contract_ownable):
        try:
            compiled_sol = CompileManager.compile(contract_path, contract_poll, contract_ownable)
            bytecode = compiled_sol['contracts'][contract_poll][contract_poll[:-4]]['evm']['bytecode']['object']
            return bytecode
        except Exception:
            raise RuntimeError('Bytecode not generated correctly')
