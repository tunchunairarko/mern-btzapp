import requests
import dpath  # https://github.com/akesterson/dpath-python
from pprint import pprint  # Needed for printing responses, can be deleted.
import re
import AzProductInformation
import arrow
import productDataApi
import json
import time
import sys

class SellerChamp(object):
    def __init__(self,query):
        for i in range(len(query)):
            if(query[0]==' '):
                query=query[1:]
            else:
                break
        for i in range(len(query)-1,0,-1):
            if(query[len(query)-1]==' '):
                query=query[:-1]
            else:
                break
        self.product_list=[]
        self.query = query
        self.product = self.get_query_details()
        
    def getQueryType(self):
        ql=len(self.query)
        if(self.query.isdigit()==True):
            if(ql>=11 and ql<13):
                return 'upc'
            else:
                return 'mpn'
        else:
            if(ql==10):
                if (any(char.isdigit() for char in self.query)==True):
                    regex=r'([A-Z0-9]{10})'
                    match=re.match(regex,self.query)
                    if(match):
                        return 'asin'
                else:
                    return 'keyword'
            elif(ql==7):
                regex=r'sky[0-9]{4,6}$'
                match=re.match(regex,self.query,flags=re.IGNORECASE)
                if(match):
                    return 'sky'
            else:
                return 'keyword' 
    def get_query_details(self):
        url='https://sellerchamp.com/api/manifests'
        data={}
        tp=self.getQueryType()
        if(tp=='asin'):
            data={
                'manifest':{
                    'name':arrow.now().format('MM-DD-YYYY'),
                    'ship_from_address_id':'5dd6b93eb5e2475184002578',
                    'marketplace_account_id':'5e445a84b5e24703870046df',
                    'product_listings_attributes':[
                        {'asin':self.query}
                    ]
                }
            }
        elif(tp=='mpn'):
            p=productDataApi.ProductDataUPC(self.query)
            upc=p.get_upc_from_mpn()
            data={
                'manifest':{
                    'name':arrow.now().format('MM-DD-YYYY'),
                    'ship_from_address_id':'5dd6b93eb5e2475184002578',
                    'marketplace_account_id':'5e445a84b5e24703870046df',
                    'product_listings_attributes':[
                        {'asin':'','upc':upc}
                    ]
                }
            }
        elif(tp=='sky'):
            p=productDataApi.ProductDataUPC(self.query)
            upc=p.get_upc_from_mpn()
            # print('Sky number converted to UPC: '+upc)
            data={
                'manifest':{
                    'name':arrow.now().format('MM-DD-YYYY'),
                    'ship_from_address_id':'5dd6b93eb5e2475184002578',
                    'marketplace_account_id':'5e445a84b5e24703870046df',
                    'product_listings_attributes':[
                        {'asin':'','upc':upc}
                    ]
                }
            }
        elif(tp=='upc'):
            data={
                'manifest':{
                    'name':arrow.now().format('MM-DD-YYYY'),
                    'ship_from_address_id':'5dd6b93eb5e2475184002578',
                    'marketplace_account_id':'5e445a84b5e24703870046df',
                    'product_listings_attributes':[
                        {'asin':'','upc':self.query}
                    ]
                }
            }
        elif(tp=='keyword'):
            p=productDataApi.ProductDataAPIWithKeyword(self.query)
            upc=p.get_query_details()
            data={
                'manifest':{
                    'name':arrow.now().format('MM-DD-YYYY'),
                    'ship_from_address_id':'5dd6b93eb5e2475184002578',
                    'marketplace_account_id':'5e445a84b5e24703870046df',
                    'product_listings_attributes':[
                        {'asin':'','upc':upc}
                    ]
                }
            }
        headers={
            'token':'7690a200d8a675b404a100dc9cc93873',
            'Content-Type': 'application/json',
            'cache-control': 'no-cache,no-cache,no-cache'
        }
        data=json.dumps(data)
        
        r=requests.post(url,headers=headers,data=data)
        data=r.content
        # print(data)
        data=json.loads(data)
        manifest_folder_id=data['manifest']['manifest_folder_id']
        manifest_id=data['manifest']['id']
        url='https://sellerchamp.com/api/manifests?marketplace_account_id=5e445a84b5e24703870046df&manifest_folder_id='+manifest_folder_id+'&page=1&page_size=25'
        headers={
            'token':'7690a200d8a675b404a100dc9cc93873'
        }
        r=requests.get(url,headers=headers)
        data=r.content
        data=json.loads(data)
        for i in range(10):            
            if(data['manifests'][0]['processing']==False):
                break
            else:
                time.sleep(1)
                # print('Waiting from seller champ API to respond to our search request. Please wait.'+'.'*i)
                url='https://sellerchamp.com/api/manifests?marketplace_account_id=5e445a84b5e24703870046df&manifest_folder_id='+manifest_folder_id+'&page=1&page_size=25'
                headers={
                    'token':'7690a200d8a675b404a100dc9cc93873'
                }
                r=requests.get(url,headers=headers)
                data=r.content
                # # print(data)
                data=json.loads(data)
        url='https://sellerchamp.com/api/manifests/'+manifest_id+'/product_listings?page=1&page_size=25'
        headers={
            'token':'7690a200d8a675b404a100dc9cc93873'
        }
        r=requests.get(url,headers=headers)
        product_ids=[]
        data=r.content
        data=json.loads(data)
        pl=data['product_listings']
        for i in range(len(pl)):
            product_ids.append(pl[i]['product_id'])
        
        for i in range(len(product_ids)):
            try:
                url='https://sellerchamp.com/api/products/'+product_ids[i]+'.json'
                headers={
                    'token':'7690a200d8a675b404a100dc9cc93873'
                }
                r=requests.get(url,headers=headers)
                data=r.content
                data=json.loads(data)
                data=data['product']
                item = {
                    'asinid': data['upc'],
                    'title': data['title'],
                    'rank': '',
                    'package_quantity': '1',
                    'retailer': data['brand'],
                    'image': '',
                    'description':data['description'],
                    'features':data['features'],
                    'price': data['retail_price'],
                    'url': '',
                    'height': data['item_dimensions']['height'],
                    'width':data['item_dimensions']['width'],
                    'length':data['item_dimensions']['length'],
                    'weight':data['weight_in_pounds'],
                    'model_no':data['mpn'],
                    'source':'Seller Champ',
                    'product_url':''  
                }
                if(tp=='sky'):
                    w=self.query
                    w=w.lower()
                    w=w.replace('sky','LQP')
                    item['title']=w+' '+item['title']
                url='https://sellerchamp.com/api/products/'+product_ids[i]+'/product_images'
                headers={
                    'content-type':'application/json',
                    'token':'7690a200d8a675b404a100dc9cc93873'
                }
                try:
                    r=requests.get(url,headers=headers)
                    data=r.content
                    data=json.loads(data)
                    # # print(data)
                    image=data['product_images'][0]['large_image_url']
                    item['image']=image
                except:
                    pass
                self.product_list.append(item)
            except:
                continue



