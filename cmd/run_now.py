import configuration
import async_html_parser
import mail_sender
import sys


if __name__ == '__main__':

    c = configuration.Configuration()

    if sys.argv != ['']:
        c.mail = sys.argv

    p = async_html_parser.HtmlParser(c)

    m = mail_sender.MailSender(c)

    m.send_zip(p.process_async())
