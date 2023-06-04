import time
from selenium import webdriver
link_head="https://www.kayak.com/flights/"
from2des="BOS,NYC-TYO"
date="/2023-07-03"
link_end="?sort=bestflight_a"
page_addr=link_head+from2des+date+link_end
driver=webdriver.Chrome()
driver.get(page_addr)