class SellerChampV2(object):
    def __init__(self,query):
        for i in range(len(query)):
            if(query[0]==' '):
                query=query[1:]
            else:
                break
        for i in range(len(query)-1,0,-1):
            if(query[len(query)-1]==' '):
                query=query[:-1]
            else:
                break
        self.product_list=[]
        self.query = query
        self.product = self.get_query_details()
        
    def getQueryType(self):
        ql=len(self.query)
        if(self.query.isdigit()==True):
            if(ql>=11 and ql<13):
                return 'upc'
            else:
                return 'mpn'
        else:
            if(ql==10):
                if (any(char.isdigit() for char in self.query)==True):
                    regex=r'([A-Z0-9]{10})'
                    match=re.match(regex,self.query)
                    if(match):
                        return 'asin'
                else:
                    return 'keyword'
            elif(ql==7):
                regex=r'sky[0-9]{4,6}$'
                match=re.match(regex,self.query,flags=re.IGNORECASE)
                if(match):
                    return 'mpn'
            else:
                return 'keyword' 
    def get_query_details(self):
        url='https://sellerchamp.com/api/manifests'
        data={}
        tp=self.getQueryType()
        if(tp=='asin'):
            data={
                'manifest':{
                    'name':arrow.now().format('MM-DD-YYYY'),
                    'ship_from_address_id':'5dd6b93eb5e2475184002578',
                    'marketplace_account_id':'5e445a84b5e24703870046df',
                    'product_listings_attributes':[
                        {'asin':self.query}
                    ]
                }
            }
        elif(tp=='mpn'):
            # p=productDataApi.ProductDataUPC(self.query)
            # upc=p.get_upc_from_mpn()
            data={
                'manifest':{
                    'name':arrow.now().format('MM-DD-YYYY'),
                    'ship_from_address_id':'5dd6b93eb5e2475184002578',
                    'marketplace_account_id':'5e445a84b5e24703870046df',
                    'product_listings_attributes':[
                        {'query':self.query}
                    ]
                }
            }
        elif(tp=='sky'):
            # p=productDataApi.ProductDataUPC(self.query)
            # upc=p.get_upc_from_mpn()
            # # print('Sky number converted to UPC: '+upc)
            data={
                'manifest':{
                    'name':arrow.now().format('MM-DD-YYYY'),
                    'ship_from_address_id':'5dd6b93eb5e2475184002578',
                    'marketplace_account_id':'5e445a84b5e24703870046df',
                    'product_listings_attributes':[
                        {'query':self.query}
                    ]
                }
            }
        elif(tp=='upc'):
            data={
                'manifest':{
                    'name':arrow.now().format('MM-DD-YYYY'),
                    'ship_from_address_id':'5dd6b93eb5e2475184002578',
                    'marketplace_account_id':'5e445a84b5e24703870046df',
                    'product_listings_attributes':[
                        {'asin':'','upc':self.query}
                    ]
                }
            }
        elif(tp=='keyword'):
            # p=productDataApi.ProductDataAPIWithKeyword(self.query)
            # upc=p.get_query_details()
            data={
                'manifest':{
                    'name':arrow.now().format('MM-DD-YYYY'),
                    'ship_from_address_id':'5dd6b93eb5e2475184002578',
                    'marketplace_account_id':'5e445a84b5e24703870046df',
                    'product_listings_attributes':[
                        {'query':self.query}
                    ]
                }
            }
        headers={
            'token':'7690a200d8a675b404a100dc9cc93873',
            'Content-Type': 'application/json',
            'cache-control': 'no-cache,no-cache,no-cache'
        }
        data=json.dumps(data)
        r=requests.post(url,headers=headers,data=data)
        data=r.content
        # print(data)
        data=json.loads(data)
        manifest_folder_id=data['manifest']['manifest_folder_id']
        manifest_id=data['manifest']['id']
        url='https://sellerchamp.com/api/manifests?marketplace_account_id=5e445a84b5e24703870046df&manifest_folder_id='+manifest_folder_id+'&page=1&page_size=25'
        headers={
            'token':'7690a200d8a675b404a100dc9cc93873'
        }
        r=requests.get(url,headers=headers)
        data=r.content
        data=json.loads(data)
        for i in range(10):            
            if(data['manifests'][0]['processing']==False):
                break
            else:
                time.sleep(1)
                # print('Waiting from seller champ API to respond to our search request. Please wait.'+'.'*i)
                url='https://sellerchamp.com/api/manifests?marketplace_account_id=5e445a84b5e24703870046df&manifest_folder_id='+manifest_folder_id+'&page=1&page_size=25'
                headers={
                    'token':'7690a200d8a675b404a100dc9cc93873'
                }
                r=requests.get(url,headers=headers)
                data=r.content
                data=json.loads(data)
        url='https://sellerchamp.com/api/manifests/'+manifest_id+'/product_listings?page=1&page_size=25'
        headers={
            'token':'7690a200d8a675b404a100dc9cc93873'
        }
        r=requests.get(url,headers=headers)
        product_ids=[]
        data=r.content
        data=json.loads(data)
        pl=data['product_listings']
        for i in range(len(pl)):
            product_ids.append(pl[i]['product_id'])
        
        for i in range(len(product_ids)):
            try:
                url='https://sellerchamp.com/api/products/'+product_ids[i]+'.json'
                headers={
                    'token':'7690a200d8a675b404a100dc9cc93873'
                }
                r=requests.get(url,headers=headers)
                data=r.content
                data=json.loads(data)
                data=data['product']
                item = {
                    'asinid': data['upc'],
                    'title': data['title'],
                    'rank': '',
                    'package_quantity': '1',
                    'retailer': data['brand'],
                    'image': '',
                    'description':data['description'],
                    'features':data['features'],
                    'price': data['retail_price'],
                    'url': '',
                    'height': data['item_dimensions']['height'],
                    'width':data['item_dimensions']['width'],
                    'length':data['item_dimensions']['length'],
                    'weight':data['weight_in_pounds'],
                    'model_no':data['mpn'],
                    'source':'Seller Champ',
                    'product_url':''  
                }
                if(tp=='sky'):
                    w=self.query
                    w=w.lower()
                    w=w.replace('sky','LQP')
                    item['title']=w+' '+item['title']
                url='https://sellerchamp.com/api/products/'+product_ids[i]+'/product_images'
                headers={
                    'content-type':'application/json',
                    'token':'7690a200d8a675b404a100dc9cc93873'
                }
                try:
                    r=requests.get(url,headers=headers)
                    data=r.content
                    data=json.loads(data)
                    # # print(data)
                    image=data['product_images'][0]['large_image_url']
                    item['image']=image
                except:
                    pass
                self.product_list.append(item)
            except:
                continue
        # for i in range(len(product_listing_ids)):
        #     url='https://sellerchamp.com/api/manifests/'+manifest_id+'/product_listings/'+product_listing_ids[i]+'.json'
        #     headers={
        #         'token':'7690a200d8a675b404a100dc9cc93873'
        #     }
        #     r=requests.request('DELETE',url,headers=headers)
