pragma solidity ^0.5.16;
pragma experimental ABIEncoderV2;

import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";

import "../contracts/Poll.sol";

contract TestPoll {
    Poll public poll;

    // Run before every test function
    function beforeEach() public {
        poll = new Poll("Test poll");
    }

    function testGetName() public {
        Assert.equal(
            poll.getName(),
            "Test poll",
            "Poll name not inserted correctly"
        );
    }

    function testGetStep() public {
        Assert.equal(
            poll.getStep(),
            "adding candidates",
            "Poll step is not adding candidates"
        );
    }

    function testAddAndGetCandidates() public {
        poll.addCandidate("Charles");
        poll.addCandidate("Peter");
        string[] memory candidates = poll.getCandidates();
        Assert.equal(candidates[0], "Charles", "Unexpected candidate");
        Assert.equal(candidates[1], "Peter", "Unexpected candidate");
    }

    function testNumberCandidates() public {
        poll.addCandidate("Maria");
        poll.addCandidate("David");
        poll.addCandidate("Ronald");
        uint256 candidatesNumber = poll.getCandidatesNumber();
        Assert.equal(candidatesNumber, 3, "Unexpected number of candidates");
    }

    function testAddCandidateTwice() public {
        bool r;
        poll.addCandidate("Charles");
        (r, ) = address(this).call(
            abi.encode(poll.addCandidate.selector, "Charles")
        );
        Assert.isFalse(r, "A candidate have been added twice");
    }

    function testVoteNonExistingCandidate() public {
        bool r;
        poll.addCandidate("Maria");
        poll.closeListCandidates();
        (r, ) = address(this).call(abi.encode(poll.vote.selector, "Charles"));
        Assert.isFalse(
            r,
            "A candidate which is not in the official candidates list has been voted"
        );
    }

    function testVoteTwice() public {
        poll.addCandidate("Maria");
        poll.addCandidate("David");
        poll.closeListCandidates();
        poll.vote("Maria");
        bool r;
        (r, ) = address(this).call(abi.encode(poll.vote.selector, "Maria"));
        Assert.isFalse(r, "A candidate has been voted twice");
    }

    function testVoteBeforeVotingStep() public {
        poll.addCandidate("Charles");
        bool r;
        (r, ) = address(this).call(abi.encode(poll.vote.selector, "Charles"));
        Assert.isFalse(r, "A vote have been emited being on voting state");
    }

    function testWinner() public {
        poll.addCandidate("Maria");
        poll.addCandidate("David");
        poll.closeListCandidates();
        poll.vote("Maria");
        poll.closePoll();
        string memory winner;
        uint256 winner_votes;
        (winner, winner_votes) = poll.getWinner();
        Assert.equal(winner, "Maria", "The winner was not the expected one");
    }
}
