#requests module will allow you to send HTTP/1.1 requests using Python. With it, you can add content like headers, form data, multipart files, and parameters via simple Python libraries. It also allows you to access the response data of Python in the same way
import requests
#json module is used to convert the python dictionary into a JSON string that can be written into a file. It will convert strings to Python datatypes, normally the JSON functions are used to read and write directly from JSON files.
import json
#csv module implements classes to read and write tabular data in CSV format
import csv
import time
import math
#importing strcheckrubbish() from Check_Rubbish file.
from Check_Rubbish import strcheckrubbish

Total_No_pages = 0

http_proxy = "Your Proxy:Port Number"
https_proxy = "Your Proxy:Port Number"
proxies = {'http': http_proxy, 'https': https_proxy}

#User defined function for extracting a portion of string from a given string.
def get_str(resp_str,frm_str,to_str):
    start_index = resp_str.find(frm_str)+ len(frm_str)
    end_index = resp_str.find(to_str, start_index)
    resp_dict = resp_str[start_index:(end_index)]
    return resp_dict

#User defined function for extracting a portion of string from a given string.
def get_json_from_strpage(resp_str,frm_str,to_str):
    start_index = resp_str.find(frm_str) + len(frm_str)
    end_index = resp_str.find(to_str) + len(to_str)
    resp_dict = resp_str[start_index:end_index]
    return resp_dict

#All men Tshirt-Category List Page url
Men_TShirt_url = "https://www.myntra.com/men-tshirts?src=sNav"

Men_TShirt_url_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Host": "www.myntra.com",
    "Referer": "https://www.myntra.com/shop/men",
    "Connection": "keep-alive",
    "Accept-Language": "en-US,en;q=0.9"
}

Men_TShirt_List_page_resp = requests.get(Men_TShirt_url, proxies=proxies, headers=Men_TShirt_url_headers, timeout=20)
# print(Men_TShirt_List_page_resp.status_code,Men_TShirt_List_page_resp.headers)

with open("Men_TShirt_List_page_resp.html", 'w', encoding='utf-8') as file:
   file.write(Men_TShirt_List_page_resp.text)

Men_TShirt_resp_List_page_dict = get_str(Men_TShirt_List_page_resp.text, '"results":', ',"seo":')
# print(Men_TShirt_resp_List_page_dict)

Total_Prod_Count = get_str(Men_TShirt_List_page_resp.text,'{"totalCount":',',"')
##print(Total_Prod_Count)

with open("Men_TShirt_resp_List_page_dict.html", 'w', encoding='utf-8') as file:
    file.write(Men_TShirt_resp_List_page_dict)

with open("Men_TShirt_resp_List_page_dict.html") as f:
    data = json.loads(f.read())
    ##print(type(data))#<class 'dict'>
    ##print(len(data))#11
    ##print(type(data['products']))#<class 'list'>
    ##print(len(data['products']))#List Length (50)

Total_No_pages = math.ceil(int(Total_Prod_Count) / len(data['products']))
# print(Total_No_pages)
# Total_No_pages = 2  # For testing upto 2 listpages

