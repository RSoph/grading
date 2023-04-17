Running notes:

- To download data from Google Drive, make sure you get tab seperated values. Google uses tab seperated values by default, and if you c&p straight from the browser that's what you'll get. You'll also get a ton of blank lines at the end which will process as students with empty pdfs, so look out for that.

- Danielle teaches multiple classes these days. Before you run the command, make sure the correct information is in the template.

- The run command is
`python3 process_paper_grades.py`

- The writer automatically overwrites existing files, so if you need to fix and run again there's no need to delete old pdfs first. The pdf generation takes about three seconds per student, be patient. 

------------

Troubleshooting ideas:
pip3 install pdfkit
brew install homebrew/cask/wkhtmltopdf
^ This one takes FOREVER and I'm not sure it's necessary. try skipping it and see what happens?

Painpoints for next semester:
- The first cell should contain the full name, "Link Brender", as it should be rendered in the report. In the terminal printout, it will show last name first. The blackboard-provided csvs aren't always consistent, so you may need to improvise on-the-fly!
- For paper scores, when Danielle puts in a 0 you should replace it with a 6. Tier 6 is the lowest and it awards 0 points.
- Any assignments left blank you should populate with 0s. Consider just doing a find and replace with two tabs.
- Pay very careful attention to the semester scores csv you get from blackboard. The table headers need cleaning up and you can really fuck things up if you do it wrong.
- There's a print statement in each processscript that prints out the name and grade. Leave that in place because it's useful for entering into blackboard right away.
- Consider generating a new csv with the whole class containing name, letter grade, number grade and uploading that to google. (I mean, this can just be a c&p from the above print statement, it doesn't have to be a whole thing)
