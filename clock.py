from apscheduler.schedulers.blocking import BlockingScheduler
import configuration
import mail_sender
import async_html_parser


sched = BlockingScheduler()


@sched.scheduled_job('cron', day_of_week='mon-sun', hour='0,12')
def scheduled_job():
    c = configuration.Configuration()

    p = async_html_parser.HtmlParser(c)

    m = mail_sender.MailSender(c)

    m.send_zip(p.process_async())


sched.start()


