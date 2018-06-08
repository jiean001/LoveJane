import json

import math

import os
import scrapy
import webbrowser
from bs4 import BeautifulSoup
from logbook import Logger
from scrapy import Request, FormRequest

import controller
from config.base_settings import *
from config.query_config import QUERY_LIST
from controller.url_config import *
from crawler.items import DataItem, WrapperItem
from service import info
from visual import create_charts
from util.JsonResult import *

logger = Logger(__name__)

class PatentSpider(scrapy.Spider):
    """
    专利网爬虫定义
    """
    name = "Patent"
    allowed_domains = ["pss-system.gov.cn"]
    query_list = QUERY_LIST
    process_len = 4

    def __init__(self, *args, **kwargs):
        self.target_dict = {
            url_detail.get('crawler_id'): self.gen_detail,
            url_related_info.get('crawler_id'): self.gen_related_info,
            url_full_text.get('crawler_id'): self.gen_full_text
        }
        super().__init__(*args, **kwargs)

    def gen_detail(self, **kwargs):
        """
        生成查询详情的请求
        :param patent_id, sipo, data_item, nrdAn, nrdPn:
        :return:
        """
        patent_id = str(kwargs.pop('patent_id'))
        formdata = url_detail.get('form_data')
        formdata.__setitem__('nrdAn', patent_id.split('.')[0])
        formdata.__setitem__('cid', patent_id)
        formdata.__setitem__('sid', patent_id)

        return FormRequest(
            url=url_detail.get('url'),
            formdata=formdata,
            headers=url_detail.get('headers'),
            callback=self.parse_patent_detail,
            meta={'sipo': kwargs.pop('sipo'), 'data_item': kwargs.pop('data_item'), 'patent_id': patent_id,
                  'law_info': {'nrdAn': kwargs.pop('nrdAn'), 'nrdPn': kwargs.pop('nrdPn')}}
        )

    def gen_related_info(self, **kwargs):
        """
        生成相关信息的请求，包含法律信息和同族信息
        :param sipo:
        :param data_item:
        :param nrdAn:
        :param nrdPn:
        :return:
        """
        form_data = url_related_info.get('form_data')
        form_data.__setitem__('literaInfo.nrdAn', kwargs.pop('nrdAn'))
        form_data.__setitem__('literaInfo.nrdPn', kwargs.pop('nrdPn'))
        return FormRequest(
            url=url_related_info.get('url'),
            method='POST',
            dont_filter=True,  # 此处可能会发生重复采集，但是还是想要采集，所以关闭过滤
            formdata=form_data,
            callback=self.parse_related_info,
            meta={'sipo': kwargs.pop('sipo'),
                  'data_item': kwargs.pop('data_item'),
                  'patent_id': kwargs.pop('patent_id')}
        )

    def gen_full_text(self, **kwargs):
        """
        生成全文文本的请求
        :param patent_id:
        :param sipo:
        :param data_item:
        :return:
        """
        patent_id = str(kwargs.pop('patent_id'))
        form_data = url_full_text.get('form_data')
        form_data.__setitem__('nrdAn', patent_id.split('.')[0])
        form_data.__setitem__('cid', patent_id)
        form_data.__setitem__('sid', patent_id)
        return FormRequest(
            url=url_full_text.get('url'),
            method='POST',
            dont_filter=True,  # 此处可能会发生重复采集，但是还是想要采集，所以关闭过滤
            formdata=form_data,
            callback=self.parse_full_text,
            meta={'sipo': kwargs.pop('sipo'), 'data_item': kwargs.pop('data_item')}
        )

    def gen_wrapper_item(self, data_item):
        """
        生成包裹的采集对象
        :param data_item:
        :return:
        """
        wrapper = WrapperItem()
        wrapper['data'] = data_item
        return wrapper

    def turn_to_request(self, now, **kwargs):
        """
        下一可采集请求的生成转换逻辑
        :param now:
        :param kwargs:
        :return:
        """
        next_target = now
        for i in range(now + 1, self.process_len):
            target_len = len(info.crawler_dict.get(str(i)))
            if target_len > 0:
                next_target = i
                break
        if next_target == now:
            data_item = kwargs.pop('data_item')
            return self.gen_wrapper_item(data_item)
        else:
            return self.target_dict.get(str(next_target))(**kwargs)

    def start_requests(self):
        """
        初始请求
        :return:
        """
        for sipo in self.query_list:
            headers = url_search.get('headers')
            search_exp_cn = sipo.search_exp_cn
            logger.info('检索表达式--- %s' % search_exp_cn)
            form_data = url_search.get('form_data')
            form_data.__setitem__('searchCondition.searchExp', search_exp_cn)
            yield FormRequest(
                url=url_search.get('url'),
                callback=self.parse,
                method="POST",
                headers=headers,
                formdata=form_data,
                meta={'sipo': sipo}
            )

    def parse_not_first_page(self, response):
        body = response.body_as_unicode()
        sipo = response.meta['sipo']
        crt_page_result = SearchResultUtil(body)

        # 处理详情等
        for record in crt_page_result.get_searchResultRecord_list():
            crt_record = SearchResultRecord(record)
            nrdAn = crt_record.get_nrdAn()
            nrdPn = crt_record.get_nrdPn()
            patent_id = crt_record.get_patent_id()
            data_item = DataItem()

            for crawler in info.crawler_dict.get('0'):
                crawler.parse(body, data_item, patent_id)
            yield self.turn_to_request(int(url_search.get('crawler_id')), data_item=data_item, nrdAn=nrdAn, nrdPn=nrdPn,
                                       patent_id=patent_id, sipo=sipo)

    def parse(self, response):
        body = response.body_as_unicode()
        sipo = response.meta['sipo']
        top_page_result = SearchResultUtil(body)

        if top_page_result.get_totalCount() == 0:
            logger.info('共0页')
        else:
            page_sum = int(math.ceil(top_page_result.get_totalCount() / top_page_result.get_limit()))
            logger.info('共 %s 页' % page_sum)
            if top_page_result.get_executableSearchExp() is None:
                return

            # 处理详情等
            for record in top_page_result.get_searchResultRecord_list():
                crt_record = SearchResultRecord(record)
                nrdAn = crt_record.get_nrdAn()
                nrdPn = crt_record.get_nrdPn()
                patent_id = crt_record.get_patent_id()
                data_item = DataItem()

                for crawler in info.crawler_dict.get('0'):
                    crawler.parse(body, data_item, patent_id)
                yield self.turn_to_request(int(url_search.get('crawler_id')), data_item=data_item, nrdAn=nrdAn, nrdPn=nrdPn, patent_id=patent_id, sipo=sipo)


            # 处理翻页
            for index in range(1, page_sum):
                formdata = url_page_turning.get('form_data')
                formdata.__setitem__('resultPagination.start', str(top_page_result.get_limit() * index))
                formdata.__setitem__('resultPagination.totalCount', str(top_page_result.get_totalCount()))
                formdata.__setitem__('searchCondition.searchExp', top_page_result.get_searchExp())
                formdata.__setitem__('searchCondition.executableSearchExp', top_page_result.get_executableSearchExp())
                yield FormRequest(
                    url=url_page_turning.get('url'),
                    callback=self.parse_not_first_page,
                    method="POST",
                    headers=url_page_turning.get('headers'),
                    formdata=formdata,
                    meta={
                        'sipo': sipo
                    }
                )

    def parse_patent_detail(self, response):
        """
        解析专利详情页
        :param response:
        :return:
        """
        sipo = response.meta['sipo']
        data_item = response.meta['data_item']
        body = response.body_as_unicode()
        detailds = DetaildsRecord(body)
        for crawler in info.crawler_dict.get(url_detail.get('crawler_id')):
            crawler.parse(body, data_item, detailds)
        yield self.turn_to_request(int(url_detail.get('crawler_id')), nrdAn=detailds.get_nrdAn(),
                                   nrdPn=detailds.get_nrdPn(), sipo=sipo, data_item=data_item, patent_id=detailds.get_patent_id())

    def parse_related_info(self, response):
        """
        解析相关信息页
        :param response:
        :return:
        """
        body = response.body_as_unicode()
        related = json.loads(body)
        data_item = response.meta['data_item']
        sipo = response.meta['sipo']
        patent_id = response.meta['patent_id']

        for crawler in info.crawler_dict.get(url_related_info.get('crawler_id')):
            crawler.parse(body, data_item, related)

        yield self.turn_to_request(int(url_related_info.get('crawler_id')), data_item=data_item, sipo=sipo, patent_id=patent_id)

    def parse_full_text(self, response):
        """
        解析全文文本页
        :param response:
        :return:
        """
        body = response.body_as_unicode()
        full = json.loads(body)
        data_item = response.meta['data_item']
        for crawler in info.crawler_dict.get(url_full_text.get('crawler_id')):
            crawler.parse(body, data_item, full)
        yield self.turn_to_request(int(url_full_text.get('crawler_id')), data_item=data_item)

    def closed(self, reason):
        # webbrowser.open(AD_PATH)
        # if os.path.exists(DATABASE_NAME) and 'data' in OUTPUT_ITEMS and 'chart' in OUTPUT_ITEMS:
        #     create_charts()
        logger.info(reason)
