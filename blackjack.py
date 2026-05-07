import os
import pygame
import random
import time
import numpy as np
import streamlit as st
from PIL import Image

# Initialize Pygame in headless mode
os.environ["SDL_VIDEODRIVER"] = "dummy"
pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 800, 600
CARD_WIDTH, CARD_HEIGHT = 80, 120
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
YELLOW = (255, 215, 0)
BLUE = (0, 51, 102)

# Fonts
try:
    FONT = pygame.font.SysFont("arial", 24, bold=True)
    LARGE_FONT = pygame.font.SysFont("arial", 48, bold=True)
    BANNER_FONT = pygame.font.SysFont("arial", 64, bold=True)
except:
    FONT = pygame.font.Font(None, 24)
    LARGE_FONT = pygame.font.Font(None, 48)
    BANNER_FONT = pygame.font.Font(None, 64)

SUITS = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
VALUES = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10, 'A': 11}

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = VALUES[rank]
        self.color = RED if suit in ['Hearts', 'Diamonds'] else BLACK
        self.is_hidden = False
        self.x = 0
        self.y = 0
        
        # Target position for animation
        self.target_x = 0
        self.target_y = 0

    def draw(self, surface):
        rect = pygame.Rect(self.x, self.y, CARD_WIDTH, CARD_HEIGHT)
        if self.is_hidden:
            pygame.draw.rect(surface, BLUE, rect, border_radius=5)
            pygame.draw.rect(surface, WHITE, rect, 2, border_radius=5)
            # Pattern back
            for i in range(10, CARD_WIDTH, 20):
                pygame.draw.line(surface, WHITE, (self.x + i, self.y), (self.x + i, self.y + CARD_HEIGHT), 1)
        else:
            pygame.draw.rect(surface, WHITE, rect, border_radius=5)
            pygame.draw.rect(surface, BLACK, rect, 2, border_radius=5)
            
            # Draw rank and suit
            text = FONT.render(self.rank, True, self.color)
            surface.blit(text, (self.x + 5, self.y + 5))
            
            suit_symbol = ''
            if self.suit == 'Hearts': suit_symbol = '♥'
            elif self.suit == 'Diamonds': suit_symbol = '♦'
            elif self.suit == 'Clubs': suit_symbol = '♣'
            elif self.suit == 'Spades': suit_symbol = '♠'
            
            suit_text = FONT.render(suit_symbol, True, self.color)
            surface.blit(suit_text, (self.x + 5, self.y + 30))
            
            # Large center symbol
            large_suit = LARGE_FONT.render(suit_symbol, True, self.color)
            suit_rect = large_suit.get_rect(center=(self.x + CARD_WIDTH//2, self.y + CARD_HEIGHT//2 + 10))
            surface.blit(large_suit, suit_rect)

class Deck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUITS for rank in RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            self.__init__() # Reshuffle if empty
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.bet = 0
        self.is_active = True

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        value = sum(card.value for card in self.cards if not card.is_hidden)
        aces = sum(1 for card in self.cards if not card.is_hidden and card.rank == 'A')
        while value > 21 and aces:
            value -= 10
            aces -= 1
        return value

    def is_bust(self):
        return self.calculate_value() > 21

    def is_blackjack(self):
        return len(self.cards) == 2 and self.calculate_value() == 21

class BlackjackGame:
    def __init__(self):
        self.balance = 1000
        self.current_bet = 0
        self.deck = Deck()
        self.player_hands = [Hand()]
        self.current_hand_idx = 0
        self.dealer_hand = Hand()
        self.state = "BETTING"
        self.message = ""
        self.animating = False

    def reset_round(self):
        self.player_hands = [Hand()]
        self.current_hand_idx = 0
        self.dealer_hand = Hand()
        self.message = ""
        
        if len(self.deck.cards) < 20:
            self.deck = Deck()

    def deal(self, bet):
        if self.balance < bet:
            self.message = "Not enough chips!"
            return

        self.reset_round()
        self.current_bet = bet
        self.balance -= bet
        self.player_hands[0].bet = bet
        
        self.state = "DEALING"
        self.animating = True

        # Deal sequence
        for i in range(2):
            self.player_hands[0].add_card(self.deck.draw_card())
            dealer_card = self.deck.draw_card()
            if i == 1:
                dealer_card.is_hidden = True
            self.dealer_hand.add_card(dealer_card)
            
        self.setup_animations()

    def setup_animations(self):
        # Set starting positions (deck location)
        deck_x, deck_y = WIDTH - 100, 50
        
        for i, card in enumerate(self.player_hands[0].cards):
            card.x, card.y = deck_x, deck_y
            card.target_x = 300 + i * 40
            card.target_y = 400

        for i, card in enumerate(self.dealer_hand.cards):
            card.x, card.y = deck_x, deck_y
            card.target_x = 300 + i * 40
            card.target_y = 100

    def update_animations(self):
        moving = False
        speed = 40
        
        cards_to_check = []
        if self.state == "DEALING":
            p_cards = self.player_hands[0].cards
            d_cards = self.dealer_hand.cards
            for i in range(max(len(p_cards), len(d_cards))):
                if i < len(p_cards): cards_to_check.append(p_cards[i])
                if i < len(d_cards): cards_to_check.append(d_cards[i])
        else:
            for hand in self.player_hands:
                cards_to_check.extend(hand.cards)
            cards_to_check.extend(self.dealer_hand.cards)
            
        for card in cards_to_check:
            if abs(card.x - card.target_x) > speed or abs(card.y - card.target_y) > speed:
                moving = True
                if abs(card.x - card.target_x) > speed:
                    card.x += speed if card.x < card.target_x else -speed
                else:
                    card.x = card.target_x
                    
                if abs(card.y - card.target_y) > speed:
                    card.y += speed if card.y < card.target_y else -speed
                else:
                    card.y = card.target_y
                break
            else:
                card.x, card.y = card.target_x, card.target_y

        if not moving:
            self.animating = False
            if self.state == "DEALING":
                self.state = "PLAYER_TURN"
                self.check_initial_blackjack()
            elif self.state == "DEALER_TURN_ANIMATING":
                self.resolve_game()

    def check_initial_blackjack(self):
        player_bj = self.player_hands[0].is_blackjack()
        
        # Temporary reveal dealer card to check
        self.dealer_hand.cards[1].is_hidden = False
        dealer_bj = self.dealer_hand.is_blackjack()
        self.dealer_hand.cards[1].is_hidden = True

        if player_bj and dealer_bj:
            self.dealer_hand.cards[1].is_hidden = False
            self.message = "PUSH!"
            self.balance += self.current_bet
            self.state = "GAME_OVER"
        elif player_bj:
            self.message = "BLACKJACK! You Win!"
            self.balance += self.current_bet + int(self.current_bet * 1.5)
            self.state = "GAME_OVER"
        elif dealer_bj:
            self.dealer_hand.cards[1].is_hidden = False
            self.message = "Dealer Blackjack! You Lose!"
            self.state = "GAME_OVER"

    def hit(self):
        hand = self.player_hands[self.current_hand_idx]
        card = self.deck.draw_card()
        # Setup animation
        card.x, card.y = WIDTH - 100, 50
        card.target_x = 300 + len(hand.cards) * 40
        card.target_y = 400 + (100 * self.current_hand_idx) # Offset for split
        hand.add_card(card)
        self.animating = True
        
        if hand.is_bust():
            self.stand()

    def stand(self):
        self.current_hand_idx += 1
        if self.current_hand_idx >= len(self.player_hands):
            self.state = "DEALER_TURN"
            self.dealer_hand.cards[1].is_hidden = False # Reveal hole card
            self.play_dealer()

    def double_down(self):
        hand = self.player_hands[self.current_hand_idx]
        if self.balance >= self.current_bet and len(hand.cards) == 2:
            self.balance -= self.current_bet
            hand.bet += self.current_bet
            self.current_bet += self.current_bet
            self.hit()
            if self.state == "PLAYER_TURN":
                self.stand()

    def split(self):
        hand = self.player_hands[self.current_hand_idx]
        if self.balance >= self.current_bet and len(hand.cards) == 2 and hand.cards[0].value == hand.cards[1].value:
            self.balance -= self.current_bet
            
            new_hand = Hand()
            new_hand.bet = self.current_bet
            split_card = hand.cards.pop()
            split_card.target_x += 120 # Move it over
            split_card.target_y += 120
            new_hand.add_card(split_card)
            self.player_hands.append(new_hand)
            
            self.hit() # Hits the first hand
            
    def play_dealer(self):
        all_bust = all(h.is_bust() for h in self.player_hands)
        if not all_bust:
            while self.dealer_hand.calculate_value() < 17:
                card = self.deck.draw_card()
                card.x, card.y = WIDTH - 100, 50
                card.target_x = 300 + len(self.dealer_hand.cards) * 40
                card.target_y = 100
                self.dealer_hand.add_card(card)
                self.animating = True
        
        if self.animating:
            self.state = "DEALER_TURN_ANIMATING"
        else:
            self.resolve_game()

    def resolve_game(self):
        self.state = "GAME_OVER"
        dealer_val = self.dealer_hand.calculate_value()
        dealer_bust = self.dealer_hand.is_bust()

        payout = 0
        results = []

        for hand in self.player_hands:
            if hand.is_bust():
                results.append("BUST")
            elif dealer_bust:
                results.append("WIN")
                payout += hand.bet * 2
            elif hand.calculate_value() > dealer_val:
                results.append("WIN")
                payout += hand.bet * 2
            elif hand.calculate_value() == dealer_val:
                results.append("PUSH")
                payout += hand.bet
            else:
                results.append("LOSE")

        self.balance += payout
        if len(self.player_hands) == 1:
            if results[0] == "WIN":
                self.message = "YOU WIN!"
            elif results[0] == "LOSE":
                self.message = "YOU LOSE!"
            else:
                self.message = results[0]
        else:
            self.message = f"Split Results: {', '.join(results)}"

    def render(self):
        surface = pygame.Surface((WIDTH, HEIGHT))
        surface.fill(GREEN)
        
        # Draw Deck
        deck_rect = pygame.Rect(WIDTH - 100, 50, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(surface, BLUE, deck_rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, deck_rect, 2, border_radius=5)
        text = FONT.render("DECK", True, WHITE)
        text_rect = text.get_rect(center=deck_rect.center)
        surface.blit(text, text_rect)

        # Draw dealer cards
        for card in self.dealer_hand.cards:
            card.draw(surface)
            
        # Draw player cards
        for hand in self.player_hands:
            for card in hand.cards:
                card.draw(surface)

        # Draw Scores
        if self.state not in ["BETTING", "DEALING"]:
            idx = min(self.current_hand_idx, len(self.player_hands) - 1)
            p_val = self.player_hands[idx].calculate_value() if self.state != "GAME_OVER" else self.player_hands[0].calculate_value()
            p_text = FONT.render(f"Player: {p_val}", True, WHITE)
            surface.blit(p_text, (300, 550))
            
            if not self.dealer_hand.cards[1].is_hidden or self.state == "GAME_OVER":
                d_val = self.dealer_hand.calculate_value()
                d_text = FONT.render(f"Dealer: {d_val}", True, WHITE)
                surface.blit(d_text, (300, 50))

        # Draw Banners
        if self.state == "BETTING" and self.balance < 10:
            banner = BANNER_FONT.render("GAME OVER", True, RED)
            banner_rect = banner.get_rect(center=(WIDTH//2, HEIGHT//2))
            
            bg_rect = banner_rect.inflate(40, 20)
            
            # Semi-transparent background
            overlay = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, bg_rect.topleft)
            pygame.draw.rect(surface, RED, bg_rect, 3)
            
            surface.blit(banner, banner_rect)
        elif self.message:
            color = YELLOW if "PUSH" in self.message else GREEN if "WIN" in self.message or "BLACKJACK" in self.message else RED
            banner = BANNER_FONT.render(self.message, True, color)
            banner_rect = banner.get_rect(center=(WIDTH//2, HEIGHT//2))
            
            bg_rect = banner_rect.inflate(40, 20)
            
            # Semi-transparent background
            overlay = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            surface.blit(overlay, bg_rect.topleft)
            pygame.draw.rect(surface, color, bg_rect, 3)
            
            surface.blit(banner, banner_rect)
            
        return surface

def surface_to_pil(surface):
    raw_str = pygame.image.tostring(surface, "RGB", False)
    image = Image.frombytes("RGB", surface.get_size(), raw_str)
    return image

# --- Streamlit App ---
def main():
    st.set_page_config(page_title="Streamlit Blackjack", layout="wide")
    
    st.markdown("""
    <style>
    .stButton>button {
        font-weight: bold;
    }
    .main .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }
    [data-testid="stAppViewBlockContainer"] {
        padding-bottom: 0rem !important;
    }
    footer {
        display: none !important;
    }
    header {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title("♠️♥️ Blackjack 21 ♣️♦️")

    if 'game' not in st.session_state:
        st.session_state.game = BlackjackGame()

    game = st.session_state.game
    
    col_game, col_ui = st.columns([2, 1])

    with col_game:
        # Placeholder for the game board
        placeholder = st.empty()
        
    with col_ui:
        st.subheader("Chip Stack")
        st.metric(label="Balance", value=f"${game.balance}")
        if game.state != "BETTING":
            st.metric(label="Current Bet", value=f"${game.current_bet}")
        else:
            if game.balance < 10:
                st.error("Game Over! You are out of chips.")
            else:
                max_bet = min(500, game.balance)
                if max_bet <= 10:
                    st.metric(label="Bet Amount", value="$10")
                    bet_amount = 10
                else:
                    bet_amount = st.slider("Bet Amount", min_value=10, max_value=max_bet, step=10, value=min(100, max_bet))
                if st.button("Deal", use_container_width=True):
                    game.deal(bet_amount)

        st.markdown("---")
        st.subheader("Player Actions")
        action_col1, action_col2 = st.columns(2)
        
        can_hit = game.state == "PLAYER_TURN" and not game.animating
        can_stand = game.state == "PLAYER_TURN" and not game.animating
        can_double = can_hit and len(game.player_hands[game.current_hand_idx].cards) == 2 and game.balance >= game.player_hands[game.current_hand_idx].bet
        
        can_split = can_hit and len(game.player_hands[game.current_hand_idx].cards) == 2 and \
                    game.player_hands[game.current_hand_idx].cards[0].value == game.player_hands[game.current_hand_idx].cards[1].value and \
                    game.balance >= game.player_hands[game.current_hand_idx].bet

        with action_col1:
            if st.button("Hit", use_container_width=True, disabled=not can_hit):
                game.hit()
            if st.button("Double Down", use_container_width=True, disabled=not can_double):
                game.double_down()
                
        with action_col2:
            if st.button("Stand", use_container_width=True, disabled=not can_stand):
                game.stand()
            if st.button("Split", use_container_width=True, disabled=not can_split):
                game.split()
                
        if game.state == "GAME_OVER":
            if st.button("Next Round", use_container_width=True, type="primary"):
                game.state = "BETTING"
                game.message = ""
                game.reset_round()
                st.rerun()

        st.markdown("---")
        st.subheader("Options")
        if st.button("Restart Game", use_container_width=True):
            st.session_state.game = BlackjackGame()
            st.rerun()

    if game.animating:
        while game.animating:
            game.update_animations()
            surf = game.render()
            placeholder.image(surface_to_pil(surf), use_container_width=True)
            time.sleep(0.02)
        st.rerun()
    else:
        surf = game.render()
        placeholder.image(surface_to_pil(surf), use_container_width=True)

if __name__ == "__main__":
    main()
