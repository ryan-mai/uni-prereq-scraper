# University of Waterloo Requirement Scraper

# Overview
Website - *https://uni-prereq-scraper.onrender.com/* 💻
Kaggle - *https://www.kaggle.com/datasets/imryanm/university-of-waterloo-admission-requirements-list/data* 📅


**Purpose** 
To enable incoming Grade 12. an easier resource to access the pre-requisites for their desired program at University of Waterloo. The last thing I or any future applicants wants is finding out that they do not fufill. 😱

It is especially true when you have to browse through various links, which clumps up your web browser and making it messy (then it already it is, I am talking about myself don't worry).And to make matters worse you have to consider alternative universities if you don't get accepted. With this website, you do not have to worry. 😅

As a result having all the neccessary requirements in one place allows you to spend more time on actually applying and writing your scholarship letters! ⌚

PS. I initially intended on scraping Wimbeldon for the latest Tennis matches and constantly update it on my website, but I was blocked. So I decided on a more meaningful crawler 🎾

## Future Improvements
- Provide a scraper for every Canadian university or for this specific university the ability to scrape the program requirements for different people. For example, if they are in a different province, country, have taken speciality programs, and/or the Waterloo competitions. 🏫
- The ability to identify the accuracy of the grades by comparing it with the common grade requirement since most of the site says for example 80% when in reality it is 95%+ 🔬
- A dynamic website to enable users a better sense of the top programs and what to search for. 🔍
- An AI assistant that will help them in choosing the best program given their grades, current enroll subjects, and any other achievements. 🏆

If you want **your** universities programs hosted, feel free to contact me at ryanmai757@gmail.com 📧

# Technical

1. **Web Crawler**
	- I used BeautifulSoup to parse the HTML. The code accesses every program link (which I also scraped from https://uwaterloo.ca/future-students/programs and can be found in `scrape_programs.py` and I ensured the validity of each site with `valid_site.py`) 🐍
    - A more robust approach would be to use Scrapy or Selenium for dynamiic heavy websites. 💪
2. **Error handling** and **Logging**
	- I used `logging` library to log every action from initiating the scraper to appending each item from the `li` tags (the requirements) ✅
	- I also handled error handling by adding exceptions which would raise `logging.error` for fatal errors or `logging.warning` for minor issues like no requirements which would be rare! ❌
	- Logs are handled in `scrape_req.log`

**Setup Instructions**
1. Clone the GitHub repo - `git clone https://github.com/ryan-mai/uni-prereq-scraper.git` 🔃
2. Install the dependencies `pip install -r requirements.txt` 👨‍🏫
3. Run `python scrape_req.py` and then find the list of programs in `scraped_requirements.json` 🏃‍♂️🏃‍♀️
4. Start the web application `python app.py` and open `http://localhost:5000` in your browser 🎉

**Data Structure**
Below is an example of what the JSON file output is like 📁
```json
{
  "program_name": "Computer-Science",

  "url": "https://uwaterloo.ca/future-students/programs/Computer-Science",

  "section_title": "Admission requirements",

  "description": "Ontario students: six Grade 12 U and/or M courses including",

  "requirements": [
    "Advanced Functions",
    "Calculus and Vectors",
    "Any Grade 12 U English",
    "One other 4U course"
  ]
}
```