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


It helps if you sort students by last name
Any assignments left blank you should populate with 0s. Consider just doing a find and replace with two tabs.