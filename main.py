import hmac
import logging
import threading

from flask import Flask, abort, request

import async_html_scraper
import configuration
import mail_sender

logger = logging.getLogger(__name__)

_config_obj: configuration.Configuration | None = None
_config_lock = threading.Lock()


def get_config() -> configuration.Configuration:
    global _config_obj
    if _config_obj is None:
        with _config_lock:
            if _config_obj is None:
                _config_obj = configuration.Configuration()
    return _config_obj


def run_job() -> None:
    logger.info("job start")
    c = get_config()
    p = async_html_scraper.HtmlScraper(c)
    m = mail_sender.MailSender(c)
    m.send_zip(p.process_async())
    logger.info("job done")


app = Flask(__name__)


@app.route("/")
def hello() -> str:
    """Return a friendly HTTP greeting."""
    return "Hello World!"


@app.route("/process")
def process() -> str:
    # App Engine cron jobs inject this header; it cannot be spoofed from outside.
    if request.headers.get("X-Appengine-Cron") == "true":
        try:
            run_job()
        except Exception:
            logger.exception("run_job failed (cron)")
            abort(500)
        return "Job Done"

    access_key = request.args.get("access_key", "")
    if not access_key:
        abort(400)
    if not hmac.compare_digest(access_key, get_config().access_key):
        abort(401)
    try:
        run_job()
    except Exception:
        logger.exception("run_job failed")
        abort(500)
    return "Job Done"


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)
