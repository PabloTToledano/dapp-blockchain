from src.poll_factory import PollFactory
from src.utils import clean_error_message, web3_socket

from web3.exceptions import InvalidAddress, SolidityError

try:
    owner = web3_socket.eth.accounts[0]
    user_2 = web3_socket.eth.accounts[1]
    #poll_id = PollFactory.new_poll(owner)
    poll_id = "0xcA8ECCA29eDCC9FFbD990019451Acdf8c166feB3"
    print(poll_id)
    poll = PollFactory.get_poll(poll_id, owner)
    poll.add_candidate("elena, se prueba mucho más rápido, tienes toda la razón")
    candidates = poll.get_candidates()
    print(candidates)
except InvalidAddress as e:
    print(e)
except SolidityError as e:
    print(clean_error_message(e))

    