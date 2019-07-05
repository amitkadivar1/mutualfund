from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import requests
import json
headers = {
    "X-RapidAPI-Host": "dmoin-mutual-fund-nav-bse-india-v1.p.rapidapi.com",
    "X-RapidAPI-Key": "c7c2dfe082msh466ae3982981b5dp195f31jsne3bdbc4aeb94"
}

def inputform(request):
    return render(request,'index.html',{})

def getmutualfund(request):
    try:
        income = request.POST['amount']
        year = request.POST['year'] 
        print(income,year)
        allmutalfund = requests.get('https://dmoin-mutual-fund-nav-bse-india-v1.p.rapidapi.com/GetAllFundsData', headers=headers)
    # print(allmutalfund)yearyear
        if allmutalfund.status_code == 200:
            dictname = []
            data = allmutalfund.json()
            for i in data:
                nav = i['NetAssetValue']
                if(nav != 'N.A.'):
                    returnfund = int(year)*int(income)*float(nav)
                    print(returnfund)
                else:
                    returnfund = 0
                dictname.append({'Code': i['SchemeCode'], 'Name': i['SchemeName'],'Nav': nav, 'ReturnFund': str(returnfund), 'Date': i['NAVDate']})
            return render(request,'detail.html',context={'dictname':dictname})
            # return HttpResponse(json.dumps(dictname))
        else:
            return HttpResponse('Oops!!! Status Code', allmutalfund.status_code)
    except Exception as e:
        return HttpResponse("Exception ",e, allmutalfund.status_code)
    

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
