from apscheduler.schedulers.background import BackgroundScheduler
import configuration
import mail_sender
import async_html_parser
from flask import Flask

config = configuration.Configuration()
b_scheduler = BackgroundScheduler(timezone=config.timezone)


def run_job():
    print("job start")
    c = configuration.Configuration()
    p = async_html_parser.HtmlParser(c)
    m = mail_sender.MailSender(c)
    m.send_zip(p.process_async())
    print("job done")


b_scheduler.add_job(func=run_job, trigger=config.trigger, day_of_week=config.day_of_week, hour=config.hour)
# b_scheduler.add_job(func=run_job, trigger="interval", minutes=5)

b_scheduler.start()

app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
