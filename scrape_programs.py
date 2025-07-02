from bs4 import BeautifulSoup
import requests
import re
import json

url = "https://uwaterloo.ca/future-students/programs#all"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    print(soup.title.string)
    p_tags = soup.find_all('p')
    
    programs_list = []
    
    for p in p_tags:
        text = p.get_text().strip()
        if text and not text.isupper() and len(text) > 1:  # Skip single letters and empty text
            import re
            programs = re.findall(r'[A-Z][^A-Z]*(?:\s+[a-z][^A-Z]*)*', text)
            
            for program in programs:
                program = program.strip()
                if len(program) > 2 and not program.isupper():
                    programs_list.append(program)
    
    unique_programs = []
    seen = set()
    for program in programs_list:
        if program not in seen:
            unique_programs.append(program)
            seen.add(program)
    
    print(f"\nFound {len(unique_programs)} unique programs:")
    print("=" * 60)
    for i, program in enumerate(unique_programs, 1):
        print(f"{i}. {program}")
    
    # Save to JSON file
    with open('programs.json', 'w', encoding='utf-8') as f:
        json.dump(unique_programs, f, indent=2, ensure_ascii=False)
    
    print(f"\nPrograms saved to programs.json")
    
    # Also save as a structured JSON with more details
    programs_data = {
        "total_programs": len(unique_programs),
        "scraped_from": url,
        "programs": unique_programs
    }
    
    with open('programs_detailed.json', 'w', encoding='utf-8') as f:
        json.dump(programs_data, f, indent=2, ensure_ascii=False)
    
    print(f"Detailed data saved to programs_detailed.json")
else:
    print("Failed to access the site...")