import json
import os

def load_all_characters():
	characters = {}
	character_files = os.listdir("characters")
	for file in character_files:
		with open(f"characters/{file}") as f:
			characters[file[:-5]] = json.load(f)
	return(characters)

# class Character:
# 	def __init__(self, file_name):
# 		with open(file_name) as f:
# 			self.data = json.load(f)

if __name__ == "__main__":
	load_all_characters()