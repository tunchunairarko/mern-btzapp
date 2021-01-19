from wapy.api import Wapy
import dpath  # https://github.com/akesterson/dpath-python


class WlmtProductInformation(object):
    def __init__(self,query):
        self.wapy = Wapy('6p5262fw27pew6vdq7n7js4c') # Create an instance of Wapy.
        self.product_list = []
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
        try:
            self.products = self.get_query_details()
            self.parsed_products()
        except KeyError:
            self.product_list.append({})

    def get_query_details(self):
        return self.wapy.search(self.query)
    def __clearTitle(self,title):
        title=title.encode('utf-8')
        title=title.decode()
        arr=['%','\\','/','\'','$','^','@']
        for i in range(len(arr)):
            title=title.replace(arr[i],'')
        return title
    def parsed_products(self):
        try:
            for i in range(len(self.products)):            
                try:
                    asinid=self.products[i].upc
                except KeyError:
                    asinid=None
                try:
                    product_url=self.products[i].product_url
                except KeyError:
                    product_url=None
                try:
                    product_title=self.products[i].name
                    product_title=self.__clearTitle(product_title)
                except KeyError:
                    product_title=None
                try:
                    price = str(self.products[i].sale_price)
                except KeyError:
                    price = None
                try:
                    product_image = self.products[i].thumbnail_image
                except KeyError:
                    product_image = None
                try:
                    product_brand = self.products[i].brand_name
                except KeyError:
                    product_brand = None
                
                try:
                    length = self.products[i].length
                except KeyError:
                    length = None
                try:
                    width = self.products[i].width
                except KeyError:
                    width = None
                try:
                    height = self.products[i].height                
                except KeyError:
                    height = None
                try:
                    weight = self.products[i].color
                except KeyError:
                    weight = None
                product_rank=''
                item = {
                    'asinid': asinid,
                    'title': product_title,
                    'rank': product_rank,
                    'retailer': product_brand,
                    'image': product_image,
                    'price': price,
                    'url': product_url,
                    'height': height,
                    'width':width,
                    'length':length,
                    'weight':weight 
                }
                self.product_list.append(item)
        except KeyError:
            self.product_list.append({})
def main():
    wlmt=WlmtProductInformation('NUTRO CANNED DOG FOOD 12 PACK')
    product=wlmt.product_list
    print(product)
if __name__=='__main__':
    main()