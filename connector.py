import socket
import urllib.request
import urllib.error
import matcher


class Connector:

    __proxy_ip = ''
    __proxy_port = ''
    __proxy_user = ''
    __proxy_password = ''
    __proxy_switch = False
    __proxy_protocal = ''
    __proxy_addr = ''
    __web_addr_stable = 'http://www.ojcfdofzbk9yik290l.com/'    # 'https://www.ojcfdofzbk9yik290l.com/ '
    __web_addr_backup = 'http://www.buscdn.pw/'                # 'https://www.buscdn.pw/'
    __user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 ' \
                   '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'

    __time_out_limit = 10
    __retry_flag = 0
    __retry_max = 3

    __headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,en;q=0.',
        'Cache-Control': 'max-age=0',
        'User-Agent': __user_agent,
        'Connection': 'keep-alive',
        'Referer': __web_addr_backup
    }

    def __init__(self, ip='127.0.0.1', port=8087, user='', password='', switch=False, protocal='http'):
        self.__proxy_ip = ip
        self.__proxy_port = port
        self.__proxy_user = user
        self.__proxy_password = password
        self.__proxy_switch = switch
        self.__proxy_protocal = protocal
        self.__proxy_addr = self.__proxy_user + ':' + \
                            self.__proxy_password + '@' + \
                            self.__proxy_ip + ':' + str(self.__proxy_port)
        # print(self.__proxy_addr)
        self.__proxy_init()

    def __proxy_init(self):
        proxy_on = urllib.request.ProxyHandler({self.__proxy_protocal: self.__proxy_addr})
        proxy_off = urllib.request.ProxyHandler({})

        if self.__proxy_switch:
            proxy_opener = urllib.request.build_opener(proxy_on)
        else:
            proxy_opener = urllib.request.build_opener(proxy_off)

        urllib.request.install_opener(proxy_opener)

    def proxy_test(self):
        try:
            req = urllib.request.Request('https://www.google.com', data=None, headers=self.__headers)
            urllib.request.urlopen(req, timeout=self.__time_out_limit).read().decode('utf-8')
        except:
            return False
        else:
            return True

    def info_getter(self, video_code, file_path, file_name, url_choose=0):
        raw_info = self.__proxy_using(video_code, url_choose)
        # print('raw_info is ' + str(raw_info))
        if raw_info:
            # if raw_info == 404:
            #     self.info_getter(video_code, file_path, file_name, file_format, url_choose=1)
            result = matcher.Matcher().info_matcher(video_code, file_path, file_name, raw_info)
            # print(result)
            return result

    def __proxy_using(self, video_code, url_choose=0):
        url_list = [self.__web_addr_stable + video_code.upper(), self.__web_addr_backup + video_code.upper()]

        # TODO A /'try except/' is needed to make sure the software can work properly.
        raw_info_response = ''
        try:
            raw_info_response = self.__get_response(url_list[url_choose])

        except urllib.error.HTTPError as http_error:
            print('http error!!!!!!', http_error)
            if str(http_error) == 'HTTP Error 404: Not Found':
                print('目前认为是没有这个番号' + video_code)
            return
        except urllib.error.URLError as url_error:
            print('url error!!!!!!', url_error)
            if str(url_error) == '<urlopen error timed out>':
                print('目前认为是翻墙失败')
                return
            elif '<urlopen error [WinError 10061]'in str(url_error):
                print('代理服务器没开')
                return
            elif '<urlopen error [Errno 11001]' in str(url_error):
                print('没有网络连接')
                return
            else:
                if self.__retry_flag <= self.__retry_max:
                    self.__proxy_using(video_code, url_choose)
                    self.__retry_flag += 1
        except Exception as e:
            print('other exception, ' + str(e))
            if self.__retry_flag <= self.__retry_max:
                self.__proxy_using(video_code, url_choose)
                self.__retry_flag += 1
            return

        return raw_info_response

    def __get_response(self, url):
        req = urllib.request.Request(url, data=None, headers=self.__headers)
        raw_info_response = urllib.request.urlopen(req, timeout=self.__time_out_limit).read().decode('utf-8')
        return raw_info_response

    def cover_image_download(self, info, dst):
        print(dst + 'jpg')
        try:
            req = urllib.request.Request(info['cover_image'], data=None, headers=self.__headers)
            image_temp = urllib.request.urlopen(req, timeout=self.__time_out_limit).read()
            image_file = open(dst + 'jpg', 'wb')
            image_file.write(image_temp)
        except urllib.error.HTTPError as http_error:
            print('http error cover_image', info['cover_image'], http_error)
        except urllib.error.URLError as url_error:
            print('url error cover image', info['cover_image'], url_error)
        except IOError as io_error:
            print('File open error')
        else:
            image_file.close()

#
# ph = Connector(ip='127.0.0.1', port=8089, switch=False)
# # print(ph.proxy_test())
# # ph.proxy_using('ipx-100')
# ph.info_getter('ipx-100')
