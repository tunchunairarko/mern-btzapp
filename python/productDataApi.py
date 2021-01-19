import requests
import dpath  # https://github.com/akesterson/dpath-python
from pprint import pprint  # Needed for printing responses, can be deleted.
import re
import AzProductInformation

class ProductDataUPC(object):
    def __init__(self,query):
        self.keys={
            'primary':'aed3a12f05464b8abb54c24d2750e377'
            
        }
        self.headers={
            'ApiGenius_API_Key': "aed3a12f05464b8abb54c24d2750e377"
        }
        self.url="https://api.apigenius.io/products/"
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
        self.query = query
        self.upc=''
    
    def get_upc_from_mpn(self,query=''):
        if not(query==''):
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
            self.query = query
        query_url=self.url+'/identifiers?mpn='+self.query
        r=requests.get(query_url,headers=self.headers)
        data=r.json()
        if(data['status']==404):
            return ''
        return data['items']['upc']
class ProductDataAPIWithKeyword(object):
    def __init__(self,query):
        self.keys={
            'primary':'aed3a12f05464b8abb54c24d2750e377'
            
        }
        self.headers={
            'ApiGenius_API_Key': "aed3a12f05464b8abb54c24d2750e377"
        }
        self.url="https://api.apigenius.io/products/"
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
        self.query = query
        self.image=[]
        self.description=''
        self.product_list=[]
        
    
    def get_query_details(self):
        endpoints=['identifiers','lookup','product-data','search']
        query_url=self.url+endpoints[3]+'?keyword='+self.query+'&api_key='+self.keys['primary']
        # print(query_url)
        r=requests.get(query_url,headers=self.headers)
        data=r.json()
        #print(data)
        if(data['status']==404):
            self.product_list.append({})
            return
        return data['items']['upc']
class ProductDataAPIWithMPN(object):
    def __init__(self,query):
        self.keys={
            'primary':'aed3a12f05464b8abb54c24d2750e377'
            
        }
        self.headers={
            'ApiGenius_API_Key': "aed3a12f05464b8abb54c24d2750e377"
        }
        self.url="https://api.apigenius.io/products/"
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
        self.query = query
        self.image=[]
        self.description=''
        self.product_list=[]
        self.product = self.get_query_details()
    
    def get_query_details(self):
        endpoints=['identifiers','lookup','product-data','search']
        query_url=self.url+endpoints[3]+'?keyword='+self.query+'&mpn='+self.query+'&api_key='+self.keys['primary']
        # print(query_url)
        r=requests.get(query_url,headers=self.headers)
        data=r.json()
        #print(data)
        if(data['status']==404):
            self.product_list.append({})
            return
        item = {'asinid': data['items']['upc'],
            'title': data['items']['title'],
            'rank': '',
            'package_quantity': '1',
            'retailer': data['items']['brand'],
            'image': '',
            'description':data['items']['description'],
            'price': data['items']['lowest_pricing'],
            'url': '',
            'height': data['items']['dimension'],
            'width':data['items']['dimension'],
            'length':data['items']['dimension'],
            'weight':data['items']['weight'],
            'model_no':data['items']['mpn'],
            'source':'',
            'product_url':''  
        }
        try:                    
            item['source']=data['items']['pricing'][0]['seller']
        except Exception as e:
            print(e)
            pass
        try:                    
            item['product_url']=data['items']['pricing'][0]['link']
        except Exception as e:
            print(e)
            pass
        try:                    
            item['image']=data['items']['images'][0]
        except Exception as e:
            print(e)
            pass
        self.product_list.append(item)
