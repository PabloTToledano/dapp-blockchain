from src.compile_manager import CompileManager
from src.utils import web3_socket
from src.poll import Poll


class PollFactory:

    @staticmethod
    def new_poll(poll_owner, poll_name):
        try:
            name = str(poll_name)
        except ValueError as e:
            raise RuntimeError("Introduce a string as a name of the poll")

        poll_ABI = CompileManager.get_ABI('poll_dapp/contracts', 'Poll.sol', 'Ownable.sol')
        bytecode = CompileManager.get_bytecode('poll_dapp/contracts', 'Poll.sol', 'Ownable.sol')
        poll = web3_socket.eth.contract(abi=poll_ABI, bytecode=bytecode)
        transaction_hash = poll.constructor(name).transact(transaction={'from': poll_owner})
        trans_receipt = web3_socket.eth.waitForTransactionReceipt(transaction_hash)
        contract_address = trans_receipt.contractAddress
        return contract_address

    @staticmethod
    def get_poll(contract_address, user):
        if not web3_socket.isAddress(contract_address):
            raise ValueError('This poll does not exist, please introduce an existing one')
        poll_ABI = CompileManager.get_ABI('poll_dapp/contracts', 'Poll.sol', 'Ownable.sol')
        return Poll(contract_address, user, poll_ABI)
