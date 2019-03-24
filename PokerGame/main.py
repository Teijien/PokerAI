from mcts_implement import think
from poker_game import main, FiveCardDrawPoker
from sys import argv

def get_human_input(game, state):
    move = None
    #action = game.bet_action(move)
    if not game.is_uneven(state):
        move = input("Bet, Check, or Fold? (q to quit)").strip()
    elif game.is_uneven(state):
        move = input("Raise, Call, or Fold? (q to quit)").strip()
    else:
        raise ValueError(
            "Betting player shouldn't have more in pot than opponent"
            )

    if move == "q":
       exit(2)
    elif game.is_legal(state, move):
        return move
    else:
        print("Not a legal move!")
        return get_human_input(game, state)

players = dict(
    human = get_human_input,
    mcts_bot = think
    )
numHands = 2
game = FiveCardDrawPoker(numHands, 50)
state0 = game.starting_state()
state0 = game.collect_blinds(state0)
game.play()

#print("Hand " + str(1) + ": ", end = "")
game.isRoyal(game.hands[0])
print('\n')

if len(argv) != 3:
    print("Need two player arguments")
    exit(1)

p1 = argv[1]
p2 = argv[2]
if p1 not in players:
    print("p1 not in " + players.keys().join(","))
    exit(1)
if p2 not in players:
    print("p2 not in " + players.keys().join(","))
    exit(1)

player1 = players[p1]
player2 = players[p2]
state = state0
last_action = None
current_player = player1

while not game.is_ended(state):
    print(game.display(state))
    print("Player " + str(game.current_player(state)))
    last_action = current_player(game, state)
    state = game.next_state(state, last_action)

    if current_player == player2:
        current_player = player1
    else:
        current_player = player2

print("Finished!\n")
sortedHand = sorted(game.hands[1], reverse = True)
hand = ''
for card in sortedHand:
    hand = hand + str(card) + ' '
print('Hand ' + str(2) + ': ' + hand + ' score: ' + str(game.point(sortedHand)))
game.isRoyal(game.hands[1])
print('\n')
if last_action == "fold":
    points = game.points_values(state)
    if current_player == player1:
        points[1] = abs(points[1])
        points[2] = -abs(points[2])
        print(points)
    else:
        points[1] = -abs(points[1])
        points[2] = abs(points[2])
        print(points)
else:
    print(game.points_values(state))