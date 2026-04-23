from auditiq.services.auth import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
    _generate_slug,
)
import uuid


def test_password_hash_and_verify():
    password = "test-password-123"
    hashed = hash_password(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("wrong-password", hashed)


def test_create_and_decode_token():
    consultant_id = uuid.uuid4()
    token = create_access_token(consultant_id)
    payload = decode_access_token(token)
    assert payload["sub"] == str(consultant_id)
    assert payload["type"] == "access"
    assert "exp" in payload


def test_generate_slug():
    assert _generate_slug("Acme Corp") == "acme-corp"
    assert _generate_slug("   Hello World!  ") == "hello-world"
    assert _generate_slug("Test--Double") == "test-double"
    assert _generate_slug("UPPER CASE") == "upper-case"
    assert _generate_slug("a" * 100)[:63] == "a" * 63
