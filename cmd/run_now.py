import configuration
import async_html_parser
import mail_sender
import sys


if __name__ == '__main__':

    c = configuration.Configuration()

    if len(sys.argv) > 1:
        c.mail = sys.argv[1:]

    p = async_html_parser.HtmlParser(c)

    m = mail_sender.MailSender(c)

    m.send_zip(p.process_async())
