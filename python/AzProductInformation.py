from mws import mws  # https://github.com/czpython/python-amazon-mws
import dpath  # https://github.com/akesterson/dpath-python
from pprint import pprint  # Needed for printing responses, can be deleted.
import dpath.util


class AzProductInformation(object):
    def __init__(self, query):
        self.access_key = 'AKIAIKLWKP5M7YJS7NQA'
        self.secret_key = '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'
        self.seller_id = 'A22T8AW2OVSAA6'
        self.marketplace_usa = 'ATVPDKIKX0DER'  # US Marketplace ATVPDKIKX0DER
        self.product_list = []
        # if(query[len(query)-1]==' ') or (query[-1]==' '):
        #     query=query[:-1]
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
        
        self.products_api = mws.Products(self.access_key, self.secret_key, self.seller_id, region='US')
        
        self.products = self.get_query_details()
        # print(self.products)
        self.parsed_products()

    def get_query_details(self):
        raw_products = self.products_api.list_matching_products(marketplaceid=self.marketplace_usa, query=self.query)
        
        return raw_products.parsed

    def get_asin_lowest_price(self, asins):
        raw_prices = self.products_api.get_competitive_pricing_for_asin(marketplaceid=self.marketplace_usa, asins=asins)
        rp = raw_prices.parsed
        prices_dict = {}
        if type(rp) is not list:
            rp = [rp]

        for p in rp:
            try:
                asin = dpath.util.get(p, '/ASIN/value')
            except KeyError as e:
                print(e)
                asin = None

            try:
                price = dpath.util.get(p, '/Product/CompetitivePricing/CompetitivePrices/CompetitivePrice')

                if type(price) is list:
                    price = dpath.util.get(price[0], '/Price/LandedPrice/Amount/value')
                else:
                    price = dpath.util.get(price, '/Price/LandedPrice/Amount/value')

            except KeyError as e:
                print(e)
                price = None
            
            prices_dict[asin] = price
        return prices_dict
    def __clearTitle(self,title):
        title=title.encode('utf-8')
        title=title.decode()
        arr=['%','\\','/','\'','$','^','@']
        for i in range(len(arr)):
            title=title.replace(arr[i],'')
        return title
    def parsed_products(self):
        try:
            prod = dpath.util.get(self.products, 'Products/Product')
            if type(prod) is not list:
                prod = [prod]

            prices = self.get_asin_lowest_price([dpath.util.get(x, '/Identifiers/MarketplaceASIN/ASIN/value') for x in prod])

            for p in prod:
                
                try:
                    ASIN = dpath.util.get(p, '/Identifiers/MarketplaceASIN/ASIN/value')
                    product_url = 'http://www.amazon.com/dp/{}'.format(ASIN)
                except KeyError as e:
                    print(e)
                    ASIN = None
                try:
                    model_no=dpath.util.get(p,'/AttributeSets/ItemAttributes/Model/value')
                except KeyError as e:
                    print(e)
                    model_no=None
                try:
                    product_title = dpath.util.get(p, '/AttributeSets/ItemAttributes/Title/value')
                    product_title=self.__clearTitle(product_title)
                except KeyError as e:
                    print(e)
                    product_title = None

                try:
                    product_rank = dpath.util.get(p, '/SalesRankings/SalesRank/[0]/Rank/value')
                except KeyError as e:
                    print(e)
                    product_rank = None

                try:
                    package_quantity = dpath.util.get(p, 'AttributeSets/ItemAttributes/PackageQuantity/value')
                except KeyError as e:
                    print(e)
                    package_quantity = None

                try:
                    product_brand = dpath.util.get(p, 'AttributeSets/ItemAttributes/Brand/value')
                except KeyError as e:
                    print(e)
                    product_brand = None

                try:
                    product_image = dpath.util.get(p, 'AttributeSets/ItemAttributes/SmallImage/URL/value')
                except KeyError as e:
                    print(e)
                    product_image = None

                try:
                    price = prices[ASIN]
                except KeyError as e:
                    print(e)
                    price = None
                if(price==None):
                    # print(p)
                    try:
                        same_price=dpath.util.get(p, 'AttributeSets/ItemAttributes/ListPrice/Amount/value')
                        price=same_price
                    except Exception as e:
                        print(e)
                        price=None
                # print('sa')
                try:
                    height = dpath.util.get(p, '/AttributeSets/ItemAttributes/PackageDimensions/Height/value')
                    length = dpath.util.get(p, '/AttributeSets/ItemAttributes/PackageDimensions/Length/value')
                    width = dpath.util.get(p, '/AttributeSets/ItemAttributes/PackageDimensions/Width/value')
                    weight = dpath.util.get(p, '/AttributeSets/ItemAttributes/PackageDimensions/Weight/value')

                    height=str(height)
                    length=str(length)
                    width=str(width)
                    weight=str(float(weight)*16)

                except KeyError:
                    height = ""
                    length = ""
                    width = ""
                    weight = ""
                item = {'asinid': ASIN,
                        'title': product_title,
                        'rank': product_rank,
                        'package_quantity': package_quantity,
                        'retailer': product_brand,
                        'image': product_image,
                        'price': price,
                        'url': product_url,
                        'height': height,
                        'width':width,
                        'length':length,
                        'weight':weight,
                        'model_no':model_no 
                        }
                if not(price==None):                       
                    self.product_list.append(item)
        except KeyError as e:
            print(e)
            self.product_list.append({})

# print('*' * 80)
# print('Search Term: x00192KM3T')
# AmazonAPI = AzProductInformation('x00192KM3T')
# pprint(AmazonAPI.product_list)

# print('*' * 80)
# print('Search Term: 047875881525')
# AmazonAPI = AzProductInformation('047875881525')
# pprint(AmazonAPI.product_list)

# print('*' * 80)
# print('Search Term: Orgain Organic Plant Based Protein Powder')
# AmazonAPI = AzProductInformation('Orgain Organic Plant Based Protein Powder')
# pprint(AmazonAPI.product_list)

# print('*' * 80)
# print('Search Term: B07SSXWJ2V')
# AmazonAPI = AzProductInformation('B07SSXWJ2V')
# pprint(AmazonAPI.product_list)
