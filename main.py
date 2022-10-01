from apscheduler.schedulers.background import BackgroundScheduler
import configuration
import mail_sender
import async_html_parser
from flask import Flask, request, abort

config_obj = configuration.Configuration()


def run_job():
    print("job start")
    c = configuration.Configuration()
    p = async_html_parser.HtmlParser(c)
    m = mail_sender.MailSender(c)
    m.send_zip(p.process_async())
    print("job done")


app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route('/process')
def process():
    access_key = request.args['access_key']
    if access_key == config_obj.access_key:
        run_job()
        return 'Job Done'
    else:
        abort(401)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. You
    # can configure startup instructions by adding `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
