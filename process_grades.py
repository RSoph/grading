import csv
import pdfkit
# import wkhtmltopdf
import jinja2

# This is a bunch of stuff I copied and pasted from Stack Overflow.
# It processes html templates.
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "report_template.html"
template = templateEnv.get_template(TEMPLATE_FILE)

# Open the rubric csv and establish a bunch of variables
score_rubric = {}
with open('rubric.csv', newline='') as csvfile:
	rubric_rows = csv.reader(csvfile, delimiter=',')
	# call next() once to skip the first row, which is just headers
	next(rubric_rows, None)
	counter = 1
	for row in rubric_rows:
		score_rubric[counter] = {
			"name": row[0],
			1: {"description": row[1], "points": int(row[2])},
			2: {"description": row[3], "points": int(row[4])},
			3: {"description": row[5], "points": int(row[6])},
			4: {"description": row[7], "points": int(row[8])},
		}
		counter += 1

# Open the scores csv, iterate through the rows:
	# create a template context for the student

print(score_rubric)

available_points = 200
letters = {
	10: "A",
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
	3: "-",
	2: "-",
	0: "-",
}

with open('final_paper_scores.csv', newline='') as csvfile:
	paper_scores = csv.reader(csvfile, delimiter=',', quotechar='|')
	# call next() once to skip the first row, which is just headers
	next(paper_scores, None)
	for row in paper_scores:
		total_score = (
			score_rubric[1][int(row[1])]["points"] +
			score_rubric[2][int(row[2])]["points"] +
			score_rubric[3][int(row[3])]["points"] +
			score_rubric[4][int(row[4])]["points"]
		)
		print("total score:")
		print(total_score)

		percent = (total_score / available_points) * 100

		if percent == 100:
			grade = "A"
		elif (percent // 10) in letters:
			letter_grade = letters[percent // 10]
			adjustment = adjustments[percent % 10]
			grade = letter_grade + adjustment
		else:
			grade = "F"

		if grade == "A+":
			grade = "A"

		context = {
			"student": {
				"name": row[0]
			},
			"sections": {
				"1": {
					"name": score_rubric[1]["name"],
					"tier_description": score_rubric[1][int(row[1])]["description"],
					"tier_points": score_rubric[1][int(row[1])]["points"],
				},
				"2": {
					"name": score_rubric[2]["name"],
					"tier_description": score_rubric[2][int(row[2])]["description"],
					"tier_points": score_rubric[2][int(row[2])]["points"],
				},
				"3": {
					"name": score_rubric[3]["name"],
					"tier_description": score_rubric[3][int(row[3])]["description"],
					"tier_points": score_rubric[3][int(row[3])]["points"],
				},
				"4": {
					"name": score_rubric[4]["name"],
					"tier_description": score_rubric[4][int(row[4])]["description"],
					"tier_points": score_rubric[4][int(row[4])]["points"],
				},
			},
			"final_grade": {
				"points": total_score,
				"available_points": available_points,
				"letter": grade,
			},
		}

		print(context)

		# fill in the html with the context
		sourceHtml = template.render(context=context)

		# process the html into a pdf, name it correctly
		file_name = context["student"]["name"] + ".pdf"
		pdfkit.from_string(sourceHtml, file_name)
