import csv
import pdfkit
import jinja2
import helpers

# This is a bunch of stuff I copied and pasted from Stack Overflow.
# It processes html templates.
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "templates/midterm_report_template.html"
template = templateEnv.get_template(TEMPLATE_FILE)

# Establish class-wide variables
class_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0, "number_of_students": 0, "score_total": 0, "score_average": 0}
rubric_csv = 'rubrics/midterm_paper_rubric.csv'
scores_csv = 'scores/midterm_scores.csv'
score_rubric = helpers.build_rubric(rubric_csv, 15)
# ^ Normally available points starts at 0, but here we're adding in sections 1 and 2 manually

# Open the scores csv, iterate through the rows:
with open(scores_csv, newline='') as csvfile:
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
		total_score = paper_score + int(row[5]) # This is just the raw number of points in part 1
		comments = row[6]

		percent = round(((total_score / score_rubric["available_points"]) * 100), 2)
		grade = helpers.letter_grade(percent)

		class_count[grade[0]] += 1
		class_count["number_of_students"] += 1
		class_count["score_total"] += percent

		context = {
			"student_name": row[0],
			"sections": {},
			"questions": int(row[5]),
			"final_grade": {
				"paper_score": paper_score,
				"total_score": total_score,
				"available_points": score_rubric["available_points"],
				"percent": percent,
				"letter": grade,
				"comments": comments,
			},
			"rubric": score_rubric,
		}

		for i in range(1, 5):
			context["sections"][i] = int(row[i])

		student_name_last_first = context["student_name"].split(" ")[-1] + " " + (" ").join(context["student_name"].split(" ")[0:-1])
		print(student_name_last_first + "   " + context["final_grade"]["letter"])

		# fill in the html with the context, process the html into a pdf, name it correctly
		sourceHtml = template.render(context=context)
		file_name = "reports/" + student_name_last_first + " midterm paper.pdf"
		pdfkit.from_string(sourceHtml, file_name)

class_count["score_average"] = class_count["score_total"] / class_count["number_of_students"]
print(class_count)
