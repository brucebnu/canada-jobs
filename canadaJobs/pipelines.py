# -*- coding: utf-8 -*-
# import pymysql
# import datetime
import logging
from scrapy import signals


# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

# 实现参考 https://www.cnblogs.com/zhangjpn/p/6838384.html

class CanadajobsPipeline:

    def process_item(self, item, spider):
        # logging.warning('pipeline',item)
        return item

