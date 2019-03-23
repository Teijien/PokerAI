# https://github.com/annaymj/Python-Code/blob/master/Poker.py

import math
import random
import string


class Card(object):
    SUITS = ('S', 'H', 'C', 'D')
    RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

    def __init__(self, rank, suit):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        if self.rank == 11:
            rank = 'J'
        elif self.rank == 12:
            rank = 'Q'
        elif self.rank == 13:
            rank = 'K'
        elif self.rank == 14:
            rank = 'A'
        else:
            rank = self.rank
        return str(rank) + self.suit

    def __eq__(self, other):
        return (self.rank == other.rank)

    def __ne__(self, other):
        return (self.rank != other.rank)

    def __lt__(self, other):
        return (self.rank < other.rank)

    def __le__(self, other):
        return (self.rank <= other.rank)

    def __gt__(self, other):
        return (self.rank > other.rank)

    def __ge__(self, other):
        return (self.rank >= other.rank)


class Deck(object):
    def __init__(self):
        self.deck = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                card = Card(rank, suit)
                self.deck.append(card)

    def shuffle(self):
        random.shuffle(self.deck)

    def __len__(self):
        return len(self.deck)

    def deal(self):
        if len(self) == 0:
            return None
        else:
            return self.deck.pop(0)


class Poker(object):
    def __init__(self, numHands):
        self.deck = Deck()
        self.deck.shuffle()
        self.hands = []
        self.tlist = []
        numCards_in_Hand = 5

        # Following are the included variables for implementing betting #
        #self.pot = 0
        #small_blind = 1
        #big_blind = 2

        for i in range(numHands):
            hand = []
            for j in range (numCards_in_Hand):
                hand.append (self.deck.deal())
            self.hands.append (hand)

    def play (self):
        for i in range (len (self.hands) ):
            sortedHand = sorted (self.hands[i], reverse = True)
            hand = ''
            for card in sortedHand:
                hand = hand + str(card) + ' '
            print ('Hand ' + str(i + 1) + ': ' + hand + " score: " + str(self.point(sortedHand)))

    def point(self,hand):                         #point()function to calculate partial score
        sortedHand=sorted(hand,reverse=True)
        c_sum=0
        ranklist=[]
        for card in sortedHand:
            ranklist.append(card.rank)
        c_sum=ranklist[0]*13**4+ranklist[1]*13**3+ranklist[2]*13**2+ranklist[3]*13+ranklist[4]
        return c_sum

      
    def isRoyal (self, hand):               #returns the total_point and prints out 'Royal Flush' if true, if false, pass down to isStraightFlush(hand)
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=10
        Cursuit=sortedHand[0].suit
        Currank=14
        total_point=h*13**6+self.point(sortedHand)
        for card in sortedHand:
            if card.suit!=Cursuit or card.rank!=Currank:
                flag=False
                break
            else:
                Currank-=1
        if flag:
            print('Royal Flush')
            self.tlist.append(total_point)    
        else:
            self.isStraightFlush(sortedHand)
    

    def isStraightFlush (self, hand):       #returns the total_point and prints out 'Straight Flush' if true, if false, pass down to isFour(hand)
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=9
        Cursuit=sortedHand[0].suit
        Currank=sortedHand[0].rank
        total_point=h*13**6+self.point(sortedHand)
        for card in sortedHand:
            if card.suit!=Cursuit or card.rank!=Currank:
                flag=False
                break
            else:
                Currank-=1
        if flag:
            print ('Straight Flush')
            self.tlist.append(total_point)
        else:
            self.isFour(sortedHand)

    def isFour (self, hand):                  #returns the total_point and prints out 'Four of a Kind' if true, if false, pass down to isFull()
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=8
        Currank=sortedHand[1].rank               #since it has 4 identical ranks,the 2nd one in the sorted listmust be the identical rank
        count=0
        total_point=h*13**6+self.point(sortedHand)
        for card in sortedHand:
            if card.rank==Currank:
                count+=1
        if not count<4:
            flag=True
            print('Four of a Kind')
            self.tlist.append(total_point)

        else:
            self.isFull(sortedHand)
    
    def isFull (self, hand):                     #returns the total_point and prints out 'Full House' if true, if false, pass down to isFlush()
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=7
        total_point=h*13**6+self.point(sortedHand)
        mylist=[]                                 #create a list to store ranks
        for card in sortedHand:
            mylist.append(card.rank)
        rank1=sortedHand[0].rank                  #The 1st rank and the last rank should be different in a sorted list
        rank2=sortedHand[-1].rank
        num_rank1=mylist.count(rank1)
        num_rank2=mylist.count(rank2)
        if (num_rank1==2 and num_rank2==3)or (num_rank1==3 and num_rank2==2):
            flag=True
            print ('Full House')
            self.tlist.append(total_point)
      
        else:
            flag=False
            self.isFlush(sortedHand)

    def isFlush (self, hand):                         #returns the total_point and prints out 'Flush' if true, if false, pass down to isStraight()
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=10**5
        total_point=h*self.point(sortedHand)
        Cursuit=sortedHand[0].suit
        for card in sortedHand:
            if not(card.suit==Cursuit):
                flag=False
                break
        if flag:
            print ('Flush')
            self.tlist.append(total_point)
      
        else:
            self.isStraight(sortedHand)

    def isStraight (self, hand):
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=5
        total_point=h*13**6+self.point(sortedHand)
        Currank=sortedHand[0].rank                        #this should be the highest rank
        for card in sortedHand:
          if card.rank!=Currank:
            flag=False
            break
          else:
            Currank-=1
        if flag:
          print('Straight')
          self.tlist.append(total_point)
      
        else:
          self.isThree(sortedHand)
        
    def isThree (self, hand):
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=4
        total_point=h*13**6+self.point(sortedHand)
        Currank=sortedHand[2].rank                    #In a sorted rank, the middle one should have 3 counts if flag=True
        mylist=[]
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(Currank)==3:
            flag=True
            print ("Three of a Kind")
            self.tlist.append(total_point)
      
        else:
            flag=False
            self.isTwo(sortedHand)

    def isTwo (self, hand):                           #returns the total_point and prints out 'Two Pair' if true, if false, pass down to isOne()
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=3
        total_point=h*13**6+self.point(sortedHand)
        rank1=sortedHand[1].rank                        #in a five cards sorted group, if isTwo(), the 2nd and 4th card should have another identical rank
        rank2=sortedHand[3].rank
        mylist=[]
        for card in sortedHand:
            mylist.append(card.rank)
        if mylist.count(rank1)==2 and mylist.count(rank2)==2:
            flag=True
            print ("Two Pair")
            self.tlist.append(total_point)
      
        else:
            flag=False
            self.isOne(sortedHand)
  
    def isOne (self, hand):                            #returns the total_point and prints out 'One Pair' if true, if false, pass down to isHigh()
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=2
        total_point=h*13**6+self.point(sortedHand)
        mylist=[]                                       #create an empty list to store ranks
        mycount=[]                                      #create an empty list to store number of count of each rank
        for card in sortedHand:
            mylist.append(card.rank)
        for each in mylist:
            count=mylist.count(each)
            mycount.append(count)
        if mycount.count(2)==2 and mycount.count(1)==3:  #There should be only 2 identical numbers and the rest are all different
            flag=True
            print ("One Pair")
            self.tlist.append(total_point)
        else:
            flag=False
            self.isHigh(sortedHand)

    def isHigh (self, hand):                          #returns the total_point and prints out 'High Card' 
        sortedHand=sorted(hand,reverse=True)
        flag=True
        h=1
        total_point=h*13**6+self.point(sortedHand)
        mylist=[]                                       #create a list to store ranks
        for card in sortedHand:
            mylist.append(card.rank)
        print ("High Card")
        self.tlist.append(total_point)


