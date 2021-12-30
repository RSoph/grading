import csv

# Open the rubric csv and establish a bunch of variables

score_rubric = {}
with open('rubric.csv', newline='') as csvfile:
	rubric_rows = csv.reader(csvfile, delimiter=',')
	# call next() once to skip the first row, which is just headers
	next(rubric_rows, None)
	for row in rubric_rows:
		score_rubric[row[0]] = {
			1: {"description": row[1], "points": row[2]},
			2: {"description": row[3], "points": row[4]},
			3: {"description": row[5], "points": row[6]},
			4: {"description": row[7], "points": row[8]},
	},

# Open the scores csv, iterate through the rows:
	# create a template context for the student

with open('final_paper_scores.csv', newline='') as csvfile:
	paper_scores = csv.reader(csvfile, delimiter=',', quotechar='|')
	# call next() once to skip the first row, which is just headers
	next(paper_scores, None)
	for row in paper_scores:

		total_score = (
			score_rubric["section_one"][row[1]]["points"] +
			score_rubric["section_two"][row[2]]["points"] +
			score_rubric["section_three"][row[3]]["points"] +
			score_rubric["section_four"][row[4]]["points"]
		)

		if 190 <= total_score between <= 200:
			letter = "A"
		elif 180 <= total_score between <= 189:
			letter = "A-"
		else:
			letter = "F"

		context = {
			"name": row[0],
			"section_one": score_rubric["section_one"][row[1]],
			"section_two": score_rubric["section_two"][row[2]],
			"section_three": score_rubric["section_three"][row[3]],
			"section_four": score_rubric["section_four"][row[4]],
			"final_grade": {
				"points": total_score,
				"available_points": 200,
				"letter": letter,
			},
		}

		# fill in the html with the context
		# process the html into a pdf, name it correctly


