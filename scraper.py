from bs4 import BeautifulSoup
import requests

subject = "computing-finance"
country = "canada"
province = "ontario"
url = f"https://uwaterloo.ca/undergraduate-admissions/admissions/admission-requirements/{subject}/{country}/{province}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

response = requests.get(url, headers=headers)
# print(f"Response status code: {response.status_code}")
# print(f"Response headers: {dict(response.headers)}")

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    if soup.title:
        print(soup.title.string)
    else:
        print("No title found")

else:
    print("Failed to access the site...")

