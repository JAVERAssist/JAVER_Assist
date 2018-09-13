import os
import shutil
import re


class FileArrangement:

    def __init__(self, connector):
        self.__connector = connector

    def file_move(self, info, dst):
        dst = dst.strip()
        # print(dst)
        if not self.__dst_dic_create(dst):
            print('输出路径不存在，请修改')
            return

        if dst[-2:] != r'\\':
            dst += r'\\'
        # print(dst)

        if info['actors']:
            if not os.path.exists(dst + info['actors'][0]):
                os.mkdir(dst + info['actors'][0])

            dst = dst + info['actors'][0] + r'\\' + info['release_date'] + ' - ' + info['title'] + r'.'
            shutil.move(
                info['file_path'],
                dst + info['file_format']
            )
            self.__connector.cover_image_download(info, dst)
        else:
            if not os.path.exists(dst + '未知女优'):
                os.mkdir(dst + '未知女优')

            dst = dst + '未知女优' + r'\\' + info['release_date'] + ' - ' + info['title'] + r'.'
            shutil.move(
                info['file_path'],
                dst + info['file_format']
            )

    def __dst_dic_create(self, dst):
        # TODO: The disk flag needs to be distinguished if it is exists.
        dst_pattern = r'\\'
        dst_dic_parts = re.split(dst_pattern, dst)
        disk_flag = dst_dic_parts.pop(0)

        if os.path.exists(disk_flag):
            dst_dic = disk_flag
        else:
            return False
        # print(dst_dic_parts)
        dst_dic_parts = list(filter(lambda item: item, dst_dic_parts))
        # print(dst_dic_parts)
        if dst_dic_parts:
            for dst_dic_part in dst_dic_parts:
                dst_dic += dst_dic_part + r'\\'
                if not os.path.exists(dst_dic):
                    os.mkdir(dst_dic)
        return True


# if __name__ == '__main__':
#     info = {
#         'actors': ['跡美しゅり'],
#         'file_path': 'G:\\test\\[2016-03-17] - [SVDVD-530] - [ビッグバンローター!自分から腰を振って、野外潮吹きをオネダリしてくる露出願望娘 跡美しゅり].avi',
#         'title': 'SVDVD-530 ビッグバンローター！自分から腰を振って、野外潮吹きをオネダリしてくる露出願望娘 跡美しゅり',
#         'file_format': r'avi',
#         'release_date': r'2016-03-17'
#     }
#     dst = 'G:\\test2\\'
#     # FileArrangement().file_move(info, dst)
#     FileArrangement().file_move(info, dst)
