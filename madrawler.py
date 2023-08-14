import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor
from alive_progress import alive_bar

class WebsiteScanner:
    def __init__(self, url):
        self.url = url
        self.base_url = urljoin(url, '/')
        self.urls = set()

    def scan_website(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')

        self._get_page_urls(soup)
        self._get_form_endpoints(soup)
        self._get_ajax_urls(soup)

    def _get_page_urls(self, soup):
        for link in soup.find_all('a', href=True):
            href = link['href']
            if not href.startswith('http'):
                href = urljoin(self.base_url, href)
            self.urls.add(href)

    def _get_form_endpoints(self, soup):
        for form in soup.find_all('form', action=True):
            action = form['action']
            if not action.startswith('http'):
                action = urljoin(self.base_url, action)
            self.urls.add(action)

    def _get_ajax_urls(self, soup):
        for script in soup.find_all('script', src=True):
            src = script['src']
            if '.js' in src:
                if not src.startswith('http'):
                    src = urljoin(self.base_url, src)
                self.urls.add(src)

    def save_urls_to_file(self, file_path):
        with open(file_path, 'a') as file:
            with alive_bar(len(self.urls), bar='blocks', spinner='dots_waves2') as bar:
                for url in self.urls:
                    if '=' in url:
                        file.write(url + '\n')
                        print(Fore.RED + url + Style.RESET_ALL)
                    else:
                        file.write(url + '\n')
                        print(url)
                    bar()

        print('Hasil URL telah ditambahkan ke dalam file', file_path)

def scan_single_target(url):
    scanner = WebsiteScanner(url)
    scanner.scan_website()
    scanner.save_urls_to_file('result.txt')

def scan_multiple_targets(file_path):
    with open(file_path, 'r') as file:
        target_urls = file.readlines()

    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in target_urls:
            url = url.strip()
            executor.submit(scan_single_target, url)

def main():
    print("""
_  _ ____ ___  ____ ____ _ _ _ _    ____ ____ 
|\/| |__| |  \ |__/ |__| | | | |    |___ |__/ 
|  | |  | |__/ |  \ |  | |_|_| |___ |___ |  \ 
                                              
[ www.github.com/MadExploits ]
""")
    print('Choose scan mode :\n')

    print('1. Single Target')
    print('2. Mass Target')

    mode = input('\nChoose beetween (1/2): ')

    if mode == '1':
        target_url = input('Input URL : ')
        scan_single_target(target_url)
    elif mode == '2':
        file_path = input('Input URL file: ')
        scan_multiple_targets(file_path)
    else:
        print('Error kontol!')

if __name__ == '__main__':
    main()
