# import libraries
import urllib3
from bs4 import BeautifulSoup
import requests
import re
import numpy


def parse_url(url):
    http = urllib3.PoolManager()
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup

def find_product(dict, num_results):

    soup = parse_url(dict["url"])

    product_list = soup.find(class_=dict['product_list_class'])
    product_list_items = product_list.find_all(dict['product_list_item_tag'], dict['product_list_item_class'])

    price_discount = []
    price_standards = []
    price_sales = []


    for product in product_list_items:
        price_standard = product.find(dict["price_standard_tag"], dict['price_standard_class']).findAll(text=True)[dict["price_standard_index"]]
        price_standard = re.findall(r'-?\d+\.?\d*', price_standard)
        price_standard = list(map(float, price_standard))
    
        price_sale = product.find(dict["price_sale_tag"], dict["price_sale_class"]).findAll(text=True)[dict["price_sale_index"]]
        price_sale = re.findall(r'-?\d+\.?\d*', price_sale)
        price_sale = list(map(float, price_sale))
        price_sale.sort(reverse=True)
        
        price_standards.append(price_standard)
        price_sales.append(price_sale)
        
        price_discount.append((price_standard[0] - price_sale[0]) / price_standard[0])
    

    index = sorted(range(len(price_discount)), key=lambda k: price_discount[k])[::-1]
    price_discount.sort(reverse=True)

    html = style()
    sep = "<br />"
    for i in index[:num_results]:
        content = product_list_items[i]
        img = content.findAll('img')[dict["img_index"]]
        img = str(img).replace("class=", "style=\"width:300px;\" class=")
        print(img)
        link = content.findAll('a')[0]["href"]
        print(link)
        
        #replace url
        link = dict["main_url"] + link
    
        origin_price = price_standards[i][0]
        sale_price = price_sales[i][0]
        discount = (origin_price - sale_price) / origin_price
        prices = "<div class=\"\" style=\"position: relative;margin: auto;width:300px;\"><div class=\"span3\">Original price: $" +  str(price_standards[i][0]) +" </div>" + "<div class=\"span3\"> Sale price: $" + str(price_sales[i][0]) + "</div><div class=\"span3\">Discount: " + str("{0:.0%}".format(discount)) + "</div></div>"
        html += "<div class=\"span3\" style=\"text-align:center;\"><a display: block; width=\"81\" height=\"75\" href=" + link + ">" + img + "</a>" + prices + sep + "</div>"

    return html
       

def start(website):

    return find_product(website, 5)

def style():
    return "<link href=\"static/styles/bootstrap.min.css'\" rel=\"stylesheet\"><link href=\"/static/styles/flat-ui.css\" rel=\"stylesheet\">"
