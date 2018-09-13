#! /usr/lib/python
# -*- coding: utf-8 -*-

import os
import re
from matcher import Matcher
from connector import Connector
from file_arrangement import FileArrangement


class FileNameFetcher:

    __video_file_pattern = '\.(mkv|avi|mp4|asf|mpg|mpeg|dat|vob|ogm|3gp|rm|rmvb|flv|swf|mov|m4v)$'

    def videos_list_fetch(self, root_dir):
        """
        The method is used to fetch all the files' name and screens out all the video files.
        :param root_dir: The root directory of all the video contains.
        :return: video_file_name_list: Each loop returns a list contains all the videos in the same subdirectory.
        """
        # TODO The instance needs to be move outside.
        file_code_results = []
        _code_matcher = Matcher()
        for root, sub_dirs, files in os.walk(root_dir):
            video_file_name_list = list(filter(self.__video_file_filter, files))
            if video_file_name_list:
                # yield video_file_name_list
                # print('a')
                file_code_results_part = _code_matcher.code_matcher(root+'\\', video_file_name_list)
                file_code_results += file_code_results_part

        # print(file_code_results, len(file_code_results))
        return file_code_results

    def __video_file_filter(self, file_name):
        """
        The method is used to provide a filter mechanism to method videos_list_fetch
        :param file_name: The method filter() send a file name to __video_file_filter.
        :return: A video file name.
        """
        re_rules = re.compile(self.__video_file_pattern, flags=re.IGNORECASE)

        if re_rules.findall(file_name):
            # print(re_rules.findall(file_name))
            return file_name


# if __name__ == '__main__':
#     file_code_result = FileNameFetcher().videos_list_fetch(r'G:\test')
#     _connector = Connector()
#     _file_arrangement = FileArrangement(_connector)
#     for code in file_code_result:
#         # print(code)
#         info = _connector.info_getter(code['file_code'], code['file_path'], code['file_name'])
#         # print('info:' + str(info))
#         if info:
#             _file_arrangement.file_move(info, r'G:\\test2')
