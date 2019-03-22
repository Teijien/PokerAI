from mcts_implement import think
from poker_game import main, Poker
from sys import argv

def get_human_input(game, bet1, bet2):
    move = None
    #action = game.bet_action(move)
    if bet1 == bet2:
        move = input("Bet, Check, or Fold? (q to quit)").strip()
    elif bet1 < bet2:
        move = input("Raise, Call, or Fold? (q to quit)").strip()
    else:
        raise ValueError(
            "Betting player shouldn't have more in pot than opponent"
            )

    if action == "q":
       exit(2)
    elif game.is_legal(state, action):
        return action
    else:
        return get_human_input(game, bet1, bet2)

players = dict(
    human = get_human_input,
    mcts_bot = think
    )
game = Poker(2)
state0 = game.starting_state()

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
players2 = players[p2]
state = state0
last_action = None
current_player = player1

while not game.is_ended(next_state):
    print(game.display(state, last_action))
    print("Player " + str(game.current_player(state)))
    last_action = current_player(board, state)
    state = game.next_state(next_state, last_action)

    if current_player == player2:
        current_player = player1
    else:
        current_player = player2

print("Finished!")
print(game.points_values(state))