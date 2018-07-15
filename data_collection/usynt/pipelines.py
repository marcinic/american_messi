# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import CsvItemExporter


class UsyntPipeline(object):
    def __init__(self):
        self.file = open('prospects_v1.csv','wb')
        self.exporter = CsvItemExporter(self.file,'unicode')
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.clean_state(item)
        self.exporter.export_item(item)
        return item

    def clean_state(self,item):
        state = item['state']
        state = state.replace('.','')
        state = state.lower()
        substitutions = {
        'calif':'California',
        'fla':'Florida',
        'ill':'Illinois',
        'nj':'New Jersey',
        'ny':'New York',
        'wisc':'Wisconsin',
        'del':'Delaware',
        'nc':'North Carolina',
        'sc':'South Carolina',
        'minn':'Minnesota',
        'colo':'Colorado',
        'ala':'Alabama',
        'md':'Maryland',
        'miss':'Missouri',
        'mass':'Massachusetts',
        'conn':'Connecticut',
        'ga':'Georgia',
        'wash':'Washington',
        'mo':'Missouri',
        'ariz':'Arizona',
        'pa':'Pennsylvania',
        'va':'Virginia',
        'nm':'New Mexico',
        'mich':'Michigan',
        'dela':'Delaware',
        'penn':'Pennsylvania',
        'ut':'Utah',
        'kan':'Kansas',
        'wis':'Wisconsin'
        }
        if state in substitutions:
            item['state'] = substitutions[state]
