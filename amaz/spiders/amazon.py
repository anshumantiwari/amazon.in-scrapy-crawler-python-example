import scrapy
import pymongo
import requests
import math
from bs4 import BeautifulSoup
from pymongo import MongoClient
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy import Request
from amaz.items import AmazonItem
from time import gmtime, strftime
import sys
class AmazSpider(BaseSpider):
    name = "amaz"
    allowed_domains = ["www.amazon.in"]
    global client
    global db
    global cat
    global slug
    cat=''
    slug=''
    for arg in sys.argv: 1
    ass=arg.split('=')
    asd=ass[1].replace('"',"")
    args=asd.split(',')
    slug=args[0]
    cat=args[1]
    client=MongoClient()
    db=client.lootore
    global coll
    coll=db.crawl_data
    durl = "www.amazon.in/gp/aw/s/ref=aw_lnk_cv_mobiles_smart_and_basic/279-5753335-8695060?aid=aw_gw&apid=585736887&arc=1201&arid=002HJ6XR1BSB8SA4YGS5&asn=center-15&node="+slug
    global block
    block=["offers","2","3","Next","Cart","Your Account","Wish List","Find a Wish List","Sign Out","Help","Amazon.in Home","Legal Terms","Previous","Try different image"]
    url=durl.replace('gp/aw/','')
    url=url+'&page=2'
    headers = {
    'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; AOL 9.7; AOLBuild 4343.19; Windows NT 6.1; WOW64; Trident/5.0; FunWebProducts)'
}
    r  = requests.get("http://" +url,headers=headers)
    data = r.text
    soup = BeautifulSoup(data)
    count=''
    counts=soup.findAll("h2", { "id" : "s-result-count" })
    for bount in counts:
            count=bount.get_text()
    bbb=count.split(' ')
    chount=int(bbb[2].replace(',',''))
    print chount
    count=math.ceil(chount/5)
    count=int(count+1)
    print count
    start_urls=[]
    for i in range(1,count):
        start_urls.append("http://" +durl+"&page="+str(i))
    def parse(self, response):
       hxs=HtmlXPathSelector(response)
       ur=hxs.select("//a/text()").extract()
       href=hxs.select("//a/@href").extract()
       for x in range(0,5):
           if ur[x] not in block:
              the_u=href[x]
              the_u=the_u.replace('gp/aw/d','gp/product')
              thev_u="http://www.amazon.in"+the_u
              request =  Request(thev_u,  callback = self.parse_statdetail)
              yield request
        
    def parse_statdetail(self, response):
       hxs=HtmlXPathSelector(response)
       item = AmazonItem()
       price=hxs.select("//div[contains(@id, 'price_feature_div')]")
       offer=hxs.select("//div[contains(@id, 'olp_feature_div')]")
       item ['product_name'] = hxs.select('.//span[@id="productTitle"]/text()').extract()
       pr=price.select("//span[contains(@id, 'priceblock_')]/text()").extract()
       ofpr=offer.select(".//span[contains(@class, 'a-color-price')]/text()").extract()
       pri=pr[0].replace(',','')
       pri=pri.replace('.','')
       ofpri=ofpr[0].replace(',','')
       ofpri=ofpri.replace('.','')
       item['price']=int(pri)/100
       item['offer_price']=int(ofpri)/100
       item ['specs']=hxs.select('.//*[@id="prodDetails"]/div/div[1]/div/div/div[2]/div/div/table/tbody/tr/td/text()').extract()
       item ['excerpts']=hxs.select(".//div[contains(@id, 'feature-bullets')]/ul/li/span/text()").extract()
       warran=hxs.select("//div[contains(@id, 'wns')]/text()").extract()
       warrant=warran[1].split(' ')
       try:
           warr=warrant[1]+' '+warrant[2]
       except IndexError:
           warr=''
       item['warranty']=warr
       imag=hxs.select('//*[@id="landingImage"]/@data-a-dynamic-image').extract()
       jg=imag[0].split(',')
       jg=jg[0].split(':[')
       jug=jg[0].replace('"','')
       jug=jug.replace('{','')
       item ['image']=jug
       rat=hxs.select("//span[contains(@class, 'reviewCountTextLinkedHistogram')]/@title").extract()
       item ['rating']=rat[0][:3].replace(" o","")
       sat=rat[0].split(" ")
       ru=hxs.select("//span[contains(@id, 'acrCustomerReviewText')]/text()").extract()
       bu=ru[0].replace(" customer reviews","")
       bu=bu.replace(",","")
       item ['rating_count']=bu
       sold=1
       preod=0
       sold_out=hxs.select('//*[@id="availability"]/text()').extract()
       sod=sold_out[0].replace('.','')
       if "unavailable" not in sod:
           sold=0
       if "will be" in sod:
           preod=1
       item['sold_out']=sold
       cod=hxs.select("//span[contains(@id, '_shippingmessage')]/span/b/text()").extract()
       ship=0
       co=0
       try:
           if "FREE" in cod[0]:
               ship=1
       except IndexError:
           ship=0
       try:
           if "Cash" in cod[1]:
               co=1
       except IndexError:
           co=0
       item['cod']=co
       item['free_shipping']=ship
       item['url']=response.url
       item['prebook']=preod
       coll.insert({"product":item['product_name'][0],"price":item['price'],"specs":item['specs'],"store":"amazon","url":item['url'],"image":item['image'],"cod":item['cod'],"sold_out":item['sold_out'],"prebook":item['prebook'],"rating":item['rating'],"rating_count":item['rating_count'],"category":cat,"excerpts":item['excerpts']})
       yield item
db.crawl_log.insert({"text":"Finished Crawling Amazon - " + cat,"time":strftime("%Y-%m-%d %H:%M:%S", gmtime())})

