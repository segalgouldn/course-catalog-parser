# Course Catalog Parser
Using Beautiful Soup to scrape the courses from Bard College course catalogs into JSON files.

At the moment, the parser program `app.py` takes around 30 seconds to parse through a semester's worth of courses. Across semesters, the layout of Bard's course catalog is very inconsistent. This has made it necessary to distinguish course catalogs which separate dates and times within tables from those which do not, as well as those course catalogs which use the two-character distributions naming system (which evidently started in Fall 2016) from those which use the four-character system.

This project was partially inspired by [@sabo](https://github.com/sabo)'s [Bard People's Insurrectionary Course Catalog](https://projects.eh.bard.edu/bpicc/).

P.S. Sorry for my ridiculous list comprehensions.

### TODO
* There's currently an issue with inconsistencies in the layout of tables within **individual** course list pages.
  * For example, see the [mathematics department course list for Spring 2018](http://inside.bard.edu/academic/courses/spring2018/mathematics.html).
  * Because the parser is not designed to automatically distinguish between course list pages which do and do not feature both the new and old distributions naming systems, pages such as this one can not be parsed.
  * To fix this, it should be possible to programmatically count the number of columns in each table for each course in each course list page, thus informing the parser on which courses use both or neither of the distributions naming systems.

### Related Repositories:
* [Course Catalog Server](https://github.com/segalgouldn/course-catalog-server)
* [Course Catalog Classifier](https://github.com/segalgouldn/course-catalog-classifier)

This was intended as a [Bard College Senior Project](https://github.com/segalgouldn/Senior-Project-Subtweets/blob/master/drafts/senior_project_guidelines.pdf), but I decided to make [this](https://github.com/segalgouldn/Senior-Project-Subtweets) instead.
