a=0
import requests
import json
import datetime 
start_time=(datetime.datetime.now() )

for i in range(1000):
    
    url="http://127.0.0.1:8000/jobs/all"
    response=requests.get(url)
    data=response.json()
    # print(data)
    # print(i)
    a+=1
    # print(a)
print(start_time)
end_time=(datetime.datetime.now() )
print(end_time)
c = end_time-start_time
print('Difference: ', c)
minutes = c.total_seconds() / 60
print('Total difference in minutes: ', minutes)