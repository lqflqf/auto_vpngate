import json
import requests
from pyquery import PyQuery
import os

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
    def save_path(self):
        return self.__config_dic__['save_path']

class VgRow:

    __nl__ = '\n'
    __eq_sign__ = '='
    __location__ = '/common/openvpn_download.aspx'

    def __init__(self, url: str, pq_obj: PyQuery):
        self.__url__ = url
        self.__country__ = pq_obj.children().eq(0).text()
        self.__session_no__ = self.__to_int__(pq_obj.children().eq(2).text().split(self.__nl__)[0].split()[0])
        self.__alive_days__ = self.__to_int__(pq_obj.children().eq(2).text().split(self.__nl__)[1].split()[0])
        self.__bandwidth__ = self.__to_float__(pq_obj.children().eq(3).text().split(self.__nl__)[0].split()[0])
        self.__ping__ = self.__to_int__(pq_obj.children().eq(3).text().split(self.__nl__)[1].split()[1])

        hrefl = pq_obj.children().eq(6).find('a').attr('href').split('?')[1].split('&')

        self.__ip__ = hrefl[1].split(self.__eq_sign__)[1]
        self.__tcp__ = hrefl[2].split(self.__eq_sign__)[1]
        self.__udp__ = hrefl[3].split(self.__eq_sign__)[1]
        self.__sid__ = hrefl[4].split(self.__eq_sign__)[1]
        self.__hid__ = hrefl[5].split(self.__eq_sign__)[1]
        self.__udp_params__ = {
            'sid': self.__sid__,
            'host': self.__ip__,
            'hid': self.__hid__,
            'udp': '1',
            'port': self.__udp__
        }
        self.__tcp_params__ = {
            'sid': self.__sid__,
            'host': self.__ip__,
            'hid': self.__hid__,
            'tcp': '1',
            'port': self.__tcp__
        }

        self.__filename__ = self.__ip__ + '_' + self.__udp__ + '.ovpn'

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

    def get_udp_file(self):
        try:
            r = requests.get(self.__url__ + self.__location__, params=self.__udp_params__)
            if r.status_code == 200:
                return r.content
        except requests.exceptions.RequestException:
            pass

        return None

    def get_tcp_file(self):
        try:
            r = requests.get(self.__url__ + self.__location__, params=self.__tcp_params__)
            if r.status_code == 200:
                return r.content
        except requests.exceptions.RequestException:
            pass

        return None

    @property
    def filename(self):
        return self.__filename__

    @property
    def country(self):
        return self.__country__




class HtmlParser:

    __lang__ = '/en/'

    def __init__(self, config: Config):
        self.__honfig__ = config
        self.__html__ = []
        self.__rows__ = []

    def __get_html__(self):
        form_data = {"__VIEWSTATE":"/wEPDwULLTE1ODQzMDg1NDMPZBYCAgEPZBYKZg8PFgIeBFRleHQF1AFZb3VyIElQOiAyMTAuMTMyLjE1MS4xNTMuYXAuZHRpLm5lLmpwICgxNTMuMTUxLjEzMi4yMTApPEJSPjxpbWcgc3JjPScuLi9pbWFnZXMvZmxhZ3MvSlAucG5nJyB3aWR0aD0nMzInIGhlaWdodD0nMzInIC8+PEJSPllvdXIgY291bnRyeTogSmFwYW48QlI+PGEgaHJlZj0nI0xJU1QnPkxldCdzIGNoYW5nZSB5b3VyIElQIGFkZHJlc3MgYnkgdXNpbmcgVlBOIEdhdGUhPC9hPmRkAgEPDxYCHwAFYzxiPlRvZGF5OiAxLDM1MCw3MjggY29ubmVjdGlvbnMsIEN1bXVsYXRpdmU6IDMsODk0LDQyMyw1MDYgY29ubmVjdGlvbnMsIFRyYWZmaWM6IDEwNCw4MjguNjMgVEIuPC9iPmRkAgMPDxYCHwAFBTMsMTA2ZGQCBA8PFgIfAAU4PGI+Myw4OTQsNDIzLDUwNiBWUE4gY29ubmVjdGlvbnMgZnJvbSAyMzMgQ291bnRyaWVzLjwvYj5kZAIGDw8WAh8ABQQ3MTY2ZGQYAQUeX19Db250cm9sc1JlcXVpcmVQb3N0QmFja0tleV9fFgQFC0NfU29mdEV0aGVyBQZDX0wyVFAFCUNfT3BlblZQTgUGQ19TU1RQNnRU35SW9+iAX1zUgCT5Wglx0zNUdzN1b/QtfmMosms=",
                     "__VIEWSTATEGENERATOR":"1A8A0CA9",
                     "__EVENTVALIDATION":"/wEdAAeSJ4zco66jEJfXkVLyEXnWZSmLidaMQ3gg2jFmkkuEoSCbR2H52ATFMg5mk6aQHX3LISMg9/mywZPt3Ki4BVA7RhcLWIOHmHJ6h2VtXvwLieWw6g9beu/2J/0raZOGI2E/WMskeKo19Gyidl+m11dTQ4jHStBhHAmWMfq++a085mllmWeyjqtOosslKzVL2wQ=",
                     "C_OpenVPN":"on"
                     }

        for u in self.__honfig__.urls:
            try:
                r = requests.post(u + self.__lang__, data=form_data, timeout=self.__honfig__.timeout)
                if r.status_code == 200:
                    self.__html__.append((u, r.text))
            except requests.exceptions.RequestException:
                continue

    def __get_dl_links__(self):
        tab_id = 'table#vg_hosts_table_id'
        tab_data_cls0 = 'vg_table_row_0'
        tab_data_cls1 = 'vg_table_row_1'
        tab_header_cls = 'vg_table_header'

        for u, h in self.__html__:
            tabq = PyQuery(h).find(tab_id).eq(2).find('tr')
            for r in tabq.items():
                if r.children().hasClass(tab_data_cls0) or r.children().hasClass(tab_data_cls1):
                    self.__rows__.append(VgRow(u, r))

    def process(self):
        self.__get_html__()
        self.__get_dl_links__()

        for r in filter(lambda e: e.country in self.__honfig__.countries, self.__rows__):
            with open(os.path.join(self.__honfig__.save_path, r.filename), 'wb') as f:
                fc = r.get_udp_file()
                if fc is not None:
                    f.write(r.get_udp_file())
                f.close()



if __name__ == '__main__':
    c = Config()
    print(c.urls)
    print(c.countries)
    print(c.protocols)
    print(str(c.timeout))
    print(str(c.retry))
    print(c.save_path)

    p = HtmlParser(c)
    p.process()







