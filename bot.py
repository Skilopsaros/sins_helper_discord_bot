import discord
import sins_functions
import re
from matplotlib import pyplot as plt
import os
from dotenv import load_dotenv
import characters

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())


character_dict = characters.load_all_characters()

def format_diceroll(results, target):
	dice_string = ""
	for die in results:
		if isinstance(die, list):
			dice_string += "("
			for d in die:
				if d >= target:
					dice_string += f"**{d}**, "
				else:
					dice_string += f"{d}, "
			dice_string = dice_string[:-2] + "), "
		else:
			if die >= target:
				dice_string += f"**{die}**, "
			else:
				dice_string += f"{die}, "
	return(dice_string[:-2])


@client.event
async def on_message(message):
	if message.author == client.user:
		return
	
	if message.content[0:2] == "$r":
		print("rolling dice")
		content = message.content.split()
		add = 0
		difficulty = 0
		pool_bonus = 0
		destroyer = False
		for info in content:
			if re.match("s[1-9]+", info):
				add = int(info[1:])
			if re.match("d[1-9]+", info):
				difficulty = int(info[1:])
			if re.match("p[1-9]+", info):
				pool_bonus = int(info[1:])
			if "-sp" == info:
				add += 1
				pool_bonus += 1
			if "-dst" == info:
				destroyer = True
		if message.content[2] == "c":
			character = character_dict[content[1]]
			if "+" in content[2]:
				base_attribute, attribute_bonus = content[2].split("+")
				attribute = character["attributes"][base_attribute] + int(attribute_bonus)
				atr_name = base_attribute
			else:
				atr_name = content[2]
				attribute = character["attributes"][content[2]]
			if destroyer:
				if atr_name == "body":
					attribute += 3
				elif atr_name == "prowess":
					attribute += 2
			if attribute <= 6:
				n_dice = attribute + character["creed"]
			else:
				n_dice = 6 + character["creed"]
				add += attribute - 6
			skill = character["skills"][content[3]]
		else:
			n_dice = int(content[1])
			skill = int(content[2])

		n_dice += pool_bonus
		target = 7 - int(skill)
		result = sins_functions.roll(int(n_dice), int(skill), add=add, difficulty=difficulty)
		dice_string = format_diceroll(result[2], target)
		success_string = f"Rolled **{result[0]}** successes"
		if add:
			success_string = f"Rolled {result[0]-add} + {add} = **{result[0]}** successes"
		await message.channel.send(f"{success_string} \n {dice_string}")

	elif message.content[0:2] == "$p":
		content = message.content.split()
		difficulty = None
		for info in content:
			if re.match("d[1-9]+", info):
				difficulty = int(info[1:])
		results, fig = sins_functions.roll_distribution(int(content[1]), int(content[2]), difficulty=difficulty)
		fig.savefig("temp.png")
		await message.channel.send(file=discord.File('temp.png'))
		os.remove("temp.png")


client.run(TOKEN)
