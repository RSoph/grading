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

with open('final_paper_scores.csv', newline='') as csvfile:
	paper_scores = csv.reader(csvfile, delimiter=',', quotechar='|')
	# call next() once to skip the first row, which is just headers
	next(paper_scores, None)
	for row in paper_scores:
		total_score = 0
		# for k, v in score_rubric.items():
		# 	# import pdb; pdb.set_trace()
		# 	# print(v)
		# 	total_score += int(v[int(row[1])]["points"])
		# 	total_score += int(v[int(row[2])]["points"])
		# 	total_score += int(v[int(row[3])]["points"])
		# 	total_score += int(v[int(row[4])]["points"])


		total_score = (
			score_rubric[1][int(row[1])]["points"] +
			score_rubric[2][int(row[2])]["points"] +
			score_rubric[3][int(row[3])]["points"] +
			score_rubric[4][int(row[4])]["points"]
		)

		print("total score:")
		print(total_score)

		if 190 <= total_score <= 200:
			letter = "A"
		elif 180 <= total_score <= 189:
			letter = "A-"
		else:
			letter = "F"

		context = {
			"name": row[0],
			"1": score_rubric[1][int(row[1])],
			"2": score_rubric[2][int(row[2])],
			"3": score_rubric[3][int(row[3])],
			"4": score_rubric[4][int(row[4])],
			"final_grade": {
				"points": total_score,
				"available_points": 200,
				"letter": letter,
			},
		}

		print(context)

		# fill in the html with the context
		sourceHtml = template.render(context=context)

		# process the html into a pdf, name it correctly
		file_name = context["name"] + ".pdf"
		pdfkit.from_string(sourceHtml, file_name)
