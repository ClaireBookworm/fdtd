import itertools

def total_cap(capacitances):
	"""
	Takes in [] of capacitances. 
	"""
	total = 0
	for cap in capacitances:
		total += float(1/cap)
	return float(1/total)


def calc_values(amount, goal, existing):
	"""
	Takes in the number of capacitors (amount), the goal cap
	(goal), and some values that we already know as a []. 
	"""
	result = []
	for val in existing: 
		if total_cap([ val for i in range(amount)]) == goal:
			result.append(val)
	return val

if __name__ == "__main__":
	print(total_cap([0.8, 0.8]))
	existing = [1.0, 1.5, 2.2, 3.0, 3.3, 3.6, 3.9, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1, 10, 12, 15, 18, 20, 22, 24, 27, 30, 33, 36, 39, 47]
	print(calc_values (4, 0.989, existing))