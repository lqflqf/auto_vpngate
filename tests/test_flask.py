import main


def test_index():
    main.app.testing = True
    client = main.app.test_client()
    r = client.get('/')
    assert r.status_code == 200


def test_job():
    assert len(main.b_scheduler.get_jobs()) > 0
