from django.http import JsonResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from parsel import Selector

def home(request):

    options = Options()
    options.headless = True
    options.add_argument('--window-size=1920,1080')
    options.add_argument('atart-maximized')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option(
        "prefs", {"profile.managed_default_content_settings.images": 2}
    )
    driver = webdriver.Chrome(options=options, chrome_options=chrome_options)
    driver.get(f"https://www.discogs.com/")            
   
    sel = Selector(text=driver.page_source)
    html = sel.css('body').get()
    soup = BeautifulSoup(html, features="html.parser")
    dict = {}

    for script in soup(["script", "style", ]):
        script.extract()

    for tag in soup.findAll():
        if tag.name != "body":
            try:   
                attr = tag.get('class')
                text = tag.text
                if attr != None and text != "":
                    key = " ".join(tag.get('class'))
                    lines = (line.strip('') for line in text.splitlines())
                    blocks = (phrase.strip() for line in lines for phrase in line.split("  "))
                    text = '\n'.join(block for block in blocks if block).split("\n")   
                    dict[key] = text
            except KeyError:
                pass    
    
    driver.quit()
    
    return JsonResponse({"data": dict })
            
     