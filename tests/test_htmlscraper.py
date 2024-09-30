import pytest
import async_html_scraper
import configuration
import pyquery


@pytest.fixture
def parser():
    return async_html_scraper.HtmlScraper(configuration.Configuration())


@pytest.mark.asyncio
async def test_openvpn(parser):
    url, html = await parser.__url_to_html__(parser.__config__.url)
    assert url == parser.__config__.url
    pq = pyquery.PyQuery(html)
    assert len(pq.children()) > 1

    row_list = await parser.__html_to_row_list__(url, html)
    assert len(row_list) > 0


@pytest.mark.asyncio
async def test_l2tp(parser):
    l2tp_text = await parser.__get_l2tp_list__(parser.__config__.url)
    assert len(l2tp_text) > 0


def test_process(parser):
    files = parser.process_async()[0]
    assert len(files) > 0
    assert files[0][1].find('data-ciphers') > 0
