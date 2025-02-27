import pyquery
import itertools
import asyncio
import aiohttp
import configuration
import prettytable


class VgRow:
    __nl__ = '\n'
    __eq_sign__ = '='

    def __init__(self, url: str, pq_obj: pyquery.PyQuery):
        self.url = url
        self.country = pq_obj.children().eq(0)('img').attr('src').split('/')[-1].split('.')[0]
        self.session_number = self.__to_int__(pq_obj.children().eq(2).text().split(self.__nl__)[0].split()[0])
        self.alive_days = self.__to_int__(pq_obj.children().eq(2).text().split(self.__nl__)[1].split()[0])
        self.bandwidth = self.__to_float__(pq_obj.children().eq(3).text().split(self.__nl__)[0].split()[0])
        self.ping = self.__to_int__(pq_obj.children().eq(3).text().split(self.__nl__)[1].split()[1])
        self.score = pq_obj.children().eq(9).text().replace(',', '')

        href_list = pq_obj.children().eq(6)('a').attr('href').split('?')[1].split('&')

        self.ip = href_list[1].split(self.__eq_sign__)[1]
        self.tcp = href_list[2].split(self.__eq_sign__)[1]
        self.udp = href_list[3].split(self.__eq_sign__)[1]
        self.sid = href_list[4].split(self.__eq_sign__)[1]
        self.hid = href_list[5].split(self.__eq_sign__)[1]
        self.link = None

    @staticmethod
    def __to_int__(s):
        try:
            r = int(s)
        except ValueError:
            r = -1
        return r

    @staticmethod
    def __to_float__(s):
        try:
            r = float(s)
        except ValueError:
            r = -1.0
        return r

    def get_link(self):
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

        self.params = {
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

        self.filename = self.vgrow.country + '_' + self.vgrow.ip + '_' + self.protocol + '_' + \
                        self.params['port'] + '_' + self.vgrow.score + '.ovpn'

        self.url = self.vgrow.url + self.__location__


class HtmlScraper:
    __lang__ = '/en/'
    __tab_id__ = 'table#vg_hosts_table_id'
    __tab_data_cls0__ = 'vg_table_row_0'
    __tab_data_cls1__ = 'vg_table_row_1'
    __tab_header_cls__ = 'vg_table_header'

    def __init__(self, config):
        self.__config__: configuration.Configuration = config

        # self.__path_obj__ = self.__create_folder__()

    async def get(self, url, params=None):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=self.__config__.timeout, params=params) as response:
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
                async with session.post(url, timeout=self.__config__.timeout, data=msg_body) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        return None
        except aiohttp.ClientError as e:
            print(e)
            return None

    def __is_row_selected__(self, e: VgRow):
        return e.country in self.__config__.country and \
            e.session_number > self.__config__.session_number and \
            e.bandwidth > self.__config__.bandwidth

    def __is_link_selected__(self, e: VgLink):
        return e.protocol in self.__config__.protocol

    @staticmethod
    def __is_not_none__(e):
        return True if e is not None else False

    @staticmethod
    def __add_data_ciphers__(s: str) -> str:
        s1, s2, s3 = s.partition('cipher AES-128-CBC\r\n')
        new_line = 'data-ciphers ' + s2.split(' ')[1]
        return s1 + s2 + new_line + s3

    async def __url_to_html__(self, url, mode='openvpn'):
        html = await self.get(url + self.__lang__)
        pq = pyquery.PyQuery(html)

        v1 = pq('input#__VIEWSTATE').attr('value')
        v2 = pq('input#__VIEWSTATEGENERATOR').attr('value')
        v3 = pq('input#__EVENTVALIDATION').attr('value')

        form_data = {'__VIEWSTATE': v1, '__VIEWSTATEGENERATOR': v2, '__EVENTVALIDATION': v3}

        if mode == 'l2tp':
            form_data['C_L2TP'] = 'on'
        else:
            form_data['C_OpenVPN'] = 'on'

        return url, await self.post(url + self.__lang__, form_data)

    async def __html_to_row_list__(self, url, html):
        tabrow = pyquery.PyQuery(html)(self.__tab_id__).eq(2)('tr')
        return [VgRow(url, r) for r in tabrow.items() if \
                r.children().hasClass(self.__tab_data_cls0__) \
                or r.children().hasClass(self.__tab_data_cls1__)]

    async def __row_to_link__(self, vgrow: VgRow):
        if self.__is_row_selected__(vgrow):
            return list(filter(self.__is_link_selected__, vgrow.get_link()))

    async def __link_to_file__(self, vglink: VgLink, sem: asyncio.Semaphore):
        async with sem:
            file = await self.get(vglink.url, vglink.params)
            return vglink.filename, self.__add_data_ciphers__(file)

    async def __get_l2tp_list__(self, url):
        html_tuple = await self.__url_to_html__(url, mode='l2tp')
        tabrow = pyquery.PyQuery(html_tuple[1])(self.__tab_id__).eq(2)('tr')
        tablist = [r for r in tabrow.items() if \
                   r.children().hasClass(self.__tab_data_cls0__) \
                   or r.children().hasClass(self.__tab_data_cls1__)]

        l2tp_list = []

        for i in tablist:
            c = i.children()
            country = c.eq(0).text()
            ip = c.eq(1).text().split('\n')[1]
            sessions, uptime = c.eq(2).text().split('\n')[:2]
            sessions = sessions.split(' ')[0]
            bandwidth, ping = c.eq(3).text().split('\n')[:2]
            bandwidth = bandwidth.split(' Mbps')[0]
            ping = ping.split(': ')[1]
            ping = ping.split(' ms')[0]
            score = c.eq(9).text()
            l2tp_list.append([country, ip, sessions, uptime, bandwidth, ping, score])

        return l2tp_list

    @staticmethod
    def __format_l2tp_list__(l2tp_list):
        output_table = prettytable.PrettyTable()
        output_table.title = 'L2TP servers'
        output_table.field_names = ["CNTY", "IPAD", "Sess", "Uptime", "BW(Mbps)", "Ping(ms)", "Score"]
        output_table.add_rows(l2tp_list)
        output_table.hrules = prettytable.ALL
        return output_table.get_html_string(format=True)

    def process_async(self):

        loop = asyncio.new_event_loop()

        asyncio.set_event_loop(loop)

        sem = asyncio.Semaphore(self.__config__.concurrency_number)

        tasks = [self.__url_to_html__(self.__config__.url)]

        html = filter(lambda e: e[1] is not None, loop.run_until_complete(asyncio.gather(*tasks)))

        tasks = [self.__html_to_row_list__(u, h) for u, h in html]

        rows = itertools.chain.from_iterable(loop.run_until_complete(asyncio.gather(*tasks)))

        tasks = [self.__row_to_link__(r) for r in rows]

        links = itertools.chain.from_iterable(
            filter(lambda e: e is not None, loop.run_until_complete(asyncio.gather(*tasks))))

        tasks = [self.__link_to_file__(l, sem) for l in links]

        files = loop.run_until_complete(asyncio.gather(*tasks))

        # get l2tp list
        tasks = [self.__get_l2tp_list__(self.__config__.url)]

        l2tp_list = loop.run_until_complete(asyncio.gather(*tasks))[0]

        ascii_table = self.__format_l2tp_list__(l2tp_list)

        loop.close()

        return list(filter(lambda i: i[1] is not None, files)), ascii_table
