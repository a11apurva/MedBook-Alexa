import urllib2
import json

g=open("diseasename.txt","w")

for i in range (1,11):    
    url='http://www.healthos.co/api/v1/diseases?page='+str(i)+'&size=100'
    request = urllib2.Request(url)
    request.add_header('Authorization','Bearer ...')
    request.add_unredirected_header('User-Agent', 'Mozilla/5.0')
    response = urllib2.urlopen(request)

    b = json.load(response)
    print str(len(b))
    print b[0]['disease_name']

    for i in range(len(b)):
        g.write(b[i]['disease_name']+"\n")

g.close()
        
        



