from fastapi.testclient import TestClient
from sqlalchemy.orm.session import Session

from src.modules.users.model import User


def test_sign_up(db: Session, client: TestClient):
    response = client.post(
        "/users", json={"email": "testuser@gmail.com", "password": "testpassword"}
    )
    assert response.status_code == 200
    assert len(db.query(User).all()) == 1
    db_user = db.query(User).first()
    assert db_user is not None
    assert db_user.email == "testuser@gmail.com"
