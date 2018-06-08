# -*- coding: utf-8 -*-
"""
Created on 2018/3/14

@author: will4906
采集的内容、方式定义

Modified on 2018.06.08
@author: jiean001
"""

from bs4 import BeautifulSoup

from controller.url_config import url_search, url_detail, url_related_info, url_full_text
from crawler.items import DataItem
from entity.crawler_item import BaseItem, ResultItem
from util.JsonResult import *


class PatentId(BaseItem):
    is_required = True
    crawler_id = url_search.get('crawler_id')
    english = 'patent_id'
    chinese = ['专利标志', '专利id', '专利ID', '专利Id']

    @classmethod
    def parse(cls, raw, item, process=None):
        if process is not None:
            patent_id = process
            item.patent_id = ResultItem(title=cls.title, value=str(patent_id))
        return item


class PatentName(BaseItem):
    is_required = True
    crawler_id = url_detail.get('crawler_id')
    english = ['patent_name', 'invention_name']
    chinese = '专利名称'

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        if process is not None:
            patent_name = process.get_patent_name()
            item.patent_name = ResultItem(title=cls.title, value=str(patent_name))
        return item


class Abstract(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = 'abstract'
    chinese = '摘要'

    @classmethod
    def parse(cls, raw, item, process:DetaildsRecord=None):
        if process is not None:
            abstract = process.get_abstract()
            item.abstract = ResultItem(title=cls.title, value=abstract)
        return item

def push_item(details_str, item: DataItem, title, name):
    item.__setattr__(title, ResultItem(title=name, value=details_str))
    return item

class RequestNumber(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = ['request_number', 'application_number']
    chinese = '申请号'

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_indexCnName(), item, 'request_number', '申请号')


class RequestDate(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = 'request_date'
    chinese = '申请日'

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_request_date(), item, 'request_date', '申请日')


class PublishNumber(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = 'publish_number'
    chinese = ['公开号', '公布号', '公开（公告）号']

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_publish_number(), item, 'publish_number', '公开（公告）号')


class PublishDate(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = 'publish_date'
    chinese = ['公开日', '公布日', '公开（公告）日']

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_publish_date(), item, 'publish_date', '公开（公告）日')


class IpcClassificationNumber(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = ['ipc_class_number', 'IPC', 'ipc', 'Ipc']
    chinese = 'IPC分类号'

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_ipc_class_number(), item, 'ipc_class_number', 'IPC分类号')


class Applicant(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = ['Applicant', 'applicant', 'assignee', 'Assignee', 'proposer']
    chinese = ['申请人', '专利权人', '专利人', '申请（专利权）人']

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_applicant(), item, 'applicant', '申请（专利权）人')


class Inventor(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = ['Inventor', 'inventor']
    chinese = '发明人'

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_inventor(), item, 'inventor', '发明人')


class PriorityNumber(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = 'priority_number'
    chinese = '优先权号'

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_priority_number(), item, 'priority_number', '优先权号')


class PriorityDate(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = 'priority_date'
    chinese = '优先权日'

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_priority_date(), item, 'priority_date', '优先权日')


class AddressOfApplicant(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = ['proposer_address', 'address_of_the_Applicant', 'applicant_address']
    chinese = '申请人地址'

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        if process is not None:
            item = push_item(process.get_proposer_address(), item, 'proposer_address', '申请人地址')
        return item


class ZipCodeOfTheApplicant(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = ['proposer_post_code', 'zip_code_of_the_applicant', 'proposer_zip_code']
    chinese = '申请人邮编'

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_proposer_post_code(), item, 'proposer_zip_code', '申请人邮编')


class CountryOfTheApplicant(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = ['proposer_location', 'country_of_the_applicant', 'country_of_the_assignee']
    chinese = ['申请人所在国（省）', '申请人所在地']

    # todo 申请人所在国
    @classmethod
    def parse(cls, raw, item, process=None):
        return push_item(' ', item, 'proposer_location', '申请人所在国（省）')


class CpcClassificationNumber(BaseItem):
    crawler_id = url_detail.get('crawler_id')
    english = ['cpc_class_number', 'cpc', 'CPC', 'Cpc']
    chinese = 'CPC分类号'

    @classmethod
    def parse(cls, raw, item, process: DetaildsRecord=None):
        return push_item(process.get_cpc_class_number(), item, 'cpc_class_number', 'CPC分类号')


class Cognation(BaseItem):
    crawler_id = url_related_info.get('crawler_id')
    table_name = 'cognation'
    english = 'cognation_list'
    chinese = '同族表'
    title = '同族'

    @classmethod
    def parse(cls, raw, item, process=None):
        if process is not None:
            cognation_list = process.get('cognationList')
            # print('cognation', cognation_list)
            if cognation_list is not None:
                pn_list = []
                for cog in cognation_list:
                    pn_list.append(cog.get('pn'))
                item.cognation_list = ResultItem(table=cls.table_name, title=cls.title, value=pn_list)
        return item


class LawStateList(BaseItem):
    crawler_id = url_related_info.get('crawler_id')
    table_name = 'law_state'
    english = 'law_state_list'
    chinese = '法律状态表'
    title = ['法律状态', '法律状态时间']

    @classmethod
    def set_title(cls, title):
        if title == cls.english:
            cls.title = ['law_status', 'law_status_date']
        elif title == cls.chinese:
            cls.title = ['法律状态', '法律状态时间']

    @classmethod
    def parse(cls, raw, item, process=None):
        if process is not None:
            law_state_list = process.get('lawStateList')
            if law_state_list is not None:
                tmp_list = []
                for law in law_state_list:
                    mean = law.get('lawStateCNMeaning')
                    law_date = law.get('prsDate')
                    part = (ResultItem(table=cls.table_name, title=cls.title[0], value=mean),
                            ResultItem(table=cls.table_name, title=cls.title[1], value=law_date))
                    tmp_list.append(part)
                item.law_state_list = tmp_list
        return item


class FullText(BaseItem):
    crawler_id = url_full_text.get('crawler_id')
    english = ['full_text', 'whole_text']
    chinese = ['全文文本', '全文']

    @classmethod
    def parse(cls, raw, item, process=None):
        if process is not None:
            item.full_text = ResultItem(table=cls.table_name, title=cls.title,
                                        value=BeautifulSoup(str(process.get('fullTextDTO').get('literaInfohtml')), 'lxml')
                                        .get_text().replace("'", '"').replace(';', ',').replace('\n', '').replace('\t',',')
        return item
