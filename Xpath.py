import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.by import By
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
#info: [0"carrier",1"price",2"duration",3"stops",4"date",5"from_to"]
def send_mail(info):
    print("sending email")
    content=""
    
    for info_single in info:
        content=content+"<p><strong>Date: </strong>"+info_single[4]+"</p>"+"<p><strong>From and To: </strong>"+info_single[5]+"</p><p><strong>Carrier Name: </strong>"+info_single[0]+"</p><p><strong>Price: </strong>"+info_single[1]+"</p><p><strong>Duration: </strong>"+info_single[2]+"</p><p><strong>Stops: </strong>"+info_single[3]+"</p>"
    message = Mail(
    from_email='zengmei888@gmail.com',
    to_emails='zengweihao99@gmail.com',
    subject="Ticket Info Update",
    #html_content='<strong>and easy to do anywhere, even with Python</strong>')
    html_content=str(content))
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def scrap(date_desire,from_to,max_price):
    date="2023-07-03"
    link_head="https://www.kayak.com/flights/"
    #from2des="BOS,NYC-TYO"
    from2des=from_to
    date=date_desire
    link_end="?sort=bestflight_a"

    page_addr=link_head+from2des+"/"+date+link_end
    driver=webdriver.Chrome()
    driver.get(page_addr)
    time.sleep(randint(2,5))

    flights_xpath='//div[@class="nrc6"]'
    flights=driver.find_elements(By.XPATH, flights_xpath)
    #print(flights[0])
    #test_id=flights[0].get_attribute("")
    # print(test)
    for i in range(0,5):
        try:
            more_button_path='//div[contains(@class,"show-more-button")]'
            driver.find_element(By.XPATH,more_button_path).click()
            time.sleep(randint(10,15))
        except:
            pass   
    carrier_name_path='//div[@class="c_cgF c_cgF-mod-variant-default" and @dir="auto"]'
    duration_path='//div[@class="xdW8"]/div[@class="vmXl vmXl-mod-variant-default"]'
    stops_path='//span[contains(@class,"stops-text")]'
    price_path='//div[@class="f8F1-price-text"]'
    carriers=driver.find_elements(By.XPATH,carrier_name_path)
    durations=driver.find_elements(By.XPATH,duration_path)
    stops=driver.find_elements(By.XPATH,stops_path)
    prices=driver.find_elements(By.XPATH,price_path)
    print(len(carriers))
    print(len(stops))
    print(len(prices))
    # if len(carriers)!=len(stops) or len(stops)!=len(prices):

    #     return
    price_number=[]
    stop_number=[]
    for i in range(0,len(stops)):
        price_temp=prices[i].text
        price_temp=price_temp.replace('$',"")
        price_number.append(int(price_temp.replace(',',"")))
        stop_temp=stops[i].text
        if stop_temp=="nonstop":
            stop_temp=0
        else:
            stop_temp=int(stop_temp[0])
        stop_number.append(stop_temp)
    # print(price_number)

    sorted_price_id = sorted(range(len(price_number)), key=lambda k: price_number[k], reverse=False)
    sorted_stop_id = sorted(range(len(stop_number)), key=lambda k: stop_number[k], reverse=False)
    # for i in range(0,len(stops)):
    #     print(stops[i].text)
    # test_path=test_path+test_id
    # test_path=test_path+'/div[@class="c_cgF c_cgF-mod-variant-default"]'
    info_to_send=[]
    for i in range(0,len(sorted_price_id)):
        if price_number[sorted_price_id[i]]<=max_price:
            temp=[carriers[sorted_price_id[i]].text,str(price_number[sorted_price_id[i]]),durations[sorted_price_id[i]].text,str(stop_number[sorted_price_id[i]]),date,from_to]
            info_to_send.append(temp)
    if len(info_to_send)>0:
        send_mail(info_to_send)
date_year_month="2023-06-"
date_day=14
#scrap(date_year_month+str(date_day),1500)
route1="BOS,NYC-TYO"
route2="BOS,NYC-HKG"
#scrap(date_year_month+str(date_day),route2,1500)
while(1):
    try:
        for i in range(0,15):
            scrap(date_year_month+str(date_day+i),route1,1000)
            scrap(date_year_month+str(date_day+i),route2,1000)
    except:
        continue
#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