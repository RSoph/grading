import csv
import pdfkit
import jinja2

# This is a bunch of stuff I copied and pasted from Stack Overflow.
# It processes html templates.
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "paper_report_template.html"
template = templateEnv.get_template(TEMPLATE_FILE)

def letter_grade(percent):
	letters = {
		9: "A",
		8: "B",
		7: "C",
		6: "D",
	}
	adjustments = {
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

# Open the rubric csv and establish a bunch of variables
score_rubric = {}
with open('paper_rubric.csv', newline='') as csvfile:
	rubric_rows = csv.reader(csvfile, delimiter='	')
	# call next() once to skip the first row, which is just headers
	next(rubric_rows, None)
	counter = 1
	available_points = 0
	for row in rubric_rows:
		score_rubric[counter] = {
			"name": row[0],
			1: {"description": row[1], "points": int(row[2])},
			2: {"description": row[3], "points": int(row[4])},
			3: {"description": row[5], "points": int(row[6])},
			4: {"description": row[7], "points": int(row[8])},
		}
		# This assumes that the top tier for each section gets
		# maximum points, i.e. 60 out of 60.
		available_points += int(row[2])
		counter += 1

# Open the scores csv, iterate through the rows:
with open('paper_scores.csv', newline='') as csvfile:
	paper_scores = csv.reader(csvfile, delimiter='	', quotechar='|')
	# call next() once to skip the first row, which is just headers
	next(paper_scores, None)
	for row in paper_scores:
		# Each row represents one student. Create a template context for them.
		total_score = (
			score_rubric[1][int(row[1])]["points"] +
			score_rubric[2][int(row[2])]["points"] +
			score_rubric[3][int(row[3])]["points"] +
			score_rubric[4][int(row[4])]["points"]
		)
		print("total score:")
		print(total_score)

		percent = round(((total_score / available_points) * 100), 2)
		grade = letter_grade(percent)

		context = {
			"student": {
				"name": row[0]
			},
			"sections": {
			},
			"final_grade": {
				"points": total_score,
				"available_points": available_points,
				"percent": percent,
				"letter": grade,
			},
		}

		for i in range(1, 5):
			context["sections"][str(i)] = {
					"name": score_rubric[i]["name"],
					"tier_description": score_rubric[i][int(row[i])]["description"],
					"tier_points": score_rubric[i][int(row[i])]["points"],
				}

		print(context)

		# fill in the html with the context
		sourceHtml = template.render(context=context)

		# process the html into a pdf, name it correctly
		file_name = context["student"]["name"] + "final paper.pdf"
		pdfkit.from_string(sourceHtml, file_name)
