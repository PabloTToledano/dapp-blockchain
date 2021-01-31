pragma solidity ^0.5.16;
pragma experimental ABIEncoderV2;

import "./Ownable.sol";

contract Poll is Ownable {
    enum Step {AddingCandidates, Voting, Closed}
    Step private step;

    string name;
    mapping(address => bool) voters;
    mapping(string => uint256) votes;
    string[] candidates;
    string winner;

    constructor(string memory pollName) public {
        step = Step.AddingCandidates;
        name = pollName;
    }

    function getName() public view returns (string memory) {
        return name;
    }

    modifier checkStep(Step _currentStep, Step _requiredStep) {
        require(
            _currentStep == _requiredStep,
            "You cannot call this function as the poll is not in the required step"
        );
        _;
    }

    modifier hasNotVoted() {
        require(
            voters[msg.sender] == false,
            "You cannot vote, as you have voted"
        );
        _;
    }

    function presentCandidate(string memory _candidate)
        internal
        view
        returns (bool)
    {
        bool isPresent = false;
        for (uint256 i = 0; i < candidates.length; i++) {
            if (equalStrings(_candidate, candidates[i])) {
                isPresent = true;
            }
        }
        return isPresent;
    }

    modifier isCandidate(string memory _candidate) {
        require(
            presentCandidate(_candidate),
            "The introduced candidate is not in the official list of candidates"
        );
        _;
    }

    modifier isNotCandidate(string memory _candidate) {
        require(
            !presentCandidate(_candidate),
            "The introduced candidate is already in the official list of candidates"
        );
        _;
    }

    function equalStrings(string memory a, string memory b)
        internal
        pure
        returns (bool)
    {
        return (keccak256(abi.encodePacked(a)) ==
            keccak256(abi.encodePacked(b)));
    }

    function addCandidate(string memory _candidate)
        public
        onlyOwner
        checkStep(step, Step.AddingCandidates)
        isNotCandidate(_candidate)
    {
        candidates.push(_candidate);
        votes[_candidate] = 0;
    }

    function getCandidatesNumber() public view returns (uint256) {
        return candidates.length;
    }

    function getCandidates() public view returns (string[] memory) {
        uint256 candidatesNumber = candidates.length;
        string[] memory tempCandidates = new string[](candidatesNumber);
        for (uint256 i = 0; i < candidatesNumber; i++) {
            tempCandidates[i] = candidates[i];
        }
        return tempCandidates;
    }

    function closeListCandidates()
        public
        onlyOwner
        checkStep(step, Step.AddingCandidates)
    {
        require(
            getCandidatesNumber() >= 1,
            "To close the candidates list there must be at least one candidate"
        );
        step = Step.Voting;
    }

    function calculateWinner() internal checkStep(step, Step.Closed) {
        uint256 _candidatesNumber = candidates.length;
        string memory _winnerCandidate = candidates[0];
        uint256 _maxVotes = votes[_winnerCandidate];

        for (uint256 i = 0; i < _candidatesNumber; i++) {
            string memory _currentCandidate = candidates[i];
            if (votes[_currentCandidate] > _maxVotes) {
                _winnerCandidate = _currentCandidate;
                _maxVotes = votes[_currentCandidate];
            }
        }

        winner = _winnerCandidate;
    }

    function getWinner()
        public
        view
        checkStep(step, Step.Closed)
        returns (string memory, uint256)
    {
        return (winner, votes[winner]);
    }

    function getStep() public view returns (string memory) {
        if (step == Step.AddingCandidates) {
            return "adding candidates";
        } else if (step == Step.Voting) {
            return "voting";
        } else if (step == Step.Closed) {
            return "closed";
        }
    }

    function closePoll() external onlyOwner checkStep(step, Step.Voting) {
        step = Step.Closed;
        calculateWinner();
    }

    function vote(string memory _candidate)
        public
        checkStep(step, Step.Voting)
        isCandidate(_candidate)
        hasNotVoted()
    {
        voters[msg.sender] = true;
        votes[_candidate]++;
    }
}
