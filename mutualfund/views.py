from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests

import json
headers = {
    "X-RapidAPI-Host": "dmoin-mutual-fund-nav-bse-india-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "c7c2dfe082msh466ae3982981b5dp195f31jsne3bdbc4aeb94"
}
api_key = "x19ec-fDEy26ozp7xHFz"


def inputform(request):
    datadict=[]
    data = requests.get('http://portal.amfiindia.com/spages/NAVAll.txt')
    if (data.status_code) == 200:
        mutualfund = data.content
        mutualfund = str(mutualfund).split('\\r\\n')
        for i in mutualfund:
            name=i.split(';')
            if(len(name)>5):
                name=i.split(';')[-3]
                code=i.split(';')[0]
                datadict.append({'code':code,'name':name})                
                
    return render(request,'index.html',context={'datadict':datadict})

def getmutualfund(request):
    try:
        income = request.POST['amount']
        year = request.POST['year'] 
        plan=request.POST['plan']  
        try:
            dictname = []
            previousYear = datetime.now() - relativedelta(years=int(year))
            previousYear=str(previousYear).split()[0]
            print(previousYear)
            api=requests.get("https://www.quandl.com/api/v3/datasets/AMFI/{}.json?api_key={}".format(plan,api_key))
            if api.status_code==200:
                api=api.json()
                dataset=api['dataset']
                apidata=dataset['data']
                # print(apidata,'------------------------------')
                nav=int(apidata[0][1])
                
                for i in apidata:
                    if(i[0]==previousYear):
                        initalnav=int(i[1])
                        ar=(nav-initalnav)/initalnav*100
                        valueamount=int(income)+((int(income)*float(ar))/100)
                        print(valueamount,ar)
                        dictname.append({'Code': dataset['dataset_code'], 'Name': dataset['name'],'Nav': nav, 'ReturnFund': str(round(ar,2)),'ReturnFundValue':str(round(valueamount,2)),'InitialData':str(previousYear), 'Date': str(dataset['end_date']),'amount':income,})
                        break    
                return render(request,'detail.html',context={'dictname':dictname,'nav':nav})
            else:
                return HttpResponse('Oops!!! Status Code', api.status_code)
        except Exception as e:
            print(e)
            return HttpResponse("Exception ",e)
    # print(allmutalfund)yearyear
      
            # return HttpResponse(json.dumps(dictname))
    except Exception as e:
        return HttpResponse("Exception ",e, api.status_code)
    

# using this you can get only one value this api is optional
def mutualfunddetail(request, schemacode):
    url = 'https://www.quandl.com/api/v3/datasets/AMFI/{}.json?api_key=x19ec-fDEy26ozp7xHFz'.format(
        schemacode)
    mutualfund = requests.get(url)
    data = mutualfund.json()
    # print(a['dataset'])
    if mutualfund.status_code == 200:
        return HttpResponse(json.dumps(data['dataset']))
    else:
        return HttpResponse(None)