i = 1  # product count for Header
for lp_page in range(1, (Total_No_pages + 1)):
	##Hitting all List Pages 
    Men_TShirt_url = "https://www.myntra.com/men-tshirts?p=" + str(lp_page)
    ##    print(Men_TShirt_url)

    Men_TShirt_url_headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        "Host": "www.myntra.com",
        "Referer": "https://www.myntra.com/shop/men",
        "Connection": "keep-alive",
        "Accept-Language": "en-US,en;q=0.9"
    }

    Men_TShirt_List_page_resp = requests.get(Men_TShirt_url, proxies = proxies, headers = Men_TShirt_url_headers,  timeout = 20)
    # print(Men_TShirt_List_page_resp.status_code,Men_TShirt_List_page_resp.headers)

    with open("Men_TShirt_List_page_resp" + str(lp_page) + ".html", 'w', encoding='utf-8') as file:
        file.write(Men_TShirt_List_page_resp.text)

    Men_TShirt_resp_List_page_dict = get_str(Men_TShirt_List_page_resp.text,'"results":',',"seo":')
    # print(Men_TShirt_resp_List_page_dict)

    with open("Men_TShirt_resp_List_page_dict" + str(lp_page) + ".html", 'w', encoding='utf-8') as file:
        file.write(Men_TShirt_resp_List_page_dict)

    with open("Men_TShirt_resp_List_page_dict" + str(lp_page) + ".html") as f:
        data = json.loads(f.read())
        # print(type(data))#<class 'dict'>
        # print(len(data))#11
        # print(type(data['products']))#<class 'list'>
        # print(len(data['products']))#List Length (50)

    for product in data['products']:
        Product_url = product['landingPageUrl']
        Product_url = 'https://www.myntra.com/' + Product_url
        product['landingPageUrl'] = Product_url
        # print(product['landingPageUrl'])

        Prod_page_url_headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Host": "www.myntra.com",
            "Referer": "https://www.myntra.com/men-tshirts",
            "Connection": "keep-alive",
            "Accept-Language": "en-US,en;q=0.9"
        }

        prod_url = product['landingPageUrl']
        prod_page_resp = requests.get(prod_url,  proxies = proxies, headers = Prod_page_url_headers,  timeout = 20)
        time.sleep(5)
        # print(prod_page_resp.status_code,prod_page_resp.headers)

        with open("Prod_Page_Resp" + str(lp_page) + "-" + str(i) + ".html", 'w', encoding='utf-8') as file1:
            file1.write(prod_page_resp.text)
            file1.close()

        Product_Page_resp_dict = get_json_from_strpage(prod_page_resp.text,'window.__myx =','"Pdp","atsa":[]}')

        with open("Prod_Page_Resp_dict" + str(lp_page) + "-" + str(i) + ".html", 'w', encoding='utf-8') as file2:
            file2.write(Product_Page_resp_dict)
            file2.close()

        with open("Prod_Page_Resp_dict" + str(lp_page) + "-" + str(i) + ".html") as file3:
            # with open("Prod_Page_Resp_dict1.html") as file3:#For testing
            Prod_data = json.loads(file3.read())
            # print(type(Prod_data))#<class 'dict'>
            # print(len(Prod_data))#<class 'dict'>
            # print(Prod_data['pdpData'])#Print all dictionary values
            # print(type(Prod_data['pdpData']))#<class 'list'>
            # print(len(Prod_data['pdpData']))#List Length
            file3.close()
			#Capturing all data from the list pages response.
            disc_per_tag = Prod_data['pdpData']['price'].get('discount')
            # print(disc_per_tag)
            if disc_per_tag != None:
                disc_per = Prod_data['pdpData']['price']['discount']['label']
                # print(disc_per)
            else:
                disc_per = "No Discount"
                # print(disc_per)

            P_id=Prod_data['pdpData'].get('id')
            P_name=Prod_data['pdpData'].get('name')
            P_manufacturer=Prod_data['pdpData'].get('manufacturer')
            P_countryOfOrigin=Prod_data['pdpData'].get('countryOfOrigin')
            P_mrp_price=Prod_data['pdpData']['price'].get('mrp')
            P_disc_price=Prod_data['pdpData']['price'].get('discounted')
            P_disc_percent=disc_per
            P_desc=strcheckrubbish(str([Prod_data['pdpData']['descriptors'][0].get('description')]))
            P_articleType=Prod_data['pdpData']['analytics'].get('articleType')
            P_subcatagory=Prod_data['pdpData']['analytics'].get('subCategory')
            P_brand=Prod_data['pdpData']['analytics'].get('brand')
            P_gender=Prod_data['pdpData']['analytics'].get('gender')
            P_title=Prod_data['pdpData']['offers'][0].get('title')
            P_offer_disc=Prod_data['pdpData']['offers'][0].get('description')
            P_design_type=Prod_data['pdpData']['articleAttributes'].get('Neck')
            P_sleeve_legth=Prod_data['pdpData']['articleAttributes'].get('Sleeve Length')
            P_wash_Care=Prod_data['pdpData']['articleAttributes'].get('Wash Care')
            P_fitting=Prod_data['pdpData']['articleAttributes'].get('Fit')
            P_fabric=Prod_data['pdpData']['articleAttributes'].get('Fabric')

        # Writing all Product's information into csv file.
        with open("Myntra_Prod_Page.csv", "a", newline='') as file:
            # Defines column names into a csv file.
            field_names = ['Prod_Id', 'Prod_Name', 'Prod_Manufacturer_Address', 'Prod_Country', 'Prod_Price', 'Prod_Disc_Price',
                      'Prod_Discount_Percentage', 'Prod_Description', 'Prod_Category', 'Prod_Sub_Category', 'Prod_Brand',
                      'Prod_Gender', 'Prod_Offer_Disc_Title', 'Prod_Offer_Disc', 'Prod_Attribute', 'Prod_Length', 'Prod_Care',
                      'Prod_Size', 'Prod_Fabric']

            writer = csv.DictWriter(file, fieldnames=field_names)
            # Condition for writing header only once.
            if i == 1:
                writer.writeheader()
            i += 1
            # Writing all information in a row.
            writer.writerow(
                {
                    'Prod_Id': P_id,
                    'Prod_Name': P_name,
                    'Prod_Manufacturer_Address': P_manufacturer,
                    'Prod_Country': P_countryOfOrigin,
                    'Prod_Price': P_mrp_price,
                    'Prod_Disc_Price': P_disc_price,
                    'Prod_Discount_Percentage': P_disc_percent,
                    'Prod_Description': P_desc,
                    'Prod_Category': P_articleType,
                    'Prod_Sub_Category': P_subcatagory,
                    'Prod_Brand': P_brand,
                    'Prod_Gender': P_gender,
                    'Prod_Offer_Disc_Title': P_title,
                    'Prod_Offer_Disc': P_offer_disc,
                    'Prod_Attribute': P_design_type,
                    'Prod_Length': P_sleeve_legth,
                    'Prod_Care': P_wash_Care,
                    'Prod_Size': P_fitting,
                    'Prod_Fabric': P_fabric
                }
            )



