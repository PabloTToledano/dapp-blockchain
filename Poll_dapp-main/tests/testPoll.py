from src.poll_factory import PollFactory
import unittest
from src.utils import web3_socket
from web3.exceptions import InvalidAddress, SolidityError

class TestPoll(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.owner = web3_socket.eth.accounts[0]
        cls.user = web3_socket.eth.accounts[1]    
    
    def test_not_owner_adding_candidate(self):
        poll_id = PollFactory.new_poll(self.owner, "Test poll")
        poll = PollFactory.get_poll(poll_id, self.user)
        self.assertRaises(SolidityError, poll.add_candidate, "Elena")

    def test_not_owner_closing_candidate_list(self):
        poll_id = PollFactory.new_poll(self.owner, "Test poll")
        poll_owner = PollFactory.get_poll(poll_id, self.owner)
        poll_owner.add_candidate("Elena")
        poll_user = PollFactory.get_poll(poll_id, self.user)
        self.assertRaises(SolidityError, poll_user.start_voting)
    
    def test_not_owner_closing_poll(self):
        poll_id = PollFactory.new_poll(self.owner, "Test poll")
        poll_owner = PollFactory.get_poll(poll_id, self.owner)
        poll_owner.add_candidate("Elena")
        poll_owner.start_voting()
        poll_user = PollFactory.get_poll(poll_id, self.user)
        self.assertRaises(SolidityError, poll_user.close_voting)


if __name__ == "__main__":
    unittest.main()