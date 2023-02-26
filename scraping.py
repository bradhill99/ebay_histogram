import requests
from bs4 import BeautifulSoup

url = "https://www.ebay.com/sch/261332/i.html?_from=R40&_nkw=2020+panini+prizm+football+hobby+box+-break&LH_TitleDesc=0&LH_Complete=1&LH_Sold=1&_pgn=1"
       
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299"
}

sold_items = []

# loop through all pages of the eBay query
while True:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    # get all sold items on the current page
    sold_items_page = soup.find_all("div", {"class": "s-item__wrapper"})
    if not sold_items_page:
        break

    # loop through all sold items on the current page
    for listing in sold_items_page:
        # Extract the title
        title = listing.find('div', class_='s-item__title').text.strip()
        # Extract the sold date
        tag_block = listing.find('div', {'class': 's-item__title--tagblock'})
        if tag_block is None:
            print("sold date is null, title={title}")
            continue
        sold_date = tag_block.find(text=lambda x: 'Sold' in str(x))
        # Extract the price
        sold_price = listing.find("span", {"class": "s-item__price"}).text.strip()
        # add the sold item to the list of sold items
        sold_items.append({
            "sold_price": sold_price,
            "sold_date": sold_date,
            "title": title
        })
    # get the URL for the next page of the eBay query
    next_page = soup.find("a", class_="pagination__next icon-link")
    if not next_page:
        break
    next_page_link = next_page["href"]
    url = f"{next_page_link}"
# print all the sold items
for item in sold_items:
    print(f"Sold Price: {item['sold_price']}")
    print(f"Sold Date: {item['sold_date']}")
    print(f"Title: {item['title']}")
    print("------------")
