# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from datetime import datetime
import hashlib
import logging
from twisted.enterprise import adbapi
from tutorial.db_connect import db_config

class MySQLPipeline(object):
  def __init__(self, db_pool):
    self.db_pool = db_pool

  @classmethod
  def from_settings(cls, settings):
    db_args = {
      'host'       : db_config['DB_HOST'],
      'db'         : db_config['DB'],
      'user'       : db_config['DB_USER'],
      'passwd'     : db_config['DB_PASSWORD'],
      'charset'    : 'utf8',
      'use_unicode': True
    }
    db_pool = adbapi.ConnectionPool('MySQLdb', **db_args)
    return cls(db_pool)

  def process_item(self, item, spider):
    d = self.db_pool.runInteraction(self._upsert, item, spider)
    d.addErrback(self._handle_error, item, spider)
    d.addBoth(lambda _: item)
    return d

  def _upsert(self, conn, item, spider):
    guid = self.get_guid(item['url'])
    now = datetime.utcnow().replace(microsecond=0).isoformat(' ')

    conn.execute("""
      SELECT EXISTS(
        SELECT 1 FROM magazine WHERE guid = %s
      )
    """, (guid,))
    ret = conn.fetchone()[0]

    if ret:
      conn.execute("""
        UPDATE magazine
        SET title=%s, updated=%s
        WHERE guid=%s
      """, (item['title'], now, guid))
    else:
      conn.execute("""
        INSERT INTO magazine (
          guid, title, url, created, updated
        ) VALUES (
          %s, %s, %s, %s, %s
        )
      """, (guid, item['title'], item['url'], now, now))

    spider.log('Saved!')

  def _handle_error(self, failure, item, spider):
    spider.log(failure, logging.ERROR)

  def get_guid(self, url):
    return hashlib.md5(url.encode('utf-8')).hexdigest()
# class TutorialPipeline:
#     def process_item(self, item, spider):
#         return item
