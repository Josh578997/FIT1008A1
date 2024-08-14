from data_structures.referential_array import ArrayR
from player import Player
from card import CardColor, CardLabel, Card
from random_gen import RandomGen
from constants import Constants
from data_structures.aset import ASet as set
from data_structures.array_sorted_list import ArraySortedList
from data_structures.stack_adt import ArrayStack

class Game:
    """
    Game class to play the game
    """

    #boolean variables determine special game states
    reversed = False
    skip = False

    def __init__(self) -> None:
        """
        Constructor for the Game class

        Args:
            None

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        self.players = ArraySortedList(Constants.MAX_PLAYERS)
        self.draw_pile = ArrayStack(Constants.DECK_SIZE)
        self.discard_pile = ArrayStack(Constants.DECK_SIZE)
        self.current_player = None
        self.current_color = None
        self.current_label = None
        
        


    def generate_cards(self) -> ArrayR[Card]:
        """
        Method to generate the cards for the game

        Args:
            None

        Returns:
            ArrayR[Card]: The array of Card objects generated

        Complexity:
            Best Case Complexity: O(N) - Where N is the number of cards in the deck
            Worst Case Complexity: O(N) - Where N is the number of cards in the deck
        """
        list_of_cards: ArrayR[Card] = ArrayR(Constants.DECK_SIZE)
        idx: int = 0

        for color in CardColor:
            if color != CardColor.CRAZY:
                # Generate 4 sets of cards from 0 to 9 for each color
                for i in range(10):
                    list_of_cards[idx] = Card(color, CardLabel(i))
                    idx += 1
                    list_of_cards[idx] = Card(color, CardLabel(i))
                    idx += 1

                # Generate 2 of each special card for each color
                for i in range(2):
                    list_of_cards[idx] = Card(color, CardLabel.SKIP)
                    idx += 1
                    list_of_cards[idx] = Card(color, CardLabel.REVERSE)
                    idx += 1
                    list_of_cards[idx] = Card(color, CardLabel.DRAW_TWO)
                    idx += 1
            else:
                # Generate the crazy and crazy draw 4 cards
                for i in range(4):
                    list_of_cards[idx] = Card(CardColor.CRAZY, CardLabel.CRAZY)
                    idx += 1
                    list_of_cards[idx] = Card(CardColor.CRAZY, CardLabel.DRAW_FOUR)
                    idx += 1

                # Randomly shuffle the cards
                RandomGen.random_shuffle(list_of_cards)

                return list_of_cards

    def initialise_game(self, players: ArrayR[Player]) -> None:
        """
        Method to initialise the game

        Args:
            players (ArrayR[Player]): The array of players

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        for player in players:
            self.players.add(player)
        self.cards = self.generate_cards()
        i = 0
        for card in self.cards:
            self.player_dealt = self.players[i]
            if len(self.player_dealt.hand) == Constants.NUM_CARDS_AT_INIT:
                self.draw_pile.push(card) #push card to the draw pile
            elif len(self.player_dealt.hand) < Constants.NUM_CARDS_AT_INIT:
                self.player_dealt.add_card(card)
            else:
                print("weird exeption please check code")
                exit()
            if i < len(self.players)-1:
                i+=1
            else:
                i = 0
        self.discard_pile.push(self.draw_pile.pop())
        checkcard = self.discard_pile.peek()
        currentcardlabel = checkcard.label

        while currentcardlabel not in [0,1,2,3,4,5,6,7,8,9]:
            self.discard_pile.push(self.draw_pile.pop())
            checkcard = self.discard_pile.peek()
        
        finalcard = self.discard_pile.peek()
        self.current_color = finalcard.color
        self.current_label = finalcard.label
        
        


    def crazy_play(self, card: Card) -> None:
        """
        Method to play a crazy card

        Args:
            card (Card): The card to be played

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        self.current_color = CardColor(RandomGen.randint(0,3))
        if card.label == CardLabel.DRAW_FOUR:
            next_player = self.next_player()
            for _ in range(4):
                self.draw_card(next_player,playing=False)
    

    def play_reverse(self) -> None:
        """
        Method to play a reverse card

        Args:
            None

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        if self.reversed == False:
            self.reversed = True
        elif self.reversed == True:
            self.reversed = False

    def play_skip(self) -> None:
        """
        Method to play a skip card

        Args:
            None

        Returns:
            None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        self.skip = True

    def draw_card(self, player: Player, playing: bool) -> Card | None:
        """
        Method to draw a card from the deck

        Args:
            player (Player): The player who is drawing the card
            playing (bool): A boolean indicating if the player is able to play the card

        Returns:
            Card - When drawing a playable card, other return None

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        card = self.draw_pile.pop()
        current_card = self.discard_pile.peek()
        if (card.label == current_card.label or card.color == current_card.color or card.label in [13,14]) and playing == True:
            return card
        else:
            player.add_card(card)
            return None


    def next_player(self) -> Player:
        """
        Method to get the next player

        Args:
            None

        Returns:
            Player: The next player

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        if self.current_player is None:
            if (self.skip is False) and (self.reversed is True):
                return self.players[len(self.players)-1]
            elif (self.skip is True) and (self.reversed is True):
                self.skip = False
                return self.players[len(self.players)-2]
            elif (self.skip is True) and (self.reversed is False):
                self.skip = False
                return self.players[1]
            else:
                return self.players[0]
        else:    
            if (self.skip is False) and (self.reversed is True):
                if self.current_player.position - 1 < 0:
                    return self.players[-1]
                else:
                    return self.players[self.current_player.position-1]
            elif (self.skip is True) and (self.reversed is True):
                self.skip = False
                if self.current_player.position - 2 < 0:
                    return self.players[-1]
                else:
                    return self.players[self.current_player.position-2]
            elif (self.skip is True) and (self.reversed is False):
                self.skip = False
                if self.current_player.position + 2 > len(self.players)-1:
                    return self.players[0]
                else:
                    return self.players[self.current_player.position+2]        
            elif (self.skip is False) and (self.reversed is False):
                if self.current_player.position == len(self.players)-1:
                    return self.players[0]
                else:
                    return self.players[self.current_player.position+1]

        

    def play_game(self) -> Player:
        """
        Method to play the game

        Args:
            None

        Returns:
            Player: The winner of the game

        Complexity:
            Best Case Complexity:
            Worst Case Complexity:
        """
        game = True
        while game:
            self.current_player = self.next_player() # get the next player and set as current
            if len(self.current_player.hand) == 0:
                return self.current_player            # win condition
            
            elif self.draw_pile.is_empty():
                top_card = self.discard_pile.pop()
                temp_array = ArrayR(len(self.discard_pile))

                for i in range(len(self.discard_pile)):
                    temp_array[i] = self.discard_pile.pop()
                temp_array = RandomGen.random_shuffle(temp_array)

                for i in range(len(temp_array)):
                    self.draw_pile.push(temp_array[i])
                self.discard_pile.push(top_card)
           
            hand_card = self.current_player.hand[0]   # card to be played
            hand_card_color = hand_card.color
            hand_card_label = hand_card.label
            if hand_card_label == CardLabel.CRAZY:
                played_card = self.current_player.play_card(0)
                self.crazy_play(played_card)
                self.play_skip()
                self.discard_pile.push(played_card)
            elif hand_card_label == CardLabel.DRAW_FOUR:
                played_card = self.current_player.play_card(0)
                self.crazy_play(played_card)
                self.discard_pile.push(played_card)
            elif hand_card_color == self.current_color or hand_card_label == self.current_label:
                played_card = self.current_player.play_card(0)
                if played_card.label == CardLabel.DRAW_TWO:
                    next_player = self.next_player()
                    for _ in range (2):                                  # draw 2 action
                        self.draw_card(next_player,playing = False)
                        self.play_skip()
                self.discard_pile.push(played_card)
            else:
                new_card = self.draw_card(self.current_player, playing = True)    
                if new_card is not None:
                    self.discard_pile.push(new_card)




def test_case():
    players: ArrayR[Player] = ArrayR(4)
    players[0] = Player("Alice", 0)
    players[1] = Player("Bob", 1)
    players[2] = Player("Charlie", 2)
    players[3] = Player("David", 3)
    g: Game = Game()
    g.initialise_game(players)
    winner: Player = g.play_game()
    print(f"Winner is {winner.name}")


if __name__ == '__main__':
    test_case()
