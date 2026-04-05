import sys

import async_html_scraper
import configuration
import mail_sender

if __name__ == '__main__':

    c = configuration.Configuration()

    if len(sys.argv) > 1:
        c.mail = sys.argv[1:]

    p = async_html_scraper.HtmlScraper(c)

    m = mail_sender.MailSender(c)

    m.send_zip(p.process_async())
