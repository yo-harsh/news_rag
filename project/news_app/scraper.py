import requests
from bs4 import BeautifulSoup as bs

url = "https://www.moneycontrol.com/news/business/markets/"

def scrape(give_url:str):
    r = requests.get(give_url)
    soup = bs(r.content,'html.parser')
    header = soup.find_all('h2')
    a_tag = []
    for h_tag in header:
        tag = h_tag.find_all('a')
        a_tag.extend(tag)
    return a_tag

def get_link(scraped):
    link_list = []
    for link_tag in scraped:
        links = link_tag['href']
        link_list.append(links)

    print(len(link_list))
    return link_list

def get_content(link_list):
    shorten_link_list = link_list[0:21]

    link_list_content = []
    sum_char = []

    for link in shorten_link_list:
        # Send a GET request to the URL
        r = requests.get(link)
        soup = bs(r.content, 'html.parser')

        # Find and extract all <h1>, <h2>, and <p> tags
        h1_tags = [tag.text.strip() for tag in soup.find_all('h1')]
        h2_tags = [tag.text.strip() for tag in soup.find_all('h2')]
        p_tags = [tag.text.strip() for tag in soup.find_all('p')]
        p_tag = p_tags[0:3]

        # Combine all the tags into a single list for this link
        pre_link_content = ["Headline: "] + h1_tags + ["Description: "] + h2_tags + ["Detail "] +  p_tag
        link_content = ' '.join(pre_link_content)
        sum_char.append(len(link_content))
        # Append the combined content list to link_content_list
        link_list_content.append(link_content)
    print('Done')
    return link_list_content, sum_char


def get_data(url:str):
    scrape_data = scrape(url)
    links = get_link(scrape_data)
    content, sum_c = get_content(links)
    print(sum(sum_c))
    print(len(content))


    # content = ' '.join(pre_content)
    return content

get_data(url)
# print(c[0])
# print(len(c[0]))