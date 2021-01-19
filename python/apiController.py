import sellerChamp
import productDataApi
import AzProductInformation
import WlmtProductInformation
import json
import sys
import jsonpickle
def main():
    query=sys.argv[1]
    marketplace=jsonpickle.loads(sys.argv[2])
    # print(marketplace)
    # jsonpickle.loads
    # print(jsonpickle.loads(marketplace))
    if(marketplace['sellerChamp']==True):
        s=sellerChamp.SellerChamp(query)
        print(json.dumps(s.product_list))
if __name__=='__main__':
    main()