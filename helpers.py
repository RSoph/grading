import csv

# In the case that someone's percent starts at 89.5, the ones will be rounded up
# to 10, so we need to have a key of 10 in the adjustments dict.
def letter_grade(percent):
	letters = {
		9: "A",
		8: "B",
		7: "C",
		6: "D",
	}
	adjustments = {
		10: "+",
		9: "+",
		8: "+",
		7: "+",
		6: "",
		5: "",
		4: "",
		3: "",
		2: "-",
		1: "-",
		0: "-",
	}
	if percent >= 100:
		return "A"
	elif (percent // 10) in letters:
		letter_grade = letters[percent // 10] # floordiv(percent, 10), gives just the tens digit.
		adjustment = adjustments[round(percent % 10, 0)] # mod(percent, 10) gives the ones only, then round to nearest integer.
		grade = letter_grade + adjustment
		if grade == "A+":
			return "A"
		else:
			return grade
	else:
		return "F"

def build_rubric(rubric_file, minimum_score):
	# Can we rewrite this to avoid hardcoding the assignment numbers?
	# There should be a second counter for number of tiers, and it should
	# add score_ruberic[counter][tier_counter] = {tier_counter: {"description": row[(tier_counter * 2)-1], "points": int(row[tier_counter * 2])"}}.
	# I'm not sure the above is exactly right, but try it!
	with open(rubric_file, newline='') as csvfile:
		score_rubric = {'available_points': minimum_score}
		rubric_rows = csv.reader(csvfile, delimiter='	')
		# call next() once to skip the first row, which is just headers
		next(rubric_rows, None)
		counter = 1
		for row in rubric_rows:
			score_rubric[counter] = {
				"name": row[0],
				"max_points": int(row[2]),
				1: {"description": row[1], "points": int(row[2])},
				2: {"description": row[3], "points": int(row[4])},
				3: {"description": row[5], "points": int(row[6])},
				4: {"description": row[7], "points": int(row[8])},
				5: {"description": row[9], "points": int(row[10])},
				# 6: {"description": row[11], "points": int(row[12])},
			}
			# This assumes that the top tier for each section gets
			# maximum points, i.e. 60 out of 60.
			score_rubric["available_points"] += int(row[2])
			counter += 1
	return score_rubric
