Running notes:

To download data from Google Drive, make sure you get tab seperated values. Google uses tab seperated values by default, and if you c&p straight from the browser that's what you'll get. You'll also get a ton of blank lines at the end which will process as students with empty pdfs, so look out for that.

The run command is
`python3 process_paper_grades.py`

Don't forget the 3!

The writer automatically overwrites existing files, so if you need to fix and run again there's no need to delete old pdfs first. The pdf generation takes about three seconds per student, be patient. 

Troubleshooting ideas:
pip3 install pdfkit
brew install homebrew/cask/wkhtmltopdf
^ This one takes FOREVER and I'm not sure it's necessary. try skipping it and see what happens?

Painpoints for next semester:
- It helps if you sort students by last name. Either way, choose first name or last name and stick with it for all assignments.
- For paper scores, when Danielle puts in a 0 you should replace it with a 6. Tier 6 is the lowest and it awards 0 points.
- Any assignments left blank you should populate with 0s. Consider just doing a find and replace with two tabs.
- Pay very careful attention to the semester scores csv you get from blackboard. The table headers need cleaning up and you can really fuck things up if you do it wrong.
- There's a print statement in the process_semester script that prints out the name and grade. Leave that in place because it's useful for entering into blackboard right away.
- Add a print statement for the number grade as well as the letter - that's what you really want to enter to blackboard.
- Consider generating a new csv with the whole class containing name, letter grade, number grade and uploading that to google.