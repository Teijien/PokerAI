#  File: Poker.py

#  Description:In this program, it returns the kind of hands (e.g. full house, straight flush, et al.), and calculate the total score of each hand

#  Student's Name: Mengjie Yu

#  Student's UT EID: my3852

#  Course Name: CS 313E 

#  Unique Number: 53260

#  Date Created: 1/31/2013

#  Date Last Modified:2/1/2013

import string, math, random

class Card (object):
  RANKS = (2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14)

  SUITS = ('S', 'D', 'H', 'C')

  def __init__ (self, rank, suit):
    self.rank = rank
    self.suit = suit

  def __str__ (self):
    if self.rank == 14:
      rank = 'A'
    elif self.rank == 13:
      rank = 'K'
    elif self.rank == 12:
      rank = 'Q'
    elif self.rank == 11:
      rank = 'J'
    else:
      rank = self.rank
    return str(rank) + self.suit

  def __eq__ (self, other):
    return (self.rank == other.rank)

  def __ne__ (self, other):
    return (self.rank != other.rank)

  def __lt__ (self, other):
    return (self.rank < other.rank)

  def __le__ (self, other):
    return (self.rank <= other.rank)

  def __gt__ (self, other):
    return (self.rank > other.rank)

  def __ge__ (self, other):
    return (self.rank >= other.rank)
   

class Deck (object):
  def __init__ (self):
    self.deck = []
    for suit in Card.SUITS:
      for rank in Card.RANKS:
        card = Card (rank, suit)
        self.deck.append(card)

  def shuffle (self):
    random.shuffle (self.deck)

  def __len__ (self):
    return len (self.deck)

  def deal (self):
    if len(self) == 0:
      return None
    else:
      return self.deck.pop(0)

