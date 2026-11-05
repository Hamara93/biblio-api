from fastapi.testclient import TestClient
from main import app, init_db

init_db()
client = TestClient(app)

def test_accueil():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Bonjour, atelier !"}

def test_creer_livre():
    r = client.post("/livres", json={"titre": "Dune", "auteur": "Herbert", "annee": 1965})
    assert r.status_code == 201
    assert r.json()["titre"] == "Dune"
    assert "id" in r.json()

def test_lister_livres():
    r = client.get("/livres")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_livre_introuvable():
    r = client.get("/livres/99999")
    assert r.status_code == 404

def test_validation_annee():
    # L'année doit être entre 1450 et 2100, donc 1000 doit échouer
    r = client.post("/livres", json={"titre": "Test", "auteur": "Test", "annee": 1000})
    assert r.status_code == 422