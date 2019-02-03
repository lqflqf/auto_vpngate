from apscheduler.schedulers.blocking import BlockingScheduler
from . import configuration
from . import mail_sender
from . import async_html_parser

sched = BlockingScheduler()

@sched.scheduled_job('cron', day_of_week='mon-sun', hour='0,8,16')
def scheduled_job():
    c = configuration.Configuration()

    p = async_html_parser.HtmlParser(c)

    m = mail_sender.MailSender(c)

    m.send_zip(p.process_async())

sched.start()


