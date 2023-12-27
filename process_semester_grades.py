import csv
import pdfkit
import jinja2
import helpers

# This is a bunch of stuff I copied and pasted from Stack Overflow.
# It processes html templates.
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "templates/semester_report_template.html"
template = templateEnv.get_template(TEMPLATE_FILE)

# Establish some class-wide variables
scores_csv = 'scores/semester_scores.csv'
class_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0, "number_of_students": 0, "score_total": 0, "score_average": 0}
# OMG you just hardcoded this!?
available_points = 750

# Open the scores csv, iterate through the rows:
with open(scores_csv, newline='') as csvfile:
	paper_scores = csv.reader(csvfile, delimiter='	', quotechar='|')
	# The first row is headers, just read them into a list for lableling later.
	assignment_names = next(paper_scores)[1:]
	for row in paper_scores:
		# Each row represents one student. Create a template context for them.
		total_score = 0
		for points in row[2:]:
			total_score += int(points)

		percent = round(((total_score / available_points) * 100), 2)
		grade = helpers.letter_grade(percent)
		class_count[grade[0]] += 1
		class_count["number_of_students"] += 1
		class_count["score_total"] += percent
		student_name_last_first = row[0] + " " + row[1]
		student_name_first_last = row[1] + " " + row[0]
		context = {
			"student_name": student_name_first_last,
			"sections": [],
			"final_grade": {
				"points": total_score,
				"available_points": available_points,
				"percent": percent,
				"letter": grade,
			},
		}

		for i in range(2, len(assignment_names)+1):
			context["sections"].append({assignment_names[i-1]: int(row[i])})

		print(student_name_last_first + "   " + context["final_grade"]["letter"] + "   " + str(context["final_grade"]["percent"]))

		# fill in the html with the context
		sourceHtml = template.render(context=context)

		# process the html into a pdf, name it correctly
		file_name = "reports/" + student_name_last_first + " class grade.pdf"
		pdfkit.from_string(sourceHtml, file_name)

class_count["score_average"] = class_count["score_total"] / class_count["number_of_students"]
print(class_count)
