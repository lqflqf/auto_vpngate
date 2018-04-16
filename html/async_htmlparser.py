import json
import requests
from pyquery import PyQuery
import os
from multiprocessing import Pool
import itertools
import pathlib
import time
import asyncio
import aiohttp


class Config:

    def __init__(self, config_path='config.json'):
        with open(config_path, 'r') as f:
            self.__config_dic__ = json.load(f)

    @property
    def urls(self):
        return self.__config_dic__['urls']

    @property
    def countries(self):
        return self.__config_dic__['countries']

    @property
    def protocols(self):
        return self.__config_dic__['protocol']

    @property
    def timeout(self):
        return self.__config_dic__['timeout']

    @property
    def retry(self):
        return self.__config_dic__['retry']

    @property
    def session_no(self):
        return self.__config_dic__['session number']

    @property
    def bandwidth(self):
        return self.__config_dic__['bandwidth']

    @property
    def save_path(self):
        return self.__config_dic__['save_path']

class VgRow:

    __nl__ = '\n'
    __eq_sign__ = '='

    def __init__(self, url: str, pq_obj: PyQuery):
        self.url = url
        self.country = pq_obj.children().eq(0).text()
        self.session_no = self.__to_int__(pq_obj.children().eq(2).text().split(self.__nl__)[0].split()[0])
        self.alive_days = self.__to_int__(pq_obj.children().eq(2).text().split(self.__nl__)[1].split()[0])
        self.bandwidth = self.__to_float__(pq_obj.children().eq(3).text().split(self.__nl__)[0].split()[0])
        self.ping = self.__to_int__(pq_obj.children().eq(3).text().split(self.__nl__)[1].split()[1])

        hrefl = pq_obj.children().eq(6).find('a').attr('href').split('?')[1].split('&')

        self.ip = hrefl[1].split(self.__eq_sign__)[1]
        self.tcp = hrefl[2].split(self.__eq_sign__)[1]
        self.udp = hrefl[3].split(self.__eq_sign__)[1]
        self.sid = hrefl[4].split(self.__eq_sign__)[1]
        self.hid = hrefl[5].split(self.__eq_sign__)[1]
        self.link = None

    def __to_int__(self, str):
        try:
            r = int(str)
        except ValueError:
            r = -1
        return r

    def __to_float__(self, str):
        try:
            r = float(str)
        except ValueError:
            r = -1.0
        return r

    def getLink(self):
        if self.link is None:
            self.link = []
            if self.tcp != '0':
                self.link.append(VgLink('tcp', self))
            if self.udp != '0':
                self.link.append(VgLink('udp', self))

        return self.link

class VgLink:

    __location__ = '/common/openvpn_download.aspx'

    def __init__(self, protocol, vgrow_obj):
        self.protocol = protocol
        self.vgrow = vgrow_obj

        self.params =  {
            'sid': self.vgrow.sid,
            'host': self.vgrow.ip,
            'hid': self.vgrow.hid
        }
        if self.protocol == 'tcp':
            self.params['tcp'] = '1'
            self.params['port'] = self.vgrow.tcp
        else:
            self.params['udp'] = '1'
            self.params['port'] = self.vgrow.udp

        self.filename = self.vgrow.country + '_' + self.vgrow.ip + '_' + self.protocol + '_' +\
                        self.params['port'] + '.ovpn'

        self.url = self.vgrow.url + self.__location__


