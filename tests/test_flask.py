import main


def test_index():
    main.app.testing = True
    client = main.app.test_client()
    r = client.get('/')
    assert r.status_code == 200


def test_process_1():
    main.app.testing = True
    client = main.app.test_client()
    r = client.get('/process')
    assert r.status_code == 400


def test_process_2():
    main.app.testing = True
    client = main.app.test_client()
    r = client.get('/process?access_key=1234abcd')
    assert r.status_code == 401
