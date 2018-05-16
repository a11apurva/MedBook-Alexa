g=open("medicineName.txt","w")



import requests
import pprint

url = "http://healthos.co/api/v1/medicines/brands"

headers = {'Authorization': 'Bearer ...'}

for i in range(1,11):
    querystring = {"page":str(i),"size":"25"}

    response = requests.request("GET", url, headers=headers, params=querystring)

    #print response.json()
    print str(len(response.json()))
    print str(response.json()[0]['name'])

    for i in range(len(response.json())):
        g.write(response.json()[i]['name']+"\n")

g.close()
        
