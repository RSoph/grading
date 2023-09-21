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

def build_rubric(rubric_file, already_counted):
	# already_counted represents the points that are seperate from the essay
	# portion. They must be added manually into the available_points
	# because they does not come from the tier system.
	with open(rubric_file, newline='') as csvfile:
		score_rubric = {'available_points': already_counted}
		rubric_rows = csv.reader(csvfile, delimiter='	')
		# call next() once to skip the first row, which is just headers
		next(rubric_rows, None)
		counter = 1
		for row in rubric_rows:
			score_rubric[counter] = {
				"name": row[0],
				"max_points": int(row[2]),
			}
			# import pdb; pdb.set_trace()
			for integer in range(1, 7): # The range here is: (1, number of tiers plus one) That's the same as the number of rows in the whole csv, but I haven't figured out how to do that.
				score_rubric[counter][integer] = {"description": row[(integer * 2)-1], "points": int(row[integer * 2])}
			# This assumes that the top tier for each section gets
			# maximum points, i.e. 60 out of 60.
			score_rubric["available_points"] += int(row[2])
			counter += 1
	print(score_rubric)
	return score_rubric
