from bs4 import BeautifulSoup
import requests
import json
import logging
from requests.exceptions import RequestException, Timeout, ConnectionError

logging.basicConfig(level=logging.INFO,
                    filename='scrape_req.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

try:
    with open("unsorted_data/valid_programs.json") as file:
        data = json.load(file)
    logging.info("Loaded programs")
except:
    logging.error("File not found!")
    exit(1)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}
logging.info("User-Agent header set")

scraped_requirements = []
total_programs = len(data)
logging.info(f"Starting to process {total_programs} programs")

for i, program in enumerate(data, 1):
    try:
        name = program.get('name', 'Unknown Program')
        url = program.get('url', '')
        
        if not url:
            logging.error(f"No URL found for program: {name}")
            continue

        try:
            response = requests.get(url, headers=headers, timeout=30)
            logging.info(f"HTTP request sent to {url}")
        except:
            logging.error(f"Error")
            continue

        if response.status_code == 200:
            logging.info(f"Successfully accessed website for {name} (Status: {response.status_code})")
            
            try:
                soup = BeautifulSoup(response.content, "html.parser")
                all_h2 = soup.find_all('h2')
            except Exception as e:
                logging.error(f"Cannot parse HTML")
                continue
            
            if all_h2:
                admission_sections_found = 0
                
                for h2 in all_h2:
                    try:
                        if "admission" in h2.text.lower() or "requirements" in h2.text.lower():
                            admission_sections_found += 1
                            logging.info(f"Found admission'")
                            
                            parent_div = h2.find_parent('div')
                            if parent_div:
                                requirements_list = h2.find_next_sibling('ul') or h2.find_next('ul')

                                if requirements_list:
                                    program_entry = {
                                        "program_name": name,
                                        "url": url,
                                        "section_title": h2.text.strip(),
                                        "description": "",
                                        "requirements": []
                                    }
                                    
                                    p_before_ul = requirements_list.find_previous_sibling('p')
                                    if p_before_ul:
                                        program_entry["description"] = p_before_ul.text.strip()
                                        logging.info("Found description of program")
                                    
                                    requirements = []
                                    for li in requirements_list.find_all('li'):
                                        requirement_text = li.text.strip()

                                        if requirement_text:
                                            requirements.append(requirement_text)
                                    
                                    program_entry["requirements"] = requirements
                                    scraped_requirements.append(program_entry)
                                    
                                    logging.info(f"Appended requirement list")
                                else:
                                    logging.warning(f"No requirements list")
                            else:
                                logging.warning(f"No parent div '{h2.text.strip()}'")
                    except Exception as e:
                        logging.error(f"Error with h2 for {name}: {str(e)}")
                        continue
        else:
            logging.error(f"Cannot access url: {response.status_code}")
        
    except Exception as e:
        logging.error(f"Error for {name}: {str(e)}")
        continue

try:
    with open("scraper/scraped_requirements.json", "w", encoding="utf-8") as json_file:
        json.dump(scraped_requirements, json_file, indent=2, ensure_ascii=False)
    logging.info(f"Saved to JSON")
except Exception as e:
    logging.error(f"Failed to save to JSON")

logging.info(f"Finished")