class Poker (object):
  def __init__ (self, numHands):
    self.deck = Deck()
    self.deck.shuffle ()
    self.hands = []
    self.tlist=[]       #create a list to store total_point
    numCards_in_Hand = 5

    for i in range (numHands):
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
      print ('Hand ' + str(i + 1) + ': ' + hand)

  def point(self,hand):                         #point()function to calculate partial score
    sortedHand=sorted(hand,reverse=True)
    c_sum=0
    for card in sortedHand:
        c_sum = c_sum + 2**(card.rank)
    return c_sum

      
  def isRoyal (self, hand):               #returns the r+h and prints out 'Royal Flush' if true, if false, pass down to isStraightFlush(hand)
    sortedHand=sorted(hand,reverse=True)
    flag=True
    r = 1000000 #Value of hand type
    h = self.point(sortedHand) #Value of main cards
    Cursuit=sortedHand[0].suit
    Currank=14
    for card in sortedHand:
      if card.suit!=Cursuit or card.rank!=Currank:
        flag=False
        break
      else:
        Currank-=1
    if flag:
        print('Royal Flush')
        self.tlist.append(r+h)    
    else:
      self.isStraightFlush(sortedHand)
    

  def isStraightFlush (self, hand):       #returns the r+h and prints out 'Straight Flush' if true, if false, pass down to isFour(hand)
    sortedHand=sorted(hand,reverse=True)
    flag=True
    r = 900000 #Value of hand type
    h = self.point(sortedHand) #Value of main cards
    Cursuit=sortedHand[0].suit
    Currank=sortedHand[0].rank
    for card in sortedHand:
      if card.suit!=Cursuit or card.rank!=Currank:
        flag=False
        break
      else:
        Currank-=1
    if flag:
      print ('Straight Flush')
      self.tlist.append(r+h)
    else:
      self.isFour(sortedHand)

  def isFour (self, hand):                  #returns the r+h and prints out 'Four of a Kind' if true, if false, pass down to isFull()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    r = 800000 #Value of hand type
    h = 0 #Value of hand ranks
    k = 0
    Currank=sortedHand[1].rank               #since it has 4 identical ranks,the 2nd one in the sorted listmust be the identical rank
    count=0
    for card in sortedHand:
      if card.rank==Currank:
        count+=1
        h += 2**(card.rank)
      else:
        k = card.rank/2
    if count==4:
      flag=True
      print('Four of a Kind')
      self.tlist.append(r+h+k)

    else:
      self.isFull(sortedHand)
    
  def isFull (self, hand):                     #returns the r+h and prints out 'Full House' if true, if false, pass down to isFlush()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    r = 700000 #Value of hand type
    h = self.point(sortedHand) #Value of hand ranks
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
      self.tlist.append(r+h)
      
    else:
      flag=False
      self.isFlush(sortedHand)

  def isFlush (self, hand):                         #returns the r+h and prints out 'Flush' if true, if false, pass down to isStraight()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    r = 600000 #Value of hand type
    h = self.point(sortedHand) #Value of hand ranks
    Cursuit=sortedHand[0].suit
    for card in sortedHand:
      if not(card.suit==Cursuit):
        flag=False
        break
    if flag:
      print ('Flush')
      self.tlist.append(r+h)
      
    else:
      self.isStraight(sortedHand)

  def isStraight (self, hand):
    sortedHand=sorted(hand,reverse=True)
    flag=True
    r = 500000 #Value of hand type
    h = self.point(sortedHand) #Value of hand ranks
    Currank=sortedHand[0].rank                        #this should be the highest rank
    for card in sortedHand:
      if card.rank!=Currank:
        flag=False
        break
      else:
        Currank-=1
    if flag:
      print('Straight')
      self.tlist.append(r+h)
      
    else:
      self.isThree(sortedHand)
        
  def isThree (self, hand):
    sortedHand=sorted(hand,reverse=True)
    flag=True
    r = 400000 #Value of hand type
    h = 0 #Value of hand ranks
    k = 0
    Currank=sortedHand[2].rank                    #In a sorted rank, the middle one should have 3 counts if flag=True
    mylist=[]
    for card in sortedHand:
      mylist.append(card.rank)
      if card.rank != Currank:    ################################################################# TJ LOOK OVER HERE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        k += (card.rank)/10
      else:
        h += 2**(card.rank)     ################################################################# TJ LOOK OVER HERE %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    if mylist.count(Currank)==3:
      flag=True
      print ("Three of a Kind")
      self.tlist.append(r+h+k)
      
    else:
      flag=False
      self.isTwo(sortedHand)
        
  def isTwo (self, hand):                           #returns the r+h and prints out 'Two Pair' if true, if false, pass down to isOne()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    r = 300000 #Value of hand type
    h = 0 #Value of hand ranks
    k = 0
    rank1=sortedHand[1].rank                        #in a five cards sorted group, if isTwo(), the 2nd and 4th card should have another identical rank
    rank2=sortedHand[3].rank
    mylist=[]
    for card in sortedHand:
      mylist.append(card.rank)
      if card.rank !=rank1 and card.rank !=rank2:
        k += (card.rank)/10
      else:
        h += 2**(card.rank)
    if mylist.count(rank1)==2 and mylist.count(rank2)==2:
      flag=True
      print ("Two Pair")
      self.tlist.append(r+h+k)
      
    else:
      flag=False
      self.isOne(sortedHand)
  
  def isOne (self, hand):                            #returns the r+h and prints out 'One Pair' if true, if false, pass down to isHigh()
    sortedHand=sorted(hand,reverse=True)
    flag=True
    r = 200000 #Value of hand type
    h = 0 #Value of hand ranks
    k = 0
    mylist=[]                                       #create an empty list to store ranks
    mycount=[]                                      #create an empty list to store number of count of each rank
    for card in sortedHand:							#Create list of card ranks (myList)
      mylist.append(card.rank)
    for each in mylist:								#Create list of counts of each rank (mycount)
      count=mylist.count(each)
      mycount.append(count)
      if mylist.count(each) != 2:
        k += (each/10)
      else:
        h += 2**(each)
		
    if mycount.count(2)==2 and mycount.count(1)==3:  #There should be only 2 identical numbers and the rest are all different
      flag=True
      print ("One Pair")
      self.tlist.append(r+h+k)
      
    else:
      flag=False
      self.isHigh(sortedHand)

  def isHigh (self, hand):                          #returns the r+h and prints out 'High Card' 
    sortedHand=sorted(hand,reverse=True)
    flag=True
    r = 100000 #Value of hand type
    h = self.point(sortedHand) #Value of hand ranks
    mylist=[]                                       #create a list to store ranks
    for card in sortedHand:
      mylist.append(card.rank)
    print ("High Card")
    self.tlist.append(r+h)
    
def main ():
  numHands = eval (input ('Enter number of hands to play: '))
  while (numHands < 2 or numHands > 6):
    numHands = eval( input ('Enter number of hands to play: ') )
  game = Poker (numHands)
  game.play()  

  print('\n')
  for i in range(numHands):
    curHand=game.hands[i]
    print ("Hand "+ str(i+1) + ": ", end="")
    game.isRoyal(curHand)
    print ("Score is " + str(game.tlist[i]))

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