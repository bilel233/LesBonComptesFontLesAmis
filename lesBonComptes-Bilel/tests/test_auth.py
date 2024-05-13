def test_register(client):
    # Données pour l'inscription
    valid_user = {
        "username": "admin",
        "password": "admin123"
    }

    # Envoi de la requête POST
    response = client.post('/auth/register', json=valid_user)

    # Vérification que l'inscription réussit
    assert response.status_code == 201
    assert b"Utilisateur cr\xe9\xe9 avec succ\xe8s" in response.data

    # Test avec un utilisateur sans mot de passe
    incomplete_user = {
        "username": "testuser2"
    }

    response = client.post('/auth/register', json=incomplete_user)
    assert response.status_code == 400
    assert b"Le mot de passe est requis" in response.data
