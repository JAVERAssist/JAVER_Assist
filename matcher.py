#! /usr/lib/python
# -*- coding: utf-8 -*-

import re


class Matcher:

    def code_matcher(self, root, file_names):
        """

        :param root: The path of the file.
        :param file_names: A list contains all the video names in the same directory.
        :return:
        """
        code_match_pattern1 = '[a-zA-Z]{2,5}[-_][0-9]{3,5}'
        code_match_pattern2 = '([a-zA-Z]{2,5})([0-9]{3,5})'

        file_code_results = []

        re_rules1 = re.compile(code_match_pattern1, flags=re.IGNORECASE)
        re_rules2 = re.compile(code_match_pattern2, flags=re.IGNORECASE)
        # print(file_names)
        for file_name in file_names:
            file_code1 = re_rules1.findall(file_name)
            file_code2 = re_rules2.findall(file_name)
            if file_code1:
                file_code = file_code1[0].upper()
                root_path = root + file_name
                # print(root_path)
                # print('success: ', file_code, file_name, root)
                file_info = {
                    'file_code': file_code,
                    'file_name': file_name,
                    'file_path': root_path,
                }
                file_code_results.append(file_info)
            elif file_code2:
                # print(file_code2[0])
                file_code = file_code2[0][0].upper() + '-' + file_code2[0][1]
                root_path = root + file_name
                # print('success2: ', file_code, file_name)
                file_info = {
                    'file_code': file_code,
                    'file_name': file_name,
                    'file_path': root_path,
                }
                file_code_results.append(file_info)
            else:
                print('fail: ', file_name)
        # print(file_code_results)
        return file_code_results

    def info_matcher(self, code, file_path, file_name, raw_info_response):
        """
        From the html file, getting useful information.
        :param code: The code of the video.
        :param file_path: The src path of the video file
        :param file_name: The name of the src video file
        :param raw_info_response: Used to receive the content of the website.
        :return: A dict contains title, code, [actors], [date], [length], [director], [studio], [publisher], [series]
        """

        info_dic = {}
        video_format_pattern = '\.(mkv|avi|mp4|asf|mpg|mpeg|dat|vob|ogm|3gp|rm|rmvb|flv|swf|mov|m4v)$'
        cover_image_pattern = '<a class="bigImage" href="(.*?)">'
        title_pattern = '<div class="container">\s*<h3>(.*?)</h3>'
        release_date_pattern = '<p>\s*<span class="header">發行日期:</span>\s?(.*?)</p>'
        length_pattern = '<p>\s*<span class="header">長度:</span>\s?(.*?)分鐘</p>'
        director_pattern = '<p>\s*<span class="header">導演:</span>\s*<a href=".*?">(.*?)</a></p>'
        producer_pattern = '<p>\s*<span class="header">製作商:</span>\s*<a href=".*?">(.*?)</a>'
        publisher_pattern = '<p>\s*<span class="header">發行商:</span>\s*<a href=".*?">(.*?)</a>'
        series_pattern = '<p>\s*<span class="header">系列:</span>\s*<a href=".*?">(.*?)</a>'
        actors_pattern = '<div class="star-name">\s*<a href=".*?" title="(.*?)">'

        # Get video format
        re_video_format_pattern = re.compile(video_format_pattern, flags=re.IGNORECASE)
        video_format_list = re_video_format_pattern.findall(file_name)

        # Get cover image url
        re_cover_image_pattern = re.compile(cover_image_pattern, flags=re.IGNORECASE)
        cover_image_content_list = re_cover_image_pattern.findall(raw_info_response)

        # Get movie title, contains code, title and [actor]
        re_title_pattern = re.compile(title_pattern, flags=re.IGNORECASE)
        title_content_list = re_title_pattern.findall(raw_info_response)

        # Get Release date
        re_release_date = re.compile(release_date_pattern, flags=re.IGNORECASE)
        release_date_list = re_release_date.findall(raw_info_response)

        # Get length
        re_length_pattern = re.compile(length_pattern, flags=re.IGNORECASE)
        length_list = re_length_pattern.findall(raw_info_response)

        # Get director
        re_director_pattern = re.compile(director_pattern, flags=re.IGNORECASE)
        director_list = re_director_pattern.findall(raw_info_response)

        # Get producer
        re_producer_pattern = re.compile(producer_pattern, flags=re.IGNORECASE)
        producer_list = re_producer_pattern.findall(raw_info_response)

        # Get publisher
        re_publisher_pattern = re.compile(publisher_pattern, flags=re.IGNORECASE)
        publisher_list = re_publisher_pattern.findall(raw_info_response)

        # Get series
        re_series_pattern = re.compile(series_pattern, flags=re.IGNORECASE)
        series_list = re_series_pattern.findall(raw_info_response)

        # Get actors
        re_actors_pattern = re.compile(actors_pattern, flags=re.IGNORECASE)
        actors_list = re_actors_pattern.findall(raw_info_response)

        info_dic['code'] = code
        info_dic['file_path'] = file_path
        info_dic['file_name'] = file_name
        info_dic['file_format'] = video_format_list[0]
        info_dic['cover_image'] = cover_image_content_list[0]
        info_dic['title'] = title_content_list[0]
        info_dic['release_date'] = release_date_list[0] if release_date_list else None
        info_dic['length'] = length_list[0] if length_list else None
        info_dic['director'] = director_list[0] if director_list else None
        info_dic['producer'] = producer_list[0] if producer_list else None
        info_dic['publisher'] = publisher_list[0] if publisher_list else None
        info_dic['series'] = series_list[0] if series_list else None
        info_dic['actors'] = actors_list if actors_list else None

        return info_dic
