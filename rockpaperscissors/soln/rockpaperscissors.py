num_matches = int(input())
aliceWinnedMatch = 0
bobWinnedMatch = 0

for i in range(num_matches):
    # add your code here
    aliceWinnedRound = 0
    tie = 0
    rounds = input()
    round_list = rounds.split()
    for round in round_list:
        if round[0] == round[1]:
            tie += 1
        elif ((round[0] == 'R') and (round[1] == 'S')) or ((round[0] == 'S') and (round[1] == 'P')) or ((round[0] == 'P') and (round[1] == 'R')):
            aliceWinnedRound += 1

    if aliceWinnedRound > len(round_list) - aliceWinnedRound - tie:
        aliceWinnedMatch += 1
    if aliceWinnedRound < len(round_list) - aliceWinnedRound - tie:
        bobWinnedMatch += 1

# print here whoever is the overall winner of all the matches and
# how many matches the winner won
if aliceWinnedMatch >= bobWinnedMatch:
    print("Alice", aliceWinnedMatch)
else:
    print("Bob", bobWinnedMatch)
