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

# OMG you just hardcoded this!?
available_points = 640

class_count = {"A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

# Open the scores csv, iterate through the rows:
with open('scores/semester_scores.csv', newline='') as csvfile:
	paper_scores = csv.reader(csvfile, delimiter='	', quotechar='|')
	# The first row is headers, just read them into a list for lableling later.
	assignment_names = next(paper_scores)[2:]
	for row in paper_scores:
		# Each row represents one student. Create a template context for them.
		total_score = 0
		for points in row[2:]:
			total_score += int(points)

		percent = round(((total_score / available_points) * 100), 2)
		grade = helpers.letter_grade(percent)
		class_count[grade[0]] += 1

		context = {
			"name": row[0] + " " + row[1],
			"sections": [],
			"final_grade": {
				"points": total_score,
				"available_points": available_points,
				"percent": percent,
				"letter": grade,
			},
		}

		for i in range(2, len(assignment_names)+2):
			context["sections"].append({assignment_names[i-2]: int(row[i])})

		print(context["name"] + "   " + context["final_grade"]["letter"])

		# fill in the html with the context
		sourceHtml = template.render(context=context)

		# process the html into a pdf, name it correctly
		file_name = "reports/" + context["name"] + " class grade.pdf"
		pdfkit.from_string(sourceHtml, file_name)

print(class_count)
