"""
main.py: třetí projekt do Engeto Online Python Akademie

author: Eva Nedvědová
email: 
"""
import sys
import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, parse_qs

def parse_args():
  if len(sys.argv) != 3:
      print("Error: 2 arguments needed (URL and file name)")
      sys.exit()
  
  url = sys.argv[1]
  output = sys.argv[2]
  
  #validace vstupu - to do
  return url, output


def webpage_load(url):
  """loads the webpage and parses content"""
  response = requests.get(url)

  #if status code is ok, proceeds
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    print("Webpage loaded succesfully")
    print(soup)
    print("end of soup")
    return soup
  else:
    print("webpage was not loaded")
    return None

def csv_prep(output: str) -> csv:
  """Takes output file name from user and creates new file with the same name."""
  new_csv = open(output, mode = "w", newline="", encoding="utf-8")
  print(f"creating csv file with name {output}")

# pro kazde url okrsku scrapuj numera si zapis do promenych
def precinct_code_scraper(soup):
  """takes parsed url for specific presinct name and scrapes data into variables"""
  # finds reference
  a_tag = soup.find("a", href=lambda x: x and "xobec=" in x)
 
  if a_tag is None:
    print("Nenalezen žádný <a> tag")
    return  
  # takes atribute href
  href = a_tag["href"]

  #finds precinct number from href
  parsed = urlparse(href)
  
  params = parse_qs(parsed.query)
  
  precinct_number = params.get("xobec", [None])[0]
  print(f"Analyzing precinct number: {precinct_number}")
  
  return precinct_number

def precinct_name_scraper(soup):
  #find precinct name
  name_tag = soup.find("h3", string=lambda t: t and "Obec:" in t)
  if name_tag:
    text = name_tag.get_text(strip=True)
    precinct_name = text.split(":")[1].strip()
    print(f"Analyzing precinct name: {precinct_name}")
  else:
    print("name tag not found")
  
  return precinct_name

def presinct_numbers_scraper(soup):
  reg_voters = soup.select_one("td.cislo[headers='sa2']")
  clean_reg_voters = reg_voters.get_text(strip=True)
  print(f"registered voters {clean_reg_voters}")

  issued_env = soup.select_one("td.cislo[headers='sa3']")
  clean_issued_env = issued_env.get_text(strip=True)
  print(f"Issued envelopes {clean_issued_env}")
  
  valid_votes = soup.select_one("td.cislo[headers='sa6']")
  clean_valid_votes = valid_votes.get_text(strip=True)
  print(f"Issued envelopes {clean_valid_votes}")
  
  # fist table votes list
  cells1 = soup.select("td.cislo[headers='t1sa2 t1sb3']")
  
  # second table votes list
  cells2 = soup.select("td.cislo[headers='t2sa2 t1sb3']")
  
  print(f"votes 1 are {cells1}, total list is {cells2}")
  
  return reg_voters, issued_env, valid_votes, cells1, cells2

def main():
  url, output = parse_args()
  csv_prep(output)
  soup = webpage_load(url)
  precinct_code_scraper(soup)
  precinct_name_scraper(soup)
  presinct_numbers_scraper(soup)

  # 1 jit na url uzemniho celku
  # pripadne overit ze to je url celku - viz validace
  # vyhledej seznam url okrsku
  # v pripade ze okrsek je rozdelen na vic okrsku, tak podokrsky pridej do seznamu
  # pro kazde url okrsku scrapuj numera si zapis do promenych
  # promene uloz jako dalsi radek do csv
  # pokracuj dalsim okrskem v seznamu
  
  


if __name__ == "__main__":
  main()
