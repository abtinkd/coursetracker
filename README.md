# CourseTracker
## Overview
CourseTracker ([live](https://studytimetracker.herokuapp.com/)) allows students to enter their courses, set goals for how much time they want to spend, log their time, and see how they've done over time.

- **Courses** provides an interface for adding classes you're taking now, letting you specify how many
    hours you wish to study each week.
    At the end of the term, simply deactivate the course so you don't have to see it in the Timer anymore -
    don't worry, this won't delete your historical data!
- **Timer** lets you record time spent studying.</li>
- **History** reveals your past performance. The target hours displayed for a course is equal to the goal
    (hours per week) divided by seven, multiplied by how many days the course was active in the date range.

## Dependencies
To run integration testing, the ChromeDriver binary needs to be [downloaded](http://chromedriver.storage.googleapis.com/2.9/chromedriver_win32.zip) and placed in the `Python36/Scripts` folder.
