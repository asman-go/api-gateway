def test_healthcheck(public_client):
    response = public_client.get('/healthcheck')

    assert response.status_code == 200
    assert response.json() == {
        'message': 'OK'
    }
