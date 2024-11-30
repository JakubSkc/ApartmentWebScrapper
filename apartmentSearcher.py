import requests
from bs4 import BeautifulSoup

url ="https://www.olx.pl/nieruchomosci/mieszkania/wynajem/krakow/"

response =requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

apt_list = soup.find_all('div', {'data-cy': 'l-card'})

filtered_apartments = []
while True:
    try:
        user_budget = float(input("Enter your budget: "))
        break
    except ValueError:
        print("Please enter a valid budget.")

def get_apartments(url, budget):
    for apt in apt_list:
        #Extracting the URL
        link_tag = apt.find('a', class_="css-qo0cxu")
        if link_tag:
            apt_url = link_tag.get('href')
            full_url = "https://www.olx.pl" + apt_url

        #Extracting the location information
        location_tag = apt.find('p', {"data-testid": "location-date"})
        if location_tag:
            location_text = location_tag.get_text(strip=True).split("-")[0].strip()

        #Extracting the price information
        price_tag = apt.find('p', class_="css-13afqrm")
        if price_tag:
            price_text = price_tag.get_text(strip=True)
            is_negotiable = "do negocjacji" in price_text.lower()
            price_text = price_text.split("do")[0].strip()

        #Extracting the size information
        size_tag = apt.find('span', class_="css-1cd0guq")
        if size_tag:
            size_text = size_tag.get_text(strip=True)
        
        price_text = float(price_text.replace("zł", "").replace(" ", ""))
        if price_text <= budget:
            filtered_apartments.append({"Url" : full_url, "Location" : location_text, "Negotiation" : is_negotiable, "Price" : price_text, "Size" : size_text})

    print(filtered_apartments)
    return filtered_apartments

get_apartments(url, user_budget)