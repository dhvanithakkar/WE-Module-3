import pygame
from diamonds_game import *
from pygame_display import *

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 600
CARD_WIDTH, CARD_HEIGHT = 80, 120
BUTTON_WIDTH, BUTTON_HEIGHT = 150, 50

MARGIN = 20

CARDS_START_Y = SCREEN_HEIGHT - CARD_HEIGHT - MARGIN

GREEN = (0, 100, 0) 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY  = (50, 50, 50)
RED  = (207, 0, 0)

BACKGROUND_COLOR = GREEN

class Diamonds_PyGame:
    
    def __init__(self, screen):   
        self.NUM_ROUNDS = 2
        self.game = DiamondsGame()
        self.screen = screen
        self.screen.fill(BACKGROUND_COLOR)
    
    def add_players(self, num_bots: int, num_randoms: int, human_names: list[str]):
        if num_bots > 0:
            self.game.add_bot()
            self.game.add_human_player(human_names[0])
            return
        
        for random in range(num_randoms):
            self.game.add_random()
        
        for human_name in human_names:
            self.game.add_human_player(human_name)
    
    def choose_bid_human_GUI(player, screen):
        """Allows the player to choose a card for bidding using a graphical interface"""
        
        running = True
        chosen_card = None

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_pos = pygame.mouse.get_pos()
                        for card in player.hand:
                            if card.is_clicked(mouse_pos):
                                chosen_card = card
                                running = False  # Exit loop once card is chosen
                                break

            screen.fill((255, 255, 255))  # Fill the screen with white
            # for card in player.hand:
            #     screen.blit(card.image, card.rect)  # Draw all cards in player's hand
            pygame.display.flip()

        return chosen_card    
    
    def round_tester(self, round_no, opponent = None):
        self.screen.fill(BACKGROUND_COLOR)
        
        print_round_title(self.screen, round_no, SCREEN_WIDTH)
        player = self.game.players[0]
        display_player_hand(player.hand, CARD_WIDTH, CARD_HEIGHT, self.screen, CARDS_START_Y, player.name)

        revealed_diamond = self.game.diamond_pile[0]
        self.game.revealed_diamonds.append(revealed_diamond.value)
        revealed_diamond.display_card(screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, CARD_WIDTH, CARD_HEIGHT, )



    def play_GUI_round(self, round_no, opponent = None):
        """Display the game state on the screen"""
        self.screen.fill(BACKGROUND_COLOR)
        
        print_round_title(self.screen, round_no, SCREEN_WIDTH)
        
        player = self.game.players[0]
        display_player_hand(player.hand, CARD_WIDTH, CARD_HEIGHT, self.screen, CARDS_START_Y)

        revealed_diamond = self.game.diamond_pile.pop(0)
        self.game.revealed_diamonds.append(revealed_diamond.value)

        revealed_diamond.display_card(screen, SCREEN_WIDTH/2, SCREEN_HEIGHT/2, CARD_WIDTH, CARD_HEIGHT, )

        if opponent:
            opponent_hand = opponent.get_hand_values()
        
        bids = []
        highest_bid = 0
        winners = []

        for player in self.game.players:
            if player.isBot and opponent_hand:
                bid = player.choose_bid(revealed_diamond, self.revealed_diamonds, opponent_hand)
            elif player.isRandom:
                bid = player.choose_bid()
            else:
                # Display cards in the players' hands
                screen.fill(BACKGROUND_COLOR)
                print_round_title(self.screen, round_no, SCREEN_WIDTH)

                display_player_hand(player.hand, CARD_WIDTH, CARD_HEIGHT, self.screen, CARDS_START_Y, player.name)

                bid = self.choose_bid_human_GUI(player, screen)
			
            bids.append(bid)
			
            if bid.value > highest_bid:
                winners = [player]
                highest_bid = bid.value
            elif bid.value == highest_bid:
                winners.append(player)
        
        revealed_diamond_value = revealed_diamond.value
        
        display_bids_and_winners(self.screen, bids, self.game.players, winners, highest_bid, round_no, revealed_diamond_value)    
        
##################  MAIN
        
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

py_game = Diamonds_PyGame(screen)

human_names, num_bots, num_randoms = player_configuration(screen)
py_game.add_players(num_bots, num_randoms, human_names)
py_game.game.setup_game()

opponent = py_game.game.players[1]
on_round = 1


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    
    if on_round > py_game.NUM_ROUNDS:
            display_final_scores(py_game.game.players, screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    py_game.round_tester(on_round, opponent) # on_round, opponent

    on_round += 1

    # flip() the display to put your work on screen
    pygame.display.flip()
    
    # screen.fill(BACKGROUND_COLOR)

    dt = clock.tick(60) / 1000

pygame.quit()

