import json
import pathlib
from fireplace import game
from fireplace.card import Card
from fireplace.utils import *
from fireplace.actions import Hit
from fireplace.actions import Shuffle
from fireplace.dsl.selector import *
from fireplace.deck import Deck
from .setup_players import create_players

class Scenario:
	def __init__(self, scenario_name):
		#parthstring = "C:\\Users\\Anton\\Desktop\\ThesisProject-master\\aiThesis\\scenarios\\" + scenario_name + ".json"
		parthstring = "C:\\Users\\45606\Documents\\ITU - Games\\ThesisProject\\aiThesis\\scenarios\\" + scenario_name + ".json"

		with open(parthstring) as f:
			data = json.load(f)

		players = create_players(data['player1Name'], data['player2Name'], data['player1Hero'], data['player2Hero'], data['player1Deck'], data['player2Deck'], data['player1Agent'], data['player2Agent'])

		self.player1 = players[0]
		self.player2 = players[1]

		self.player1_hand = data['player1Hand']
		self.player2_hand = data['player2Hand']

		self.player1_field = data['player1Field']
		self.player2_field = data['player2Field']

		self.player1_health = data['player1Health']
		self.player2_health = data['player2Health']

		self.player1_deck = data['player1Deck']
		self.player2_deck = data['player2Deck']

		self.start_at_turn = data['beginScenarioAtTurn']
		self.starting_player = data['startingPlayer']

	def setup_scenario(self, game):
		#player hand
		self.set_player_hand(self.player1_hand, self.player1)
		self.set_player_hand(self.player2_hand, self.player2)

		#player field
		self.set_player_field(self.player1_field, self.player1)
		self.set_player_field(self.player2_field, self.player2)

		#player health
		self.set_player_health(self.player1_health, self.player1, game)
		self.set_player_health(self.player2_health, self.player2, game)

		#player deck
		self.set_player_deck(self.player1_deck, self.player1)
		self.set_player_deck(self.player2_deck, self.player2)


		self.print_player_stats(game)


	def print_player_stats(self, game):
		player1 = game.players[0]
		player2 = game.players[1]
		print("\n\n")

		print("*****************STATS*****************")
		print("*****************PLAYER 1*****************")
		print("player health: " + str(player1.hero.health))
		print("player hand: " + str(player1.hand))
		print("player field: " + str(player1.field))
		print("player deck: " + str(player1.deck))

		print("\n")

		print("*****************PLAYER 2*****************")
		print("player health: " + str(player2.hero.health))
		print("player hand: " + str(player2.hand))
		print("player field: " + str(player2.field))
		print("player deck: " + str(player2.deck))

		print("\n\n")
		print("SCENARIO STARTS")
		print("\n\n")



	def add_card_to_field(self, card_id, player):
		player.summon(card_id)

	def set_player_field(self, cards_on_board, player):
		player.field = CardList()
		for card in cards_on_board:
			self.add_card_to_field(card, player)

	def add_card_to_hand(self, card_id, player):
		player.give(card_id)

	def set_player_hand(self, cards_in_hand, player):
		player.hand = CardList()
		for card in cards_in_hand:
			self.add_card_to_hand(card, player)

	def set_player_deck(self, cards_in_deck, player):
		cards = []
		for card in cards_in_deck:
			c = Card(card)
			c.controller = player
			cards.append(c)
		player.deck = Deck(cards)

	def set_player_health(self, hero_health, player, game):
		game.queue_actions(game, [Hit(player.hero, 30-hero_health)])

	def skip_to_next_turn(self, game):
		game.queue_actions(game.current_player, [Shuffle(game.current_player, "BT_019")]) #hack to prevent deck to run out of cards before getting to the right turn
		game.end_turn()
		return game





