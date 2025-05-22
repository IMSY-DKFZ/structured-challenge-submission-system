# backend/BMC_API/tests/test_redis_route.py

import pytest
from fastapi import HTTPException, status

import BMC_API.src.api.routes.admin.admin_redis as admin_redis_module


@pytest.mark.anyio
async def test_redis_health_success(monkeypatch):
    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def ping(self): return True

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    result = await admin_redis_module.redis_health(redis_pool=None)
    assert result == {"message": "Redis server works"}

@pytest.mark.anyio
async def test_redis_health_failure(monkeypatch):
    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def ping(self): raise Exception("down")

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    with pytest.raises(HTTPException) as exc_info:
        await admin_redis_module.redis_health(redis_pool=None)
    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

@pytest.mark.anyio
async def test_get_redis_value_success(monkeypatch):
    key = "foo"
    value = "bar"

    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def get(self, k):
            assert k == key
            return value

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    dto = await admin_redis_module.get_redis_value(key=key, redis_pool=None)
    assert dto.key == key
    assert dto.value == value

@pytest.mark.anyio
async def test_get_redis_value_not_found(monkeypatch):
    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def get(self, k): return None

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    with pytest.raises(HTTPException) as exc_info:
        await admin_redis_module.get_redis_value(key="foo", redis_pool=None)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND
    assert "Key not found" in exc_info.value.detail

@pytest.mark.anyio
async def test_get_redis_value_service_unavailable(monkeypatch):
    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def get(self, k): raise Exception("lost connection")

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    with pytest.raises(HTTPException) as exc_info:
        await admin_redis_module.get_redis_value(key="foo", redis_pool=None)
    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

@pytest.mark.anyio
async def test_get_all_redis_values_success(monkeypatch):
    keys = [b"a", b"b"]
    values = [b"1", None]

    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def keys(self, pattern):
            assert pattern == "*"
            return keys
        async def mget(self, ks):
            assert ks == keys
            return values

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    result = await admin_redis_module.get_all_redis_values(redis_pool=None)
    assert isinstance(result, list)
    assert result[0].key == "a" and result[0].value == "1"
    assert result[1].key == "b" and result[1].value is None

@pytest.mark.anyio
async def test_get_all_redis_values_not_found(monkeypatch):
    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def keys(self, pattern): return []

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    with pytest.raises(HTTPException) as exc_info:
        await admin_redis_module.get_all_redis_values(redis_pool=None)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_set_redis_value_success(monkeypatch):
    from BMC_API.src.api.schemas.redis_schema import RedisValueDTO
    dto = RedisValueDTO(key="x", value="y")
    calls = []

    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def set(self, name, value):
            calls.append((name, value))

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    result = await admin_redis_module.set_redis_value(redis_value=dto, redis_pool=None)
    assert calls == [("x", "y")]
    assert result == {"message": "key-value pair successfully stored in Redis database."}

@pytest.mark.anyio
async def test_set_redis_value_no_value():
    from BMC_API.src.api.schemas.redis_schema import RedisValueDTO
    dto = RedisValueDTO(key="x", value=None)
    result = await admin_redis_module.set_redis_value(redis_value=dto, redis_pool=None)
    assert result is None

@pytest.mark.anyio
async def test_delete_redis_key_success(monkeypatch):
    key = "k"
    calls = []

    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def get(self, k): return b"v"
        async def delete(self, k): calls.append(k)

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    result = await admin_redis_module.delete_redis_key(key=key, redis_pool=None)
    assert calls == [key]
    assert result == {"message": "key-value pair successfully deleted from Redis database."}

@pytest.mark.anyio
async def test_delete_redis_key_not_found(monkeypatch):
    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def get(self, k): return None

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    with pytest.raises(HTTPException) as exc_info:
        await admin_redis_module.delete_redis_key(key="k", redis_pool=None)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_delete_redis_key_delete_error(monkeypatch):
    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def get(self, k): return b"v"
        async def delete(self, k): raise Exception("fail")

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    with pytest.raises(HTTPException) as exc_info:
        await admin_redis_module.delete_redis_key(key="k", redis_pool=None)
    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE

@pytest.mark.anyio
async def test_delete_all_redis_keys_success(monkeypatch):
    calls = []

    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def keys(self, pattern): return [b"a", b"b"]
        async def delete(self, *keys): calls.extend(keys)

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    result = await admin_redis_module.delete_all_redis_keys(current_active_user=None, redis_pool=None)
    assert calls == [b"a", b"b"]
    assert result == {"message": "All key-value pairs successfully deleted from Redis database."}

@pytest.mark.anyio
async def test_delete_all_redis_keys_not_found(monkeypatch):
    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def keys(self, pattern): raise Exception("No active exception to reraise")

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    with pytest.raises(HTTPException) as exc_info:
        await admin_redis_module.delete_all_redis_keys(current_active_user=None, redis_pool=None)
    assert exc_info.value.status_code == status.HTTP_404_NOT_FOUND

@pytest.mark.anyio
async def test_delete_all_redis_keys_service_unavailable(monkeypatch):
    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def keys(self, pattern): raise Exception("redis down")

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    with pytest.raises(HTTPException) as exc_info:
        await admin_redis_module.delete_all_redis_keys(current_active_user=None, redis_pool=None)
    assert exc_info.value.status_code == status.HTTP_503_SERVICE_UNAVAILABLE


@pytest.mark.anyio
async def test_health_endpoint(monkeypatch, client, fastapi_app):
    # Bypass auth
    monkeypatch.setattr(admin_redis_module.RoleChecker, "__call__", lambda self: None)
    fastapi_app.dependency_overrides[admin_redis_module.get_redis_pool] = lambda: None

    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def ping(self): return True

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    url = fastapi_app.url_path_for("redis_health")
    response = await client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Redis server works"}

@pytest.mark.anyio
async def test_delete_all_keys_endpoint(monkeypatch, client, fastapi_app):
    # Bypass auth and password check
    monkeypatch.setattr(admin_redis_module.RoleChecker, "__call__", lambda self: None)
    fastapi_app.dependency_overrides[admin_redis_module.validate_active_user_password_dependency] = lambda: None
    fastapi_app.dependency_overrides[admin_redis_module.get_redis_pool] = lambda: None

    calls = []
    class DummyRedis:
        def __init__(self, connection_pool): pass
        async def __aenter__(self): return self
        async def __aexit__(self, exc_type, exc, tb): pass
        async def keys(self, pattern): return [b"x"]
        async def delete(self, *keys): calls.extend(keys)

    monkeypatch.setattr(admin_redis_module, "Redis", DummyRedis)
    url = fastapi_app.url_path_for("delete_all_redis_keys")
    response = await client.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "All key-value pairs successfully deleted from Redis database."}
    assert calls == [b"x"]