class SellerChampV3(object):
    def __init__(self,query):
        for i in range(len(query)):
            if(query[0]==' '):
                query=query[1:]
            else:
                break
        for i in range(len(query)-1,0,-1):
            if(query[len(query)-1]==' '):
                query=query[:-1]
            else:
                break
        self.product_list=[]
        self.query = query
        self.get_query_details()
        
    def getQueryType(self):
        ql=len(self.query)
        if(self.query.isdigit()==True):
            if(ql>=11 and ql<13):
                return 'upc'
            else:
                return 'mpn'
        else:
            if(ql==10):
                if (any(char.isdigit() for char in self.query)==True):
                    regex=r'([A-Z0-9]{10})'
                    match=re.match(regex,self.query)
                    if(match):
                        return 'asin'
                else:
                    return 'keyword'
            elif(ql==7):
                regex=r'sky[0-9]{4,6}$'
                match=re.match(regex,self.query,flags=re.IGNORECASE)
                if(match):
                    return 'mpn'
            else:
                return 'keyword' 
    def get_query_details(self):
        url='https://sellerchamp.com/api/manifests'
        data={}
        data={
            'manifest':{
                'name':arrow.now().format('MM-DD-YYYY'),
                'ship_from_address_id':'5dd6b93eb5e2475184002578',
                'marketplace_account_id':'5e445a84b5e24703870046df',
                'product_listings_attributes':[
                    {'asin':'','upc':self.query}
                ]
            }
        }
        
        headers={
            'token':'7690a200d8a675b404a100dc9cc93873',
            'Content-Type': 'application/json',
            'cache-control': 'no-cache,no-cache,no-cache'
        }
        data=json.dumps(data)
        r=requests.post(url,headers=headers,data=data)
        data=r.content
        # # print(data)
        data=json.loads(data)
        manifest_folder_id=data['manifest']['manifest_folder_id']
        manifest_id=data['manifest']['id']
        url='https://sellerchamp.com/api/manifests?marketplace_account_id=5e445a84b5e24703870046df&manifest_folder_id='+manifest_folder_id+'&page=1&page_size=25'
        headers={
            'token':'7690a200d8a675b404a100dc9cc93873'
        }
        r=requests.get(url,headers=headers)
        data=r.content
        data=json.loads(data)
        for i in range(20):            
            if(data['manifests'][0]['processing']==False):
                break
            else:
                time.sleep(1)
                # print('Waiting from seller champ API to respond to our search request. Please wait.'+'.'*i)
                url='https://sellerchamp.com/api/manifests?marketplace_account_id=5e445a84b5e24703870046df&manifest_folder_id='+manifest_folder_id+'&page=1&page_size=25'
                headers={
                    'token':'7690a200d8a675b404a100dc9cc93873'
                }
                r=requests.get(url,headers=headers)
                data=r.content
                data=json.loads(data)
        url='https://sellerchamp.com/api/manifests/'+manifest_id+'/product_listings?page=1&page_size=25'
        headers={
            'token':'7690a200d8a675b404a100dc9cc93873'
        }
        r=requests.get(url,headers=headers)
        product_ids=[]
        data=r.content
        data=json.loads(data)
        pl=data['product_listings']
        for i in range(len(pl)):
            product_ids.append(pl[i]['product_id'])
        
        for i in range(len(product_ids)):
            try:
                url='https://sellerchamp.com/api/products/'+product_ids[i]+'.json'
                headers={
                    'token':'7690a200d8a675b404a100dc9cc93873'
                }
                r=requests.get(url,headers=headers)
                data=r.content
                data=json.loads(data)
                data=data['product']
                item = {
                    'asinid': data['upc'],
                    'title': data['title'],
                    'rank': '',
                    'package_quantity': '1',
                    'retailer': data['brand'],
                    'image': '',
                    'description':data['description'],
                    'features':data['features'],
                    'price': data['retail_price'],
                    'url': '',
                    'height': data['item_dimensions']['height'],
                    'width':data['item_dimensions']['width'],
                    'length':data['item_dimensions']['length'],
                    'weight':data['weight_in_pounds'],
                    'model_no':data['mpn'],
                    'source':'Seller Champ',
                    'product_url':''  
                }
                # if(tp=='sky'):
                #     w=self.query
                #     w=w.lower()
                #     w=w.replace('sky','LQP')
                #     item['title']=w+' '+item['title']
                url='https://sellerchamp.com/api/products/'+product_ids[i]+'/product_images'
                headers={
                    'content-type':'application/json',
                    'token':'7690a200d8a675b404a100dc9cc93873'
                }
                try:
                    r=requests.get(url,headers=headers)
                    data=r.content
                    data=json.loads(data)
                    # # print(data)
                    image=data['product_images'][0]['large_image_url']
                    item['image']=image
                except:
                    pass
                self.product_list.append(item)
            except:
                continue
        
def main():
    query=sys.argv[1]
    s=SellerChamp(query)
    print(json.dumps(s.product_list))
if __name__=='__main__':
    main()