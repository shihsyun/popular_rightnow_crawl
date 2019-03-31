# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from pymongo import MongoClient
import logging
import json

class PopularSpiderPipeline(object):
    def open_spider(self, spider):
        db_name = spider.settings.get('MONGODB_DB_NAME', 'etsy')
        self.db_client = MongoClient('mongodb://mongo:27017')
        self.db = self.db_client[db_name]
        

    def process_item(self, item, spider):
        logger = logging.getLogger()
        collect = self.db['popular_rightnow']
        item = dict(item)
        logger.info('function def process_item got item _id: %s .', str(item['_id']))
        if bool(len(['' for x in item.values() if not x])):
            logger.info('function def process_item got this item didn\'t have name/shopname, let\'s drop it.')
            return item

        logger.info('function def process_item query document.')
        result = collect.find_one({'_id':item['_id']})
        logger.info('%s', json.dumps(result, indent=4))

        if result is None:
            item = dict(item)
            logger.info('function def process_item insert new document.')
            logger.info('%s', json.dumps(item, indent=4))
            try:
                collect.insert_one(item)
            except Exception as e:                    
                logging.error('mongodb insert data fail, Exception occured: %s' %e , exc_info=True)

        else:            
            tmp = result['appeardate']
            elem = item['appeardate'].pop()
            if elem not in tmp:
                tmp.append(elem)
                logger.info('function def process_item update old document for new appeardate')
                logger.info('%s', json.dumps(tmp, indent=4))
                try:
                    collect.update_one({'_id':item['_id']},{'$set':{'appeardate':tmp}}, upsert=False)
                except Exception as e:                    
                    logging.error('mongodb update data fail, Exception occured: %s' %e , exc_info=True)
                
        return item

    def close_spider(self, spider):
        self.db_client.close()
