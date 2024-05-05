def test_example(client):
    response = client.get('/example')

    assert response.status_code == 200
    assert response.json() == {
        'message': 'test1'
    }
