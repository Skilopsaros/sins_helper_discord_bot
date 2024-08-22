import json
import os
from collections import UserDict

def load_all_characters():
	characters = {}
	character_files = os.listdir("characters")
	for file in character_files:
		characters[file[:-5]] = Character(f"characters/{file}")
	return(characters)

class Character(UserDict):
	def __init__(self, file_name):
		self.file_name = file_name
		with open(file_name) as f:
			super().__init__(json.load(f))

	def set_atr(self, attribute, new_val):
		if new_val < 0:
			new_val = 0
		self.data["attributes"][attribute] = new_val
		self.save_character()
	
	def raise_atr(self, attribute, raise_by=1):
		self.set_atr(attribute, self.data["attributes"][attribute]+raise_by)
		self.save_character()
	
	def set_skill(self, skill, new_val):
		if new_val > 4:
			new_val = 4
		if new_val < 0:
			new_val = 0
		self.data["skills"][skill] = new_val
		self.save_character()

	def raise_skill(self, skill, raise_by=1):
		self.set_skill(skill, self.data["skills"][skill]+raise_by)
		self.save_character()
	
	def set_creed(self, kind, new_val):
		self.data["creed"][kind] = new_val
		self.save_character()
		
	def raise_creed(self, raise_by=1):
		self.set_creed("temporary", self.data["creed"]["temporary"]+raise_by)
		if self.data["creed"]["temporary"] > 6:
			self.raise_creed(raise_by=-7)
			self.set_creed("permanent", self.data["creed"]["temporary"]+1)
		if self.data["creed"]["temporary"] < 0:
			self.raise_creed(raise_by=7)
			self.set_creed("permanent", self.data["creed"]["temporary"]-1)
		self.save_character()

	def __str__(self):
		return(json.dumps(self.data, indent=1))
	
	def save_character(self):
		with open(self.file_name, "w") as f:
			f.write(str(self))



if __name__ == "__main__":
	characters = load_all_characters()