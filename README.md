# Course Catalog Parser
### A part of my Senior Project
Using Beautiful Soup to scrape the courses from Bard College course catalogs into JSON files.

The project will have three parts:
* Web-scraping course catalogs ✔️
* Better serving course catalogs (compared to the current site) **¯\\(ツ)/¯**
* Machine learning to predict future potential course catalogs

At the moment, the parser program `app.py` takes around 30 seconds to parse through a semester's worth of courses. Across semesters, the layout of Bard's course catalog is very inconsistent. This has made it necessary to distinguish course catalogs which separate dates and times within tables from those which do not, as well as those course catalogs which use the two-character distributions naming system (which evidently started in Fall 2016) from those which use the four-character system.

This project was partially inspired by [@sabo](https://github.com/sabo).

P.S. Sorry for my ridiculous list comprehensions.

### Related Repositories:
* [Course Catalog Server](https://github.com/segalgouldn/sproj-course-catalog-server)
* [Course Catalog Classifier](https://github.com/segalgouldn/sproj-course-catalog-classifier)
