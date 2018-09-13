#! /usr/lib/python
# -*- coding: utf-8 -*-


from file_name_fetcher import FileNameFetcher
from connector import  Connector
from file_arrangement import FileArrangement


def main(location, proxy):
    file_code_result = FileNameFetcher().videos_list_fetch(location['src'])
    _connector = Connector()
    _file_arrangement = FileArrangement(_connector)
    for code in file_code_result:
        # print(code)
        info = _connector.info_getter(code['file_code'], code['file_path'], code['file_name'])
        # print('info:' + str(info))
        if info:
            _file_arrangement.file_move(info, location['dst'])
