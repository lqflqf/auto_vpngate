import aiohttp
import pyquery
import pytest

import async_html_scraper
import configuration


@pytest.fixture
def scraper():
    if not __import__("os").getenv("GOOGLE_CLOUD_PROJECT"):
        pytest.skip("Requires GOOGLE_CLOUD_PROJECT environment variable")
    return async_html_scraper.HtmlScraper(configuration.Configuration())


@pytest.mark.integration
@pytest.mark.asyncio
async def test_openvpn(scraper):
    async with aiohttp.ClientSession() as session:
        url, html = await scraper._url_to_html(session, scraper._config.url)
    assert url == scraper._config.url
    assert html is not None
    pq = pyquery.PyQuery(html)
    assert len(pq.children()) > 1

    row_list = await scraper._html_to_row_list(url, html)
    assert len(row_list) > 0


@pytest.mark.integration
@pytest.mark.asyncio
async def test_l2tp(scraper):
    async with aiohttp.ClientSession() as session:
        l2tp_list = await scraper._get_l2tp_list(session, scraper._config.url)
    assert len(l2tp_list) > 0


@pytest.mark.integration
def test_process(scraper):
    files, mail_text = scraper.process_async()
    assert len(files) > 0
    assert files[0][1].find("data-ciphers") > 0
    assert len(mail_text) > 0
