def test_example(user_client):
    response = user_client.get('/example')

    assert response.status_code == 200, f'{response.request.url} and {response.request}'
    assert 'message' in response.json()
