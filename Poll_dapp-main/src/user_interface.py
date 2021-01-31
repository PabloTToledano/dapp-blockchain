import sys
from src.poll_factory import PollFactory
from src.utils import clean_error_message
from web3.exceptions import InvalidAddress, SolidityError


def add_candidate(poll):
    candidate_name = stdin_write("Introduce the name of the candidate you want to add: ", str)

    try:
        poll.add_candidate(candidate_name)
    except SolidityError as e:
        print(clean_error_message(e))
    except InvalidAddress as e:
        print("This account does not exist")
    else:
        print("Candidate correctly added")

def get_candidates(poll):
    candidates = poll.get_candidates()
    print("These are the candidates for the poll")
    if not candidates:
        print("There are no candidates for this poll yet")
    else:
        for candidate in candidates:
            print(f"{candidate}\n")

def get_candidates_number(poll):
    candidates_number = poll.get_candidates_number()
    if candidates_number == 0:
        print("There is no candidates")
    elif candidates_number == 1:
        print("There is 1 candidate")
    elif candidates_number > 1:
        print(f"There are {candidates_number} candidates")

def vote(poll):
    candidate_name = stdin_write("Introduce the candidate name: ", str)
    try:
        poll.vote(candidate_name)
    except SolidityError as e:
        print(clean_error_message(e))
    except InvalidAddress:
        print("This account does not exist")
    else:
        print(f"{candidate_name} voted, thanks for contributing to democracy!")

def start_voting(poll):
    try:
        poll.start_voting()
    except SolidityError as e:
        print(clean_error_message(e))
    except InvalidAddress:
        print("This account does not exist")
    else:
        print("Candidates list closed. Voting process has started!")

def close_voting(poll):
    try:
        poll.close_voting()
    except SolidityError as e:
        print(clean_error_message(e))
    except InvalidAddress:
        print("This account does not exist")
    else:
        print("Voting process has finished! You can now check the results!")

def get_winner(poll):
    try:
        winner, votes = poll.get_winner()
    except SolidityError as e:
        print(clean_error_message(e))
    else:
        print(f"The winner of the poll is {winner} with {votes} votes")

def get_poll_name(poll):
    try:
        name = poll.get_name()
    except SolidityError as e:
        print(clean_error_message)
    else:
        print(f"Poll '{name}'")

def get_poll_state(poll):
    try:
        state_name = poll.get_step()
    except SolidityError as e:
        print(clean_error_message)
    else:
        print(f"The poll is in the {state_name} state")

def poll_menu(poll):

    switch = {
        0 : exit,
        1 : add_candidate,
        2 : get_poll_state,
        3 : get_candidates,
        4 : get_candidates_number,
        5 : start_voting, 
        6 : vote,
        7 : close_voting,
        8 : get_winner,
        9 : get_poll_name
    }

    while True:
        print('''\nSelect an option:
        1. Add candidate
        2. Get the actual poll state
        3. Show candidates
        4. Get number of candidates
        5. Close candidate list
        6. Vote
        7. Close the poll
        8. Get poll winner
        9. Get poll name
        0. Exit poll menu  
        ''')
    
        option = stdin_write("Choose an option: ", int)
        function = switch.get(option, None)
        if function == None:
            print("Invalid option. Try again!")
            continue
        elif option == 0:
            function()
        else:
            function(poll)
    

def interact_with_poll():
    poll_address = stdin_write("\nIntroduce the address of the poll you want to interact with: ", str)
    user_account = stdin_write("Enter your account address: ", str)
    try:
        poll = PollFactory.get_poll(poll_address, user_account)
        poll_menu(poll)
    except InvalidAddress as e:
        print("The poll address does not exist")
    
def create_poll():
    user_account = stdin_write("\nIntroduce your account address: ", str)
    poll_name = stdin_write("\nIntroduce a name for the poll: ", str)
    try:
        poll_address = PollFactory.new_poll(user_account, poll_name)
        print(f"Your poll address is: {poll_address}")
    except InvalidAddress as e:
        print("This user address does not exist in the network")
    

def menu():
    print("¡Welcome to our Poll DApp!")

    switch = {
        0 : exit,
        1 : create_poll,
        2 : interact_with_poll
    }
    
    while True:
        print('''\nSelect an action:
            1. Create a poll
            2. Interact with a poll
            0. Exit the system''')
    
        option = stdin_write("Choose an option: ", int)

        function = switch.get(option, None)
        if not function:
            print("Invalid option. Try again!")
            continue
        else:
            function() 

def stdin_write(message, caster):
    while True:
        try:
            variable = caster(input(message))
            return variable
        except ValueError:
            print("Wrong format. Try again!")
    
def exit():
    print("Thank you for using our system. Bye!")
    sys.exit(0)

if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("Thank you for using our system. Bye!")
    except Exception as e:
        print(e) 
        print("System error. Closing!")