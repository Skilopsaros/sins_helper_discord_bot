import random as rng
from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np
from scipy import stats

def roll(n_dice, skill_level, explode=None, add=0, difficulty=0):
	if explode is None:
		explode = False if skill_level == 0 else True

	dice_results = [rng.choice(range(1,7)) for _ in range(n_dice)]
	results_per_die = []
	non_6_results = []
	if explode:
		explosion_results = []
		for die in dice_results:
			if die == 6:
				new_result = roll(1, skill_level, explode)[1]
				explosion_results.extend(new_result)
				explosion_and_results = [6]
				explosion_and_results.extend(new_result)
				results_per_die.append(explosion_and_results)
			else:
				non_6_results.append(die)
		dice_results.extend(explosion_results)
	dice_results.sort(reverse=True)
	results_per_die.sort(key=lambda x: len(x), reverse=True)
	non_6_results.sort(reverse=True)
	results_per_die.extend(non_6_results)

	skill_level = max(skill_level, 1)
	n_success = 0
	for die in dice_results:
		if die >= 7-skill_level:
			n_success += 1
	n_success += add - difficulty
	return(n_success, dice_results, results_per_die)

def roll_until(target, n_dice, skill_level, add=0, difficulty=0, n_tries=1):
	successes= roll(n_dice, skill_level, add=add, difficulty=difficulty)[0]
	if successes < target:
		return(roll_until(target, n_dice, skill_level, add+successes, difficulty, n_tries+1))
	return(n_tries)

def roll_distribution(n_dice, skill_level, n_rolls=10000, add=0, plot=True, difficulty=None, show=False):
	results = []
	for _ in range(n_rolls):
		results.append(roll(n_dice, skill_level, add=add)[0])
	results = np.array(results)
	if difficulty:
		probability_of_success = np.where(results >= difficulty, 1, 0).sum()/n_rolls
		print(probability_of_success)

	if plot:
		mode = stats.mode(results, keepdims=False)
		modal_bin = [mode[0]-0.5,mode[0]+0.5]
		bins = np.arange(-0.5, max(results)+1.5, 1)
		fig = plt.figure()
		ax = fig.add_subplot(111)
		ax.title.set_text(f"Roll {n_dice} dice with skill {skill_level}")
		ax.hist(results, bins, weights=np.ones(len(results)) / len(results))
		ax.hist([mode[0] for x in range(mode[1])], modal_bin, weights=np.ones(mode[1]) / len(results))
		ax.yaxis.set_major_formatter(ticker.PercentFormatter(1))
		if difficulty:
			fig.suptitle(f"Roll {n_dice} dice with skill {skill_level}, difficulty {difficulty}",fontsize=20, y=0.99)
			ax.title.set_text(f"probability of success: {probability_of_success*100:.2f}%")
			ax.plot([difficulty, difficulty], [0, mode[1]/ len(results)], linewidth=4)
		ax.set_xticks(range(max(results)+1))
		if show:
			plt.show()
	return(results, fig)


if __name__ == "__main__":
	roll_distribution(3, 3, show=True, difficulty=2)
	pass