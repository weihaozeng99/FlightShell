from bs4 import BeautifulSoup
from urllib import request

link_head="https://www.kayak.com/flights/"
from2des="BOS,NYC-TYO"
date="/2023-07-03"
link_end="?sort=bestflight_a"


page_addr=link_head+from2des+date+link_end
def check_price(page_addr):
    page=request.urlopen(page_addr)
    soup=BeautifulSoup(page,'html.parser')
    test=soup.find_all(class_="nrc6")
    print(test)

# def has_result():
check_price(page_addr)
