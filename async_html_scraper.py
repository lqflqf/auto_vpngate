import asyncio
import itertools
import logging

import aiohttp
import prettytable
import pyquery

import configuration

logger = logging.getLogger(__name__)


class VgRow:
    _nl = "\n"
    _eq_sign = "="

    def __init__(self, url: str, pq_obj: pyquery.PyQuery):
        self.url = url
        src = pq_obj.children().eq(0)("img").attr("src")
        self.country = src.split("/")[-1].split(".")[0] if src else "unknown"
        self.session_number = self._to_int(pq_obj.children().eq(2).text().split(self._nl)[0].split()[0])
        self.alive_days = self._to_int(pq_obj.children().eq(2).text().split(self._nl)[1].split()[0])
        self.bandwidth = self._to_float(pq_obj.children().eq(3).text().split(self._nl)[0].split()[0])
        self.ping = self._to_int(pq_obj.children().eq(3).text().split(self._nl)[1].split()[1])
        self.score = pq_obj.children().eq(9).text().replace(",", "")

        href = pq_obj.children().eq(6)("a").attr("href")
        if href is None:
            raise ValueError("Missing href in VgRow — unexpected table structure")
        href_list = href.split("?")[1].split("&")

        self.ip = href_list[1].split(self._eq_sign)[1]
        self.tcp = href_list[2].split(self._eq_sign)[1]
        self.udp = href_list[3].split(self._eq_sign)[1]
        self.sid = href_list[4].split(self._eq_sign)[1]
        self.hid = href_list[5].split(self._eq_sign)[1]
        self.link: list[VgLink] | None = None

    @staticmethod
    def _to_int(s: str) -> int:
        try:
            return int(s)
        except ValueError:
            return -1

    @staticmethod
    def _to_float(s: str) -> float:
        try:
            return float(s)
        except ValueError:
            return -1.0

    def get_link(self) -> list[VgLink]:
        if self.link is None:
            self.link = []
            if self.tcp != "0":
                self.link.append(VgLink("tcp", self))
            if self.udp != "0":
                self.link.append(VgLink("udp", self))
        return self.link


class VgLink:
    _location = "/common/openvpn_download.aspx"

    def __init__(self, protocol: str, vgrow_obj: VgRow):
        self.protocol = protocol
        self.vgrow = vgrow_obj

        self.params = {
            "sid": self.vgrow.sid,
            "host": self.vgrow.ip,
            "hid": self.vgrow.hid,
        }
        if self.protocol == "tcp":
            self.params["tcp"] = "1"
            self.params["port"] = self.vgrow.tcp
        else:
            self.params["udp"] = "1"
            self.params["port"] = self.vgrow.udp

        self.filename = (
            f"{self.vgrow.country}_{self.vgrow.ip}_{self.protocol}_{self.params['port']}_{self.vgrow.score}.ovpn"
        )
        self.url = self.vgrow.url + self._location


