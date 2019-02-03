from . import configuration
from . import async_html_parser
from . import mail_sender


if __name__ == '__main__':

    c = configuration.Configuration()

    p = async_html_parser.HtmlParser(c)

    m = mail_sender.MailSender(c)

    m.send_zip(p.process_async())
