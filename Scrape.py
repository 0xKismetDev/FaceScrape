from bs4 import BeautifulSoup # bs4 for image scraping
import requests # requests for initial request
import argparse # for arguments

# argument parser
parser = argparse.ArgumentParser(
    description='Scrape images from site.',
    epilog='Example: python scrape.py -u https://www.google.com -p "pics/"'
)
parser.add_argument('-u', '--url', help='Target url', required=True)
parser.add_argument('-p', '--path', help='Path where images will be saved', required=True)
args = parser.parse_args()

# loop through all images in url (multiple requests incase of different images on page reload, may cause WAF to trigger, turn off if needed)
def scrape():
    #while True:
        try:
            URL = args.url
            getURL = requests.get(URL, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"})
            soup = BeautifulSoup(getURL.text, 'html.parser')
            images = soup.find_all('img')
            resolvedURLs = []
            for image in images:
                src = image.get('src')
                resolvedURLs.append(requests.compat.urljoin(URL, src))
            for image in resolvedURLs:
                webs = requests.get(image)
                try:
                    open(args.path + image.split('/')[-1], 'wb').write(webs.content)
                except FileNotFoundError:
                    print("Invalid path.")
                    exit()
        except KeyboardInterrupt:
            print("Exiting...")
            exit()

if __name__ == "__main__":
    scrape()