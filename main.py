import requests
import csv
from bs4 import BeautifulSoup


# Requests is used to get the full html code of the page.
# Bs4 is a library that makes page search very convinient. It allows moving through tags and has some nice search methods

def job(st):
    title = st.h2.a.span.get("title")
    cname = st.find("span", "companyName").text
    location = st.find("div", "companyLocation").text
    summary = st.find("div", "job-snippet").text.strip()
    date = st.find("span", "date").text
    link = st.h2.a
    joblink = "https://ca.indeed.com" + link.get("href")
    try:
        salary = st.find("div", "attribute_snippet").text.strip()
    except AttributeError:
        salary = "Salary not available"
    return [title, cname, location, date[6:], salary, summary, joblink]


# The 'job' function utilizes bs4 methods and gets all needed information such as Posting title, Company name,
# Location, Short Summary and Posting Date. It also tries to get the salary value, but not all postings have them

# This list stores all information collected
pg = []
jobname = input("Input job name: ")
location = input("Input location: ")
number = int(input("Input number of postings you want to see: "))
# The url to analyze. You can enter any Indeed.com link and it should work fine. The default link is for Python
# postings.
URL = "https://ca.indeed.com/jobs?q="+jobname+"&l="+location

# Get full html page
response = requests.get(URL)

# Reformat html page to BeautifulSoup object, to be able to utilize BeautifulSoup methods
soup = BeautifulSoup(response.text, "html.parser")

# Using find_all method I "shrink" search area to one div object
st1 = soup.find_all("div", "slider_container")

while len(pg)<number:
    for i in st1:
        pg.append(job(i))
        if len(pg) > number:
            break
    # This part "presses" the next button each time the program finishes analyzing one page.
    try:
        url = "https://ca.indeed.com" + soup.find("a", {"aria-label": "Next"}).get("href")
    except AttributeError:
        print("I BROKE")
        break

# Copied this part from stackoverflow
# It creates csv file in the project location
with open("new_file.csv", "w", newline="") as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=',')
    csvWriter.writerow(["Job Title", "Company", "Location", "Posted", "Salary", "Brief description", "Job Link"])
    csvWriter.writerows(pg)
print("File ready")
# Links used
# https://stackoverflow.com/questions/44691524/write-a-2d-array-to-a-csv-file-with-delimiter
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/