class HtmlParser:
    __lang__ = '/en/'
    __tab_id__ = 'table#vg_hosts_table_id'
    __tab_data_cls0__ = 'vg_table_row_0'
    __tab_data_cls1__ = 'vg_table_row_1'
    __tab_header_cls__ = 'vg_table_header'
    __form_data__ = {
        "__VIEWSTATE": "/wEPDwULLTE1ODQzMDg1NDMPZBYCAgEPZBYKZg8PFgIeBFRleHQF1AFZb3VyIElQOiAyMTAuMTMyLjE1MS4xNTMuYXAuZHRpLm5lLmpwICgxNTMuMTUxLjEzMi4yMTApPEJSPjxpbWcgc3JjPScuLi9pbWFnZXMvZmxhZ3MvSlAucG5nJyB3aWR0aD0nMzInIGhlaWdodD0nMzInIC8+PEJSPllvdXIgY291bnRyeTogSmFwYW48QlI+PGEgaHJlZj0nI0xJU1QnPkxldCdzIGNoYW5nZSB5b3VyIElQIGFkZHJlc3MgYnkgdXNpbmcgVlBOIEdhdGUhPC9hPmRkAgEPDxYCHwAFYzxiPlRvZGF5OiAxLDM1MCw3MjggY29ubmVjdGlvbnMsIEN1bXVsYXRpdmU6IDMsODk0LDQyMyw1MDYgY29ubmVjdGlvbnMsIFRyYWZmaWM6IDEwNCw4MjguNjMgVEIuPC9iPmRkAgMPDxYCHwAFBTMsMTA2ZGQCBA8PFgIfAAU4PGI+Myw4OTQsNDIzLDUwNiBWUE4gY29ubmVjdGlvbnMgZnJvbSAyMzMgQ291bnRyaWVzLjwvYj5kZAIGDw8WAh8ABQQ3MTY2ZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgQFC0NfU29mdEV0aGVyBQZDX0wyVFAFCUNfT3BlblZQTgUGQ19TU1RQNnRU35SW9+iAX1zUgCT5Wglx0zNUdzN1b/QtfmMosms=",
        "__VIEWSTATEGENERATOR": "1A8A0CA9",
        "__EVENTVALIDATION": "/wEdAAeSJ4zco66jEJfXkVLyEXnWZSmLidaMQ3gg2jFmkkuEoSCbR2H52ATFMg5mk6aQHX3LISMg9/mywZPt3Ki4BVA7RhcLWIOHmHJ6h2VtXvwLieWw6g9beu/2J/0raZOGI2E/WMskeKo19Gyidl+m11dTQ4jHStBhHAmWMfq++a085mllmWeyjqtOosslKzVL2wQ=",
        "C_OpenVPN": "on"
        }

    def __init__(self, config: Config):
        self.__honfig__ = config

        self.__path_obj__ = self.__create_folder__()

    async def get(self, url, params=None):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=self.__honfig__.timeout, params=params) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        return None
        except aiohttp.ClientError as e:
            print(e)
            return None


    async def post(self, url, msg_body):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, timeout=self.__honfig__.timeout, data=msg_body) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        return None
        except aiohttp.ClientError as e:
            print(e)
            return None

    def __is_row_selected__(self, e: VgRow):
        return e.country in self.__honfig__.countries and \
               e.session_no > self.__honfig__.session_no and \
               e.bandwidth > self.__honfig__.bandwidth

    def __is_link_selected__(self, e: VgLink):
        return e.protocol in self.__honfig__.protocols

    @staticmethod
    def __is_not_none__(e):
        return True if e is not None else False

    async def __url_to_html__(self, url):
        return url, await self.post(url + self.__lang__, self.__form_data__)

    async def __html_to_rowlist__(self, url, html):
        tabrow = PyQuery(html).find(self.__tab_id__).eq(2).find('tr')
        return [VgRow(url, r) for r in tabrow.items() if \
                r.children().hasClass(self.__tab_data_cls0__) \
                or r.children().hasClass(self.__tab_data_cls1__)]

    async def __row_to_link__(self, vgrow: VgRow):
        if self.__is_row_selected__(vgrow):
            return list(filter(self.__is_link_selected__, vgrow.getLink()))


    async def __link_to_file__(self, vglink: VgLink):
        response = await self.get(vglink.url, vglink.params)
        if response is not None:
            with (self.__path_obj__ / vglink.filename).open(mode='w') as fw:
                n = fw.write(response)
        else:
            n = 0
        return n


    def __create_folder__(self):
        p = pathlib.Path(self.__honfig__.save_path)
        p.mkdir(exist_ok=True)
        q = p / time.asctime().replace(':', '')
        q.mkdir(exist_ok=True)
        return q

    def process_async(self):

        now = time.time()

        loop = asyncio.get_event_loop()

        tasks = [self.__url_to_html__(u) for u in self.__honfig__.urls]

        htmls = filter(lambda e: e[1] is not None, loop.run_until_complete(asyncio.gather(*tasks)))

        tasks = [self.__html_to_rowlist__(u, h) for u, h in htmls]

        rows = itertools.chain.from_iterable(loop.run_until_complete(asyncio.gather(*tasks)))

        tasks = [self.__row_to_link__(r) for r in rows]

        links = itertools.chain.from_iterable(filter(lambda e: e is not None, loop.run_until_complete(asyncio.gather(*tasks))))

        tasks = [self.__link_to_file__(l) for l in links]

        fn = loop.run_until_complete(asyncio.gather(*tasks))

        loop.close()

        print(fn)

        print(time.time() - now)



if __name__ == '__main__':

    c = Config()

    p = HtmlParser(c)

    p.process_async()