class ProductDataAPI(object):
    def __init__(self,query):
        self.keys={
            'primary':'aed3a12f05464b8abb54c24d2750e377'
            
        }
        self.headers={
            'ApiGenius_API_Key': "aed3a12f05464b8abb54c24d2750e377"
        }
        self.url="https://api.apigenius.io/products/"
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
        self.query = query
        self.image=[]
        self.description=''
        self.product_list=[]
        self.product = self.get_query_details()
    
        
    def get_query_details(self):
        endpoints=['identifiers','lookup','product-data','search']
        ql=len(self.query)
        if(self.query.isdigit()==True):
            #1st case: check if it is a upc
            # ql=len(self.query)
            if(ql>=11 and ql<13):#UPC CONFIRMED
                query_url=self.url+endpoints[1]+'?upc='+self.query+'&api_key='+self.keys['primary']
                r=requests.get(query_url,headers=self.headers)
                data=r.json()
                print(r.status_code)
                if(r.status_code==404):
                    self.product_list.append({})
                    return
                item = {'asinid': data['items']['upc'],
                    'title': data['items']['title'],
                    'rank': '',
                    'package_quantity': '1',
                    'retailer': data['items']['brand'],
                    'image': '',
                    'description':data['items']['description'],
                    'price': data['items']['lowest_pricing'],
                    'url': '',
                    'height': data['items']['dimension'],
                    'width':data['items']['dimension'],
                    'length':data['items']['dimension'],
                    'weight':data['items']['weight'],
                    'model_no':data['items']['mpn'],
                    'source':'',
                    'product_url':'' 
                }
                try:                    
                    item['source']=data['items']['pricing'][0]['seller']
                except Exception as e:
                    print(e)
                    pass
                try:                    
                    item['product_url']=data['items']['pricing'][0]['link']
                except Exception as e:
                    print(e)
                    pass
                try:                    
                    item['image']=data['items']['images'][0]
                except Exception as e:
                    print(e)
                    pass
                self.product_list.append(item)
            else:
                query_url=self.url+endpoints[3]+'?keyword='+self.query+'&mpn='+self.query+'&api_key='+self.keys['primary']
                # print(query_url)
                r=requests.get(query_url,headers=self.headers)
                data=r.json()
                print(r.status_code)
                if(data['status']==404):
                    self.product_list.append({})
                    return
                item = {'asinid': data['items']['upc'],
                    'title': data['items']['title'],
                    'rank': '',
                    'package_quantity': '1',
                    'retailer': data['items']['brand'],
                    'image': '',
                    'description':data['items']['description'],
                    'price': data['items']['lowest_pricing'],
                    'url': '',
                    'height': data['items']['dimension'],
                    'width':data['items']['dimension'],
                    'length':data['items']['dimension'],
                    'weight':data['items']['weight'],
                    'model_no':data['items']['mpn'],
                    'source':'',
                    'product_url':''  
                }
                try:                    
                    item['source']=data['items']['pricing'][0]['seller']
                except Exception as e:
                    print(e)
                    pass
                try:                    
                    item['product_url']=data['items']['pricing'][0]['link']
                except Exception as e:
                    print(e)
                    pass
                try:                    
                    item['image']=data['items']['images'][0]
                except Exception as e:
                    print(e)
                    pass
                self.product_list.append(item)
        else:
            regex=r'sky[0-9]{4,6}$'
            match=re.match(regex,self.query,flags=re.IGNORECASE)
            if(match): #BEST CHOICE PRODUCTS
                query_url=self.url+endpoints[3]+'?keyword='+self.query+'&mpn='+self.query+'&api_key='+self.keys['primary']
                # print(query_url)
                r=requests.get(query_url,headers=self.headers)
                
                data=r.json()
                print(r.status_code)
                if(data['status']==404):
                    self.product_list.append({})
                    return
                item = {'asinid': data['items']['upc'],
                    'title': data['items']['title'],
                    'rank': '',
                    'package_quantity': '1',
                    'retailer': data['items']['brand'],
                    'image': '',
                    'description':data['items']['description'],
                    'price': data['items']['lowest_pricing'],
                    'url': '',
                    'height': data['items']['dimension'],
                    'width':data['items']['dimension'],
                    'length':data['items']['dimension'],
                    'weight':data['items']['weight'],
                    'model_no':data['items']['mpn'],
                    'source':'',
                    'product_url':''  
                }
                try:                    
                    item['source']=data['items']['pricing'][0]['seller']
                except Exception as e:
                    print(e)
                    pass
                try:                    
                    item['product_url']=data['items']['pricing'][0]['link']
                except Exception as e:
                    print(e)
                    pass
                try:                    
                    item['image']=data['items']['images'][0]
                except Exception as e:
                    # print('lsadf')
                    print(e)
                    pass
                self.product_list.append(item)
                return
            if(ql==10) and (any(char.isdigit() for char in self.query)==True):#there is a chance it is an ASIN
                regex=r'([A-Z0-9]{10})'
                match=re.match(regex,self.query)
                if(match):
                    api=AzProductInformation.AzProductInformation(self.query)                
                    prodSearch=api.product_list[0]
                    if not(prodSearch['model_no']==None):
                        mpn=prodSearch['model_no']
                        query_url=self.url+endpoints[3]+'?keyword='+mpn+'&mpn='+mpn+'&api_key='+self.keys['primary']
                        r=requests.get(query_url,headers=self.headers)
                        data=r.json()
                        print(r.status_code)
                        if(data['status']==404):
                            self.product_list.append({})
                            return
                        item = {'asinid': data['items']['upc'],
                            'title': data['items']['title'],
                            'rank': '',
                            'package_quantity': '1',
                            'retailer': data['items']['brand'],
                            'image': '',
                            'description':data['items']['description'],
                            'price': data['items']['lowest_pricing'],
                            'url': '',
                            'height': data['items']['dimension'],
                            'width':data['items']['dimension'],
                            'length':data['items']['dimension'],
                            'weight':data['items']['weight'],
                            'model_no':data['items']['mpn'],
                            'source':'',
                            'product_url':''  
                        }
                        try:                    
                            item['source']=data['items']['pricing'][0]['seller']
                        except Exception as e:
                            print(e)
                            pass
                        try:                    
                            item['product_url']=data['items']['pricing'][0]['link']
                        except Exception as e:
                            print(e)
                            pass
                        try:                    
                            item['image']=data['items']['images'][0]
                        except Exception as e:
                            print(e)
                            pass
                        self.product_list.append(item)
                else:
                    query_url=self.url+endpoints[3]+'?keyword='+self.query+'&api_key='+self.keys['primary']
                    r=requests.get(query_url,headers=self.headers)
                    print(r.status_code)
                    data=r.json()
                    if(data['status']==404):
                        self.product_list.append({})
                        return
                    
                    item = {'asinid': data['items']['upc'],
                        'title': data['items']['title'],
                        'rank': '',
                        'package_quantity': '1',
                        'retailer': data['items']['brand'],
                        'image': '',
                        'description':data['items']['description'],
                        'price': data['items']['lowest_pricing'],
                        'url': '',
                        'height': data['items']['dimension'],
                        'width':data['items']['dimension'],
                        'length':data['items']['dimension'],
                        'weight':data['items']['weight'],
                        'model_no':data['items']['mpn'],
                        'source':'' ,
                        'product_url':''  
                    }
                    try:                    
                        item['source']=data['items']['pricing'][0]['seller']
                    except Exception as e:
                        print(e)
                        pass
                    try:                    
                        item['product_url']=data['items']['pricing'][0]['link']
                    except Exception as e:
                        print(e)
                        pass
                    try:                    
                        item['image']=data['items']['images'][0]
                    except Exception as e:
                        print(e)
                        pass
                    self.product_list.append(item)
            else:
                if(self.query.find(' ')==-1):
                    query_url=self.url+endpoints[3]+'?keyword='+self.query+'&mpn='+self.query+'&api_key='+self.keys['primary']
                    # print(query_url)
                    r=requests.get(query_url,headers=self.headers)
                    data=r.json()
                    if(data['status']==404):
                        self.product_list.append({})
                        return
                    item = {'asinid': data['items']['upc'],
                        'title': data['items']['title'],
                        'rank': '',
                        'package_quantity': '1',
                        'retailer': data['items']['brand'],
                        'image': '',
                        'description':data['items']['description'],
                        'price': data['items']['lowest_pricing'],
                        'url': '',
                        'height': data['items']['dimension'],
                        'width':data['items']['dimension'],
                        'length':data['items']['dimension'],
                        'weight':data['items']['weight'],
                        'model_no':data['items']['mpn'],
                        'source':'' ,
                        'product_url':''  
                    }
                    try:                    
                        item['source']=data['items']['pricing'][0]['seller']
                    except Exception as e:
                        print(e)
                        pass
                    try:                    
                        item['product_url']=data['items']['pricing'][0]['link']
                    except Exception as e:
                        print(e)
                        pass
                    try:                    
                        item['image']=data['items']['images'][0]
                    except Exception as e:
                        print(e)
                        pass
                    self.product_list.append(item)
                    return
                query_url=self.url+endpoints[3]+'?keyword='+self.query+'&api_key='+self.keys['primary']
                r=requests.get(query_url,headers=self.headers)
                data=r.json()
                if(data['status']==404):
                    self.product_list.append({})
                    return
                item = {'asinid': data['items']['upc'],
                    'title': data['items']['title'],
                    'rank': '',
                    'package_quantity': '1',
                    'retailer': data['items']['brand'],
                    'image': '',
                    'description':data['items']['description'],
                    'price': data['items']['lowest_pricing'],
                    'url': '',
                    'height': data['items']['dimension'],
                    'width':data['items']['dimension'],
                    'length':data['items']['dimension'],
                    'weight':data['items']['weight'],
                    'model_no':data['items']['mpn'],
                    'source':'' ,
                    'product_url':''  
                }
                try:                    
                    item['source']=data['items']['pricing'][0]['seller']
                except Exception as e:
                    print(e)
                    pass
                try:                    
                    item['product_url']=data['items']['pricing'][0]['link']
                except Exception as e:
                    print(e)
                    pass
                try:                    
                    item['image']=data['items']['images'][0]
                except Exception as e:
                    print(e)
                    pass
                self.product_list.append(item)
        # try:https://api.apigenius.io/products/search?keyword=0003093730273&mpn=0003093730273&api_key=5db34e7105f6491e99b02f4d5fca37c0
        #     query=int(self.query)
            
        #     # querystring={'upc':query,'api_key':self.keys['primary']}
        #     # r = requests.request("GET", self.url, headers=self.headers, params=querystring)
        #     r=requests.get(query_url,headers=self.headers)
        #     data=r.json()
        #     if(data['status']==404):
        #         return
        #     #print(data)
        # except Exception as e:
        #     #2nd case: Check if the query is a keyword or not
        #     ql=len(self.query)
        #     if(ql==10) and (any(char.isdigit() for char in self.query)==True):#there is a chance it is an ASIN
        #         #3rd case: check if it is an ASIN
        #         regex=r'([A-Z0-9]{10})'
        #         match=re.match(regex,self.query)
        #         if(match):
        #             api=AzProductInformation.AzProductInformation(self.query)                
        #             prodSearch=api.product_list[0]
        #             if not(prodSearch['model_no']==None):
        #                 upc=prodSearch['model_no']
        #                 query_url=self.url+endpoints[1]+'?upc='+upc+'&api_key='+self.keys['primary']
        #                 r=requests.get(query_url,headers=self.headers)
        #                 data=r.json()
        # querystring={"upc":self.query}
        # r = requests.request("GET", self.url, headers=self.headers, params=querystring)
        # data=r.json()
        # if(data['status']==404):
        #     return
        # self.image=data['items']['images']
        # self.description=data['items']['description']

        



# headers = {
#     'x-rapidapi-host': "product-data1.p.rapidapi.com",
#     'x-rapidapi-key': "3edae6ad4emsh2286662ae9bcb68p1bb68djsn63c5cf6f2cc6"
#     }

# r = requests.request("GET", url, headers=headers, params=querystring)
# print(r.json())


def main():
    # p=ProductDataUPC('SKY1263')
    p=ProductDataAPIWithKeyword('x00192KM3T')
    print(p.product_list)
if __name__=='__main__':
    main()