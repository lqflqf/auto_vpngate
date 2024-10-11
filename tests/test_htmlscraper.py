import pytest
import async_html_scraper
import configuration
import pyquery


@pytest.fixture
def scraper():
    return async_html_scraper.HtmlScraper(configuration.Configuration())


@pytest.mark.asyncio
async def test_openvpn(scraper):
    url, html = await scraper.__url_to_html__(scraper.__config__.url)
    assert url == scraper.__config__.url
    pq = pyquery.PyQuery(html)
    assert len(pq.children()) > 1

    row_list = await scraper.__html_to_row_list__(url, html)
    assert len(row_list) > 0


@pytest.mark.asyncio
async def test_l2tp(scraper):
    l2tp_list = await scraper.__get_l2tp_list__(scraper.__config__.url)
    assert len(l2tp_list) > 0


def test_process(scraper):
    files, mail_text = scraper.process_async()
    assert len(files) > 0
    assert files[0][1].find('data-ciphers') > 0
    assert len(mail_text) > 0
