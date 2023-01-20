import requests
import json
import os


try: 
    os.mkdir('./AZURE_DATA') 
except:
    pass

services=["Azure Kubernetes Service","Virtual Network", "Storage", "Load Balancer", "Virtual Machines"]

url = "https://prices.azure.com/api/retail/prices"


def save_data(json_data,service_name):
    filename = "./AZURE_DATA/{}.json".format(service_name)

    if os.path.exists(filename):
        
        with open(filename, 'r+') as json_file:
            
            # file exists
            # load the existing data
            json_file_data = json.load(json_file)

            # join new data with existing
            print('adding new data')
            for data in json_data["Items"]:
                json_file_data["Items"].append(data)

            json_file_data["NextPageLink"] = json_data["NextPageLink"]


            # set file position to offset
            json_file.seek(0)

            # convert back to json
            json.dump(json_file_data, json_file, indent=4)

    else:
        
        data_to_save = {"Items": [], "NextPageLink": ""}
        data_to_save["Items"] = json_data["Items"]
        data_to_save["NextPageLink"] = json_data["NextPageLink"]
        
        with open(filename, 'a') as json_file:
            print('creating file and adding new data')
            json.dump(data_to_save, json_file, indent=4)


def get_data(url,service,NextPageLink=''):

    if NextPageLink == '':
        service_url = url + "?$filter=serviceName eq '{}'".format(service)
    else:
        service_url = NextPageLink
    # print("serviceurl: \n",service_url)
    json_data = requests.get(service_url).json()
    NextPageLink = json_data["NextPageLink"]
    save_data(json_data,service)

    if NextPageLink != None:
        print(NextPageLink)
        get_data(url,service,NextPageLink)


for service in services:
    get_data(url,service)

# n= 'https://prices.azure.com:443/api/retail/prices?$filter=serviceName%20eq%20%27Virtual%20Machines%27&$skip=166800'
# s="Virtual Machines"
#incase the download stops and tries missed
# get_data(url, s,n)