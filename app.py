'''
A Legends of Runeterra Game Logger
Just run this script before your game starts to run
python app.py

Made by https://www.linkedin.com/in/nascimentovictor/
'''

import requests
import time
import json


class GameState:
	def __init__(self):
		self.__menus = 'Menus'
		self.__in_game = 'InProgress'

		self.__base = 'http://127.0.0.1:21337'
		self.__board = '/positional-rectangles'
		self.__result = '/game-result'
		self.__deck = '/static-decklist'
		
		self.__history = 'history.log'
		self.__results = 'results.log'
		
		self.__last_str = ''
		self.__opponent = ''
		self.__my_deck = ''
		self.__starttime = ''

		self.state = 'IDLE'


	def is_new_game(self, state:dict) -> bool:
		return state['OpponentName'] != self.__opponent and state['OpponentName'] is not None


	def game_ended(self, state:dict) -> bool:
		return state['OpponentName'] is None and self.__opponent != ''


	def __deck_code(self) -> str:
		return json.loads(requests.get(f'{self.__base}{self.__deck}').text)['DeckCode']


	def update_log(self, str_board:str) -> None:
		if self.__last_str != str_board:
			with open(f'./matches/{self.__starttime}_{self.__opponent}.log', 'a') as f:
				f.write(f'{str_board}, \n')
			self.__last_str = str_board


	def run(self):
		x = self.__call__()
		x_dict = json.loads(x)

		if self.is_new_game(x_dict):
			print("New Game Detected")
			self.__opponent = x_dict['OpponentName']
			self.__starttime = str(int(time.time()))
			self.__my_deck = self.__deck_code()
			self.state = 'PLAYING'

		if self.game_ended(x_dict):
			print("Game Ended")
			with open(self.__results, 'a') as f:
				res = json.loads(self.__game_result())
				res['EndTime'] = str(int(time.time()))
				res['OpponentName'] = self.__opponent
				res['DeckCode'] = self.__my_deck
				f.write(f'{json.dumps(res)}, \n')
			self.__opponent = ''
			self.__my_deck = ''
			self.state = 'IDLE'

		if self.state == 'PLAYING':
			self.update_log(x)
		

	def __call__(self) -> str:
		return requests.get(f'{self.__base}{self.__board}').text


	def __game_result(self) -> str:
		return requests.get(f'{self.__base}{self.__result}').text
		

def main():
	gs = GameState()
	print(json.loads(gs()))
	while True:
		gs.run()
		time.sleep(2)


if __name__ == '__main__':
	main()