class FiveCardDrawPoker(Poker):
    def __init__(self, blinds, buy_in):
        super().__init__(2)     # Game will only be played with two players
        self.big_blind = blinds
        self.small_blind = blinds / 2
        self.lower_limit = blinds       # Lower betting limit
        self.upper_limit = blinds * 2       # Upper betting limit
        self.buy_in = buy_in

    def starting_state(self):
        """ Defines the starting pot for each player.
            
            Returns a tuple consisting of each player's buy-in and chips bet, as
            well as if it's Turn 0, if the bets are uneven, and the player to
            take their turn.
        """
        return (self.buy_in, 0), (self.buy_in, 0), (0, False, 1)

    def get_player(self, state, player):
        return state[player - 1]

    def get_player_chips(self, state, player):
        return self.get_player(state, player)[0]

    def get_player_bet(self, state, player):
        return self.get_player(state, player)[1]

    def get_current_player(self, state):
        return self.get_player(state, 3)[-1]

    def is_uneven(self, state):
        """ Checks if the bets are uneven """
        return self.get_player(state, 3)[1]

    def legal_actions(self, state):
        actions = []
        if self.is_uneven(state):
            actions = ["raise", "call", "fold"]
        else:
            actions = ["bet", "check", "fold"]

        current_player = self.get_current_player(state)
        if self.get_player_chips(state, current_player) < self.lower_limit:
            actions.pop(0)

        return actions

    def collect_blinds(self, state):
        """ Updates the state after collecting blinds. Current turn must be
            Turn 0.
        """
        player_one = self.get_player(state, 1)
        player_two = self.get_player(state, 2)
        stats = self.get_player(state, 3)

        # Check if the current turn is Turn 0 #
        if stats[0] != 0:
            print("Cannot collect blinds! Round is not finished!\n")
            return player_one, player_two, stats

        new_chips_p1 = player_one[0] - self.small_blind
        new_bet_p1 = player_one[1] + self.small_blind
        player_one = (new_chips_p1, new_bet_p1)

        new_chips_p2 = player_two[0] - self.big_blind
        new_bet_p2 = player_two[1] + self.big_blind
        player_two = (new_chips_p2, new_bet_p2)

        turn_one = stats[0] + 1
        is_uneven = True
        stats = (turn_one, is_uneven, stats[-1])

        return player_one, player_two, stats

    def get_action(self, state):
        actions = self.legal_actions(state)
        player_action = input("Enter action: ")
        if player_action not in actions:
            print("Not a legal action.")
            return self.get_action(state)

        return player_action

    # NEEDS TO BE IMPLEMENTED #
    def next_state(self, state, action):

        pass


