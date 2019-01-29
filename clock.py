import configuration
import async_html_parser
import mail_sender
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('interval', minutes=10)
def timed_job():
    c = configuration.Configuration()

    p = async_html_parser.HtmlParser(c)

    m = mail_sender.MailSender(c)

    m.send_zip(p.process_async())

sched.start()

