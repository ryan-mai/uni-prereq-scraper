from bs4 import BeautifulSoup
import requests
import json

# Load program list
with open('program_list.json', 'r') as file:
    data = json.load(file)

valid_links = []
invalid_links = []

print(f"Checking {len(data['programs'])} programs...")
print("-" * 50)

for i, name in enumerate(data["programs"]):
    
    url = f"https://uwaterloo.ca/future-students/programs/{name}"
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.title and "404" not in soup.title.text.lower():
                valid_links.append({"name": name, "url": url})
                # print(f"✓ Valid: {name}")
            else:
                invalid_links.append({"name": name, "url": url, "reason": "No title or 404 page"})
                # print(f"✗ Invalid: {name} (No valid title)")
        else:
            invalid_links.append({"name": name, "url": url, "reason": f"HTTP {response.status_code}"})
            # print(f"✗ Invalid: {name} (HTTP {response.status_code})")
            
    except requests.exceptions.RequestException as e:
        invalid_links.append({"name": name, "url": url, "reason": f"Request failed: {str(e)}"})
        print(f"✗ Invalid: {name} (Request failed)")
    
    # if (i + 1) % 10 == 0:
    #     print(f"Progress: {i + 1}/{len(data['programs'])} checked")

print("\n" + "=" * 60)
print(f"SUMMARY:")
print(f"Total programs checked: {len(data['programs'])}")
print(f"Valid links: {len(valid_links)}")
print(f"Invalid links: {len(invalid_links)}")

if invalid_links:
    print("\n" + "=" * 60)
    print("INVALID LINKS:")
    print("=" * 60)
    for item in invalid_links:
        print(f"Program: {item['name']}")
        print(f"URL: {item['url']}")
        print(f"Reason: {item['reason']}")
        print("-" * 40)
else:
    print("\n🎉 All links are valid!")

with open('valid_programs.json', 'w') as f:
    json.dump(valid_links, f, indent=2)

with open('invalid_programs.json', 'w') as f:
    json.dump(invalid_links, f, indent=2)

print(f"\nResults saved to:")
print(f"- valid_programs.json ({len(valid_links)} programs)")
print(f"- invalid_programs.json ({len(invalid_links)} programs)")