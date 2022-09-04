import csv
import pdfkit
import jinja2
import helpers

# This is a bunch of stuff I copied and pasted from Stack Overflow.
# It processes html templates.
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "templates/paper_report_template_full_table.html"
template = templateEnv.get_template(TEMPLATE_FILE)



# Establish class-wide variables
class_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}
rubric_csv = 'rubrics/final_paper_rubric.csv'
scores_csv = 'scores/paper_scores.csv'
score_rubric = helpers.build_rubric(rubric_csv, 0)

with open(scores_csv, newline='') as csvfile:
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
		comments = row[5]

		percent = round(((total_score / score_rubric["available_points"]) * 100), 2)
		grade = helpers.letter_grade(percent)

		class_count[grade[0]] += 1

		context = {
			"student_name": row[0],
			"sections": {
			},
			"final_grade": {
				"points": total_score,
				"available_points": score_rubric["available_points"],
				"percent": percent,
				"letter": grade,
				"comments": comments,
			},
			"rubric": score_rubric,
		}

		for i in range(1, 5):
			context["sections"][i] = int(row[i])

		print(context["student_name"] + "   " + context["final_grade"]["letter"])

		# fill in the html with the context
		sourceHtml = template.render(context=context)

		# process the html into a pdf, name it correctly
		file_name = "reports/" + context["student_name"] + " final paper.pdf"
		pdfkit.from_string(sourceHtml, file_name)

print(class_count)
