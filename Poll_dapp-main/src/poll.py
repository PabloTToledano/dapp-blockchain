from src.utils import web3_socket


class Poll:
    
    def __init__(self, contract_address, user, abi):
        self.user = user
        self.poll_id = contract_address
        self.contract = web3_socket.eth.contract(abi=abi, address=self.poll_id)

    def get_name(self):
        return self.contract.functions.getName().call()

    def add_candidate(self, candidate_name):
        return self.contract.functions.addCandidate(candidate_name).transact({"from": self.user})

    def get_step(self):
        return self.contract.functions.getStep().call()
            
    def get_candidates(self):
        return self.contract.functions.getCandidates().call()
        
    def get_candidates_number(self):
        return self.contract.functions.getCandidatesNumber().call()
        
    def vote(self, candidate_name):
        return self.contract.functions.vote(candidate_name).transact({"from": self.user})        

    def start_voting(self):
        self.contract.functions.closeListCandidates().transact({"from": self.user})
    
    def close_voting(self):
        self.contract.functions.closePoll().transact({"from": self.user})
    
    def get_winner(self):
        return self.contract.functions.getWinner().call()
        
    
