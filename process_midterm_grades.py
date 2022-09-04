import csv
import pdfkit
import jinja2
import helpers

# This is a bunch of stuff I copied and pasted from Stack Overflow.
# It processes html templates.
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "templates/midterm_report_template_full_table.html"
template = templateEnv.get_template(TEMPLATE_FILE)

class_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

# Open the rubric csv and establish a bunch of variables
score_rubric = {}
with open('rubrics/midterm_paper_rubric.csv', newline='') as csvfile:
	rubric_rows = csv.reader(csvfile, delimiter='	')
	# call next() once to skip the first row, which is just headers
	next(rubric_rows, None)
	counter = 1
	# available_points would normally start with 0, but I'm hardcoding in
	# the 10 and 5 for the first two sections.
	available_points = 15
	for row in rubric_rows:
		score_rubric[counter] = {
			"name": row[0],
			"max_points": int(row[2]),
			1: {"description": row[1], "points": int(row[2])},
			2: {"description": row[3], "points": int(row[4])},
			3: {"description": row[5], "points": int(row[6])},
			4: {"description": row[7], "points": int(row[8])},
			5: {"description": row[9], "points": int(row[10])},
			6: {"description": row[11], "points": int(row[12])},
		}
		# This assumes that the top tier for each section gets
		# maximum points, i.e. 60 out of 60.
		available_points += int(row[2])
		counter += 1

# Open the scores csv, iterate through the rows:
with open('scores/midterm_scores.csv', newline='') as csvfile:
	paper_scores = csv.reader(csvfile, delimiter='	', quotechar='|')
	# call next() once to skip the first row, which is just headers
	next(paper_scores, None)

	for row in paper_scores:
		# Each row represents one student. Create a template context for them.
		paper_score = (
			score_rubric[1][int(row[1])]["points"] +
			score_rubric[2][int(row[2])]["points"] +
			score_rubric[3][int(row[3])]["points"] +
			score_rubric[4][int(row[4])]["points"]
		)
		total_score = (
			paper_score +
			int(row[5]) + # This is just the raw number of points in the
			int(row[6])   # "questions" and "thesis" columns
		)
		comments = row[7]

		percent = round(((total_score / available_points) * 100), 2)
		grade = helpers.letter_grade(percent)

		class_count[grade[0]] += 1

		context = {
			"student_name": row[0],
			"sections": {},
			"final_grade": {
				"paper_score": paper_score,
				"total_score": total_score,
				"available_points": available_points,
				"percent": percent,
				"letter": grade,
				"comments": comments,
			},
			"rubric": score_rubric,
		}

		for i in range(1, 5):
			context["sections"][i] = int(row[i])
		context["questions"] = int(row[5])
		context["thesis"] = int(row[6])

		print(context["student_name"] + "   " + context["final_grade"]["letter"])

		# fill in the html with the context
		sourceHtml = template.render(context=context)

		# process the html into a pdf, name it correctly
		file_name = "reports/" + context["student_name"] + " midterm paper.pdf"
		pdfkit.from_string(sourceHtml, file_name)

print(class_count)