class HtmlScraper:
    _lang = "/en/"
    _tab_id = "table#vg_hosts_table_id"
    _tab_data_cls0 = "vg_table_row_0"
    _tab_data_cls1 = "vg_table_row_1"

    def __init__(self, config: configuration.Configuration):
        self._config = config

    async def _http_get(self, session: aiohttp.ClientSession, url: str, params=None) -> str | None:
        timeout = aiohttp.ClientTimeout(total=self._config.timeout)
        try:
            async with session.get(url, timeout=timeout, params=params) as response:
                return await response.text() if response.status == 200 else None
        except aiohttp.ClientError as e:
            logger.error("GET %s failed: %s", url, e)
            return None

    async def _http_post(self, session: aiohttp.ClientSession, url: str, data) -> str | None:
        timeout = aiohttp.ClientTimeout(total=self._config.timeout)
        try:
            async with session.post(url, timeout=timeout, data=data) as response:
                return await response.text() if response.status == 200 else None
        except aiohttp.ClientError as e:
            logger.error("POST %s failed: %s", url, e)
            return None

    def _is_row_selected(self, e: VgRow) -> bool:
        return (
            e.country in self._config.country
            and e.session_number > self._config.session_number
            and e.bandwidth > self._config.bandwidth
        )

    def _is_link_selected(self, e: VgLink) -> bool:
        return e.protocol in self._config.protocol

    @staticmethod
    def _add_data_ciphers(s: str) -> str:
        for sep in ("cipher AES-128-CBC\r\n", "cipher AES-128-CBC\n"):
            if sep in s:
                s1, s2, s3 = s.partition(sep)
                cipher_value = s2.split()[-1].strip()
                return s1 + s2 + f"data-ciphers {cipher_value}\n" + s3
        return s

    async def _url_to_html(
        self, session: aiohttp.ClientSession, url: str, mode: str = "openvpn"
    ) -> tuple[str, str | None]:
        html = await self._http_get(session, url + self._lang)
        if html is None:
            return url, None
        pq = pyquery.PyQuery(html)

        v1 = pq("input#__VIEWSTATE").attr("value")
        v2 = pq("input#__VIEWSTATEGENERATOR").attr("value")
        v3 = pq("input#__EVENTVALIDATION").attr("value")

        form_data = {"__VIEWSTATE": v1, "__VIEWSTATEGENERATOR": v2, "__EVENTVALIDATION": v3}

        if mode == "l2tp":
            form_data["C_L2TP"] = "on"
        else:
            form_data["C_OpenVPN"] = "on"

        return url, await self._http_post(session, url + self._lang, form_data)

    async def _html_to_row_list(self, url: str, html: str) -> list[VgRow]:
        tabrow = pyquery.PyQuery(html)(self._tab_id).eq(2)("tr")
        rows = []
        for r in tabrow.items():
            if r.children().hasClass(self._tab_data_cls0) or r.children().hasClass(self._tab_data_cls1):
                try:
                    rows.append(VgRow(url, r))
                except (AttributeError, IndexError, ValueError) as e:
                    logger.warning("Skipping malformed VgRow: %s", e)
        return rows

    async def _row_to_link(self, vgrow: VgRow) -> list[VgLink] | None:
        if self._is_row_selected(vgrow):
            return list(filter(self._is_link_selected, vgrow.get_link()))
        return None

    async def _link_to_file(
        self, vglink: VgLink, sem: asyncio.Semaphore, session: aiohttp.ClientSession
    ) -> tuple[str, str | None]:
        async with sem:
            content = await self._http_get(session, vglink.url, vglink.params)
            if content is None:
                return vglink.filename, None
            return vglink.filename, self._add_data_ciphers(content)

    async def _get_l2tp_list(self, session: aiohttp.ClientSession, url: str) -> list[list[str]]:
        _, html = await self._url_to_html(session, url, mode="l2tp")
        if html is None:
            return []
        tabrow = pyquery.PyQuery(html)(self._tab_id).eq(2)("tr")
        tablist = [
            r
            for r in tabrow.items()
            if r.children().hasClass(self._tab_data_cls0) or r.children().hasClass(self._tab_data_cls1)
        ]

        l2tp_list = []
        for i in tablist:
            c = i.children()
            country = c.eq(0).text()
            ip = c.eq(1).text().split("\n")[1]
            sessions, uptime = c.eq(2).text().split("\n")[:2]
            sessions = sessions.split(" ")[0]
            bandwidth, ping = c.eq(3).text().split("\n")[:2]
            bandwidth = bandwidth.split(" Mbps")[0]
            ping = ping.split(": ")[1]
            ping = ping.split(" ms")[0]
            score = c.eq(9).text()
            l2tp_list.append([country, ip, sessions, uptime, bandwidth, ping, score])

        return l2tp_list

    @staticmethod
    def _format_l2tp_list(l2tp_list: list[list[str]]) -> str:
        output_table = prettytable.PrettyTable()
        output_table.title = "L2TP servers"
        output_table.field_names = ["CNTY", "IPAD", "Sess", "Uptime", "BW(Mbps)", "Ping(ms)", "Score"]
        output_table.add_rows(l2tp_list)
        output_table.hrules = prettytable.HRuleStyle.ALL
        return output_table.get_html_string(format=True)

    async def _run(self) -> tuple[list[tuple[str, str]], str]:
        sem = asyncio.Semaphore(self._config.concurrency_number)
        async with aiohttp.ClientSession() as session:
            url_html_list = await asyncio.gather(self._url_to_html(session, self._config.url))
            valid_html = [(u, h) for u, h in url_html_list if h is not None]

            row_lists = await asyncio.gather(*[self._html_to_row_list(u, h) for u, h in valid_html])
            rows = list(itertools.chain.from_iterable(row_lists))

            link_lists = await asyncio.gather(*[self._row_to_link(r) for r in rows])
            links = list(itertools.chain.from_iterable(e for e in link_lists if e is not None))

            files = await asyncio.gather(*[self._link_to_file(link, sem, session) for link in links])

            l2tp_list = await self._get_l2tp_list(session, self._config.url)
            ascii_table = self._format_l2tp_list(l2tp_list)

        return [(fname, content) for fname, content in files if content is not None], ascii_table

    def process_async(self) -> tuple[list[tuple[str, str]], str]:
        return asyncio.run(self._run())
