from mcts_node import MCTSNode
from random import choice
from math import sqrt, log

num_nodes = 1000
explore_factor = 2


def traverse_nodes(node, game, state, identity):
    """ Traverses the tree until the end criterion are met.

        Returns a leaf node.
    """
    child_nodes = sorted(node.child_nodes.values(),
                         key = lambda c: c.wins/c.visits + explore_factor
                         * sqrt(2 * log(node.visits)/c.visits))
    if identity == game.current_player(state):
        node = child_nodes[-1]
    else:
        node = child_nodes[0]

    return node


def expand_leaf(node, game, state):
    """ Adds a new leaf to the tree by creating a new child node for the given
        node.

        Returns an added child node.
    """
    action = choice(node.untried_actions)
    state = game.next_state(state,action)
    node.untried_actions.remove(action)
    new_leaf = MCTSNode(node, action, game.legal_actions(state))
    node.child_nodes[action] = new_leaf
    
    return new_leaf


def rollout(game, state):
    """ Given the state of the game, the rollout plays out the remainder
    
        Returns the result of the game.
    """
    while not game.is_ended(state):
        next_move = choice(game.legal_actions(state))
        state = game.next_state(state,next_move)
    
    game_points = game.points_values(state)
    return game_points


def backpropagate(node, won):
    """ Navigates the tree from a leaf node to the root, updating the win
        and visit count of each node along the path.
    """

    while node != None:
        node.visits += 1
        node.wins += won
        node = node.parent


def think(game, state):
    """ Performs MCTS by sampling games and calling the appropriate functions to
        construct the game tree.

        Returns the actions to be taken.
    """
    #print(game.display(state))
    identity_of_bot = game.current_player(state)
    root_node = MCTSNode(parent=None, parent_action=None, action_list=game.legal_actions(state))
    
    for step in range(num_nodes):
        sampled_game = state    # Copy the game for sampling a playthrough
        node = root_node    # Start at root

        print

        while node.untried_actions == [] and node.child_nodes != {}:
            node = traverse_nodes(node, game, sampled_game, identity_of_bot)
            sampled_game = game.next_state(sampled_game, node.parent_action)

        if node.untried_actions != []:
            node = expand_leaf(node, game, sampled_game)
            sampled_game = game.next_state(sampled_game, node.parent_action)
            print(sampled_game)

        points = rollout(game,sampled_game)
        result = points[identity_of_bot]
        backpropagate(node, result)

    choice = sorted(root_node.child_nodes.values(),
                   key = lambda c: c.visits)[-1].parent_action
    print("MCTS bot ", identity_of_bot, " picking ", choice)

    return choice