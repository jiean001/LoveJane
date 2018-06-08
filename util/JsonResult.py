# -*- coding: utf-8 -*-
"""
Created on 2018/06/08

@Author: jiean001
"""
import json
from bs4 import BeautifulSoup

class DetaildsRecord:
    def __init__(self, body):
        self.body = json.loads(body)
        self.parse()

    def parse(self):
        abstractInfoDTO_dict = self.body['abstractInfoDTO']
        self.nrdAn = abstractInfoDTO_dict['nrdAn']
        self.nrdPn = abstractInfoDTO_dict['pn']
        self.patent_id = abstractInfoDTO_dict['id']

        tioIndex_dict = abstractInfoDTO_dict['tioIndex']
        self.patent_name = tioIndex_dict['value']

        abstractItemList = abstractInfoDTO_dict['abstractItemList']
        self.indexCnName = abstractItemList[0]['value']
        self.request_date = abstractItemList[1]['value']
        self.publish_number = abstractItemList[2]['value']
        self.publish_date = abstractItemList[3]['value']
        self.ipc_class_number = abstractItemList[4]['value']
        self.applicant = abstractItemList[5]['value']
        self.inventor = abstractItemList[6]['value']
        self.priority_number = abstractItemList[7]['value']
        self.priority_date = abstractItemList[8]['value']
        self.proposer_address = abstractItemList[9]['value']
        self.proposer_post_code = abstractItemList[10]['value']
        self.cpc_class_number = abstractItemList[11]['value']

        abIndexList = abstractInfoDTO_dict['abIndexList']
        self.abstract = abIndexList[0]['value']

    # CPC分类号
    def get_cpc_class_number(self):
        return self.cpc_class_number

    # 申请人邮编
    def get_proposer_post_code(self):
        return self.proposer_post_code

    # 申请人地址
    def get_proposer_address(self):
        return self.proposer_address

    # 优先权日
    def get_priority_date(self):
        return self.priority_date

    # 优先权号
    def get_priority_number(self):
        return self.priority_number

    # 发明人
    def get_inventor(self):
        return self.inventor

    # 专利权人
    def get_applicant(self):
        return self.applicant

    # ipc_class_number
    def get_ipc_class_number(self):
        return self.ipc_class_number

    # 公开日
    def get_publish_date(self):
        return self.publish_date

    # 公开号
    def get_publish_number(self):
        return self.publish_number

    # 申请日
    def get_request_date(self):
        return self.request_date

    # 摘要
    def get_abstract(self):
        self.abstract = BeautifulSoup(self.abstract, 'lxml').text.replace('\n', '').strip()
        return self.abstract

    # 申请号
    def get_indexCnName(self):
        return self.indexCnName

    def get_nrdAn(self):
        return self.nrdAn

    def get_nrdPn(self):
        return self.nrdPn

    def get_patent_id(self):
        return self.patent_id

    def get_patent_name(self):
        return self.patent_name

class SearchResultRecord:
    def __init__(self, searchResultRecord):
        self.searchResultRecord = searchResultRecord
        self.parse()

    def parse(self):
        searchResultRecord_fieldMap = self.searchResultRecord['fieldMap']
        self.patent_id = searchResultRecord_fieldMap['ID']
        self.nrdAn = searchResultRecord_fieldMap['AP']
        self.nrdPn = searchResultRecord_fieldMap['PN']

    def get_patent_id(self):
        return self.patent_id

    def get_nrdAn(self):
        return self.nrdAn

    def get_nrdPn(self):
        return self.nrdPn

class SearchResultUtil:
    def __init__(self, body):
        self.body = body
        self.parse()

    def parse(self):
        wb_data = json.loads(self.body)
        searchResultDTO_dict = wb_data['searchResultDTO']
        self.executableSearchExp = searchResultDTO_dict['executableSearchExp']
        self.searchResultRecord_list = searchResultDTO_dict['searchResultRecord']

        searchCondition_dict = wb_data['searchCondition']
        pagination_dict = searchCondition_dict['pagination']
        self.limit = pagination_dict['limit']
        self.start = pagination_dict['start']
        self.totalCount = pagination_dict['totalCount']

        self.searchExp = searchCondition_dict['searchExp']

    def get_searchResultRecord_list(self):
        return self.searchResultRecord_list

    def get_limit(self):
        return self.limit

    def get_start(self):
        return self.start

    def get_totalCount(self):
        return self.totalCount

    def get_executableSearchExp(self):
        return self.executableSearchExp

    def get_searchExp(self):
        return self.searchExp