def main ():
  #numHands = eval (input ('Enter number of hands to play: '))
  #while (numHands < 2 or numHands > 6):
  numHands = eval( input ('Enter number of hands to play: ') )
  game = Poker (numHands)
  game.play()

  print('\n')
  for i in range(numHands):
    curHand=game.hands[i]
    print ("Hand "+ str(i+1) + ": ", end="")
    game.isRoyal(curHand)

  maxpoint=max(game.tlist)
  maxindex=game.tlist.index(maxpoint)

  print ('\nHand %d wins'% (maxindex+1))


def test():
    game = FiveCardDrawPoker(2, 50)
    state = game.starting_state()
    assert state == ((50, 0), (50, 0), (0, False, 1)), "starting_state() fail!"
    print("starting_state() pass!")

    uneven_state = game.collect_blinds(state)
    assert uneven_state == ((49, 1), (48, 2), (1, True, 1)), "collect_blinds() fail!"
    print("collect_blinds() pass!")

    legal_actions = game.legal_actions(uneven_state)
    assert legal_actions == ["raise", "call", "fold"]

    even_state = ((48, 2), (48, 2), (2, False, 2))
    legal_actions = game.legal_actions(even_state)
    assert legal_actions == ["bet", "check", "fold"]

    few_chips_state = ((1, 0), (1, 0), (1, False, 1))
    legal_actions = game.legal_actions(few_chips_state)
    assert legal_actions == ["check", "fold"]

    input = game.get_action(uneven_state)
    #assert input in ["raise", "call", "fold"], "get_action() for uneven bets fail!"

    input = game.get_action(even_state)
    #assert input in ["bet", "check", "fold"], "get_action() for even bets fail!"

    action = "bet"
    new_state = game.next_state(even_state, action)
    assert new_state == ((48, 2), (46, 4), (3, True, 1))

    action = "check"
    new_state = game.next_state(even_state, action)
    assert new_state == ((48, 2), (48, 2), (3, False, 1))

    action = "fold"
    new_state = game.next_state(even_state, action)
    assert new_state == ((52, 0), (48, 0), (0, False, 1))

    raise_action = "raise"
    newer_state = game.next_state(uneven_state, raise_action)
    assert new_state == ((46, 4), (48, 2), (2, True, 2))

    call_action = "call"
    new_state = game.next_state(uneven_state, call_action)
    assert new_state == ((48, 2), (48, 2), (2, False, 2))

    new_state = game.next_state(newer_state, raise_action)
    assert new_state == ((46, 4), (44, 6), (3, True, 1))

    new_state = game.next_state(newer_state, call_action)
    assert new_state == ((46, 4), (46, 4), (3, False, 1))

    print("All tests pass!")

main()
#test()