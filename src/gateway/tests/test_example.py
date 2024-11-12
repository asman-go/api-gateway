def test_example(public_client):
    response = public_client.get('/example')

    assert response.status_code == 200
    assert response.json() == {
        'message': 'test1'
    }
