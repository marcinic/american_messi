# -*- coding: utf-8 -*-
import scrapy
import lxml.etree
import lxml.html
import re
from urllib.parse import urlparse
from scrapy.loader import ItemLoader
from usynt.items import Player
from usynt.pipelines import UsyntPipeline

class ProspectSpider(scrapy.Spider):
    name = 'prospect'
    allowed_domains = ['ussoccer.com']
    f = open('usynt_links.txt')
    start_urls = [url.strip() for url in f.readlines()]
    #start_urls = ['https://www.ussoccer.com/stories/2018/07/13/20/08/20180713-news-u20mnt-builds-roster-with-world-cup-qualifying-on-horizon-with-camp-in-north-carolina']
    pipeline = UsyntPipeline()

    def parse(self, response):

        root = lxml.html.fromstring(response.body)
        lxml.etree.strip_elements(root,lxml.etree.Comment,"script","head")
        text = lxml.html.tostring(root,method="text",encoding="unicode")

        gk = re.search('GOALKEEPERS',text)
        d = re.search('DEFENDERS',text)
        mid = re.search('MIDFIELDERS',text)
        fwd = re.search('FORWARDS',text)

        if gk:
            title = response.selector.xpath('//h1/text()')[0].extract()
            level = re.search('U-[0-9]{2}',title)
            if level:
                level = level.group(0)
            date = self.get_date(response.url)
            filename = level.replace('-','')+date.replace('/','')+'.csv'.lower()
            goalie_text = text[gk.span()[1]+5:d.span()[0]]
            defender_text = text[d.span()[1]+5:mid.span()[0]]
            mid_text = text[mid.span()[1]+5:fwd.span()[0]]
            text_break = re.search('\n',text[fwd.span()[1]::]).span()[0]
            fwd_text = text[fwd.span()[1]+5:fwd.span()[1]+text_break]
            self.extract_info(goalie_text,'Goalkeeper',level,date)
            self.extract_info(defender_text,'Defender',level,date)
            self.extract_info(mid_text,'Midfielder',level,date)
            self.extract_info(fwd_text,'Forward',level,date)
        else:
             pass

    def extract_info(self,text,position,level,date,pipeline):
        rows = text.split('),')
        players = []
        for row in rows :
            name,rest = row.split('(')
            rest = rest.replace(';',',')
            try:
                club,city,state = rest.split(',')
            except ValueError:
                club,rest = rest.split(',')
                city,state = rest.split()

            state = state.replace(')','')
            state = state.replace('\n','')
            state = state.strip()
            player = Player(name=name,club=club,city=city,state=state,position=position,level=level,date=date)
            self.pipeline.process_item(player,None)


    def get_date(self,url):
        o = urlparse(url)
        parts = o.path.split('/')
        date = parts[2:5]
        date = '/'.join(date)
        return date
