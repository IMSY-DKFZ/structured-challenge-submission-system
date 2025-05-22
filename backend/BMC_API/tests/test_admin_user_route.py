# backend/BMC_API/tests/test_admin_user.py
from unittest.mock import patch

import pytest
from fastapi import FastAPI, status
from httpx import AsyncClient

from BMC_API.src.application.dto.user_dto import UserCreateAdminDTO, UserUpdateAdminDTO

pytest_plugins = [
    "BMC_API.tests.fixtures.admin_user_fixtures",
    "BMC_API.tests.fixtures.user_fixtures",
]


class TestAdminUserRoutes:
    """Tests for the admin user routes"""

    @pytest.mark.anyio
    async def test_get_user_admin_success(
        self, client: AsyncClient, fastapi_app: FastAPI, test_user_confirmed: UserCreateAdminDTO, admin_token
    ):
        """Test successfully getting a user as admin"""
        # Create a user first
        user_data = test_user_confirmed.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route_admin")
        create_response = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        created_admin_id = create_response.json()["id"]

        # Act
        url = fastapi_app.url_path_for("get_user_route_admin", id=created_admin_id)
        response = await client.get(url, headers={"Authorization": f"Bearer {admin_token}"})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == test_user_confirmed.email
        assert "password" not in response.json()

    @pytest.mark.anyio
    async def test_get_user_admin_not_found(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        """Test getting a non-existent user as admin"""
        # Arrange

        non_existent_id = 9999  # Assuming this ID doesn't exist

        # Act
        url = fastapi_app.url_path_for("get_user_route_admin", id=non_existent_id)
        response = await client.get(url, headers={"Authorization": f"Bearer {admin_token}"})

        # Assert - Assuming your API returns null/None for non-existent users
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.anyio
    async def test_get_user_admin_unauthorized(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        test_user_confirmed: UserCreateAdminDTO,
        admin_token,
    ):
        """Test getting a user as a non-admin user (should fail)"""
        # Arrange
        # Create a user first
        user_data = test_user_confirmed.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route_admin")
        await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        login_data = {
            "username": test_user_confirmed.email,
            "password": test_user_confirmed.password,
        }
        login_url = fastapi_app.url_path_for("login_route")
        login_response = await client.post(login_url, data=login_data)

        user_token = login_response.json()["access_token"]

        # Act
        url = fastapi_app.url_path_for("get_user_route_admin", id=1)  # Any ID
        response = await client.get(url, headers={"Authorization": f"Bearer {user_token}"})

        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "You don't have permission".lower() in response.json()["detail"].lower()

    @pytest.mark.anyio
    async def test_list_users_admin_success(
        self, client: AsyncClient, fastapi_app: FastAPI, test_user: UserCreateAdminDTO, admin_token
    ):
        """Test listing users as admin"""
        # Create a regular user
        user_data = test_user.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route_admin")
        create_response = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        # Act
        url = fastapi_app.url_path_for("list_users_route_admin")
        response = await client.post(url, headers={"Authorization": f"Bearer {admin_token}"})

        # Assert

        assert response.status_code == status.HTTP_200_OK
        assert "content" in response.json()
        assert "total_records" in response.json()
        assert "total_pages" in response.json()
        assert response.json()["total_records"] >= 2  # At least admin and created user

    @pytest.mark.anyio
    async def test_list_users_admin_with_pagination(
        self, client: AsyncClient, fastapi_app: FastAPI, test_user: UserCreateAdminDTO, admin_token
    ):
        """Test listing users with pagination as admin"""
        # Act
        url = fastapi_app.url_path_for("list_users_route_admin")
        response = await client.post(
            url,
            params={"limit": 1, "offset": 0},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()["content"]) <= 1  # Should return at most 1 user

    @pytest.mark.anyio
    async def test_list_users_admin_with_search_filter(
        self, client: AsyncClient, fastapi_app: FastAPI, test_admin: UserCreateAdminDTO, admin_token
    ):
        """Test listing users with search filters as admin"""
        # Act
        url = fastapi_app.url_path_for("list_users_route_admin")
        response = await client.post(
            url,
            json={"search_filters": {"email": test_admin.email}},
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        # If there are results, the specific user should be in the response
        if response.json()["total_records"] > 0:
            user_emails = [user["email"] for user in response.json()["content"]]
            assert test_admin.email in user_emails

    @pytest.mark.anyio
    async def test_create_user_admin_success(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        admin_token,
        test_user_admin_create_dto: UserCreateAdminDTO,
    ):
        """Test creating a user as admin"""
        # Arrange

        user_data = test_user_admin_create_dto.model_dump()

        # Act
        url = fastapi_app.url_path_for("create_user_route_admin")
        response = await client.post(url, json=user_data, headers={"Authorization": f"Bearer {admin_token}"})

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == test_user_admin_create_dto.email
        assert response.json()["first_name"] == test_user_admin_create_dto.first_name
        assert response.json()["last_name"] == test_user_admin_create_dto.last_name
        assert "password" not in response.json()

    @pytest.mark.anyio
    async def test_create_user_admin_duplicate(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        admin_token,
        test_user_admin_create_dto: UserCreateAdminDTO,
    ):
        """Test creating a duplicate user as admin"""
        # Arrange

        user_data = test_user_admin_create_dto.model_dump()

        # First create the user
        url = fastapi_app.url_path_for("create_user_route_admin")
        await client.post(url, json=user_data, headers={"Authorization": f"Bearer {admin_token}"})

        # Act - Try to create the same user again
        response = await client.post(url, json=user_data, headers={"Authorization": f"Bearer {admin_token}"})

        # Assert
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "already exists" in response.json()["detail"]

    @pytest.mark.anyio
    async def test_create_user_admin_validation_error(self, client: AsyncClient, fastapi_app: FastAPI, admin_token):
        """Test creating a user with invalid data as admin"""
        # Arrange

        invalid_user_data = {
            "email": "not-an-email",  # Invalid email format
            "password": "short",  # Too short password
            "first_name": "Test",
            "last_name": "User",
            "roles": ["ADMIN"],
        }

        # Act
        url = fastapi_app.url_path_for("create_user_route_admin")
        response = await client.post(
            url,
            json=invalid_user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # Assert
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    @pytest.mark.anyio
    async def test_update_user_admin_success(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        admin_token,
        test_user: UserCreateAdminDTO,
        test_user_update_admin_dto: UserUpdateAdminDTO,
        confirmed_user,
    ):
        """Test updating a user as admin"""
        # Arrange

        # Create a regular user first
        user_data = test_user.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route_admin")
        create_response = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        created_user_id = create_response.json()["id"]

        update_data = test_user_update_admin_dto.model_dump()
        update_data.pop("password")

        # Act
        url = fastapi_app.url_path_for("update_user_route_admin", id=created_user_id)
        response = await client.put(url, json=update_data, headers={"Authorization": f"Bearer {admin_token}"})

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["email"] == test_user_update_admin_dto.email
        assert response.json()["first_name"] == test_user_update_admin_dto.first_name
        assert response.json()["last_name"] == test_user_update_admin_dto.last_name
        assert response.json()["country"] == test_user_update_admin_dto.country
        assert "password" not in response.json()

    @pytest.mark.anyio
    async def test_update_user_admin_not_found(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        admin_token,
        test_user_update_admin_dto: UserUpdateAdminDTO,
    ):
        """Test updating a non-existent user as admin"""
        # Arrange

        update_data = test_user_update_admin_dto.model_dump()
        update_data.pop("password")
        non_existent_id = 9999  # Assuming this ID doesn't exist

        # Act
        url = fastapi_app.url_path_for("update_user_route_admin", id=non_existent_id)
        response = await client.put(url, json=update_data, headers={"Authorization": f"Bearer {admin_token}"})

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.anyio
    async def test_bulk_update_users_admin_success(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        admin_token,
        test_user: UserCreateAdminDTO,
        test_bulk_update_data,
        confirmed_user,
    ):
        """Test bulk updating users as admin"""
        # Arrange

        # Create users first
        user_data = test_user.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route_admin")
        create_response1 = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        user_data["email"] = "another_test@example.com"
        create_response2 = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # Update bulk_update_data with actual user IDs
        test_bulk_update_data[0]["id"] = create_response1.json()["id"]
        test_bulk_update_data[1]["id"] = create_response2.json()["id"]

        # Act
        url = fastapi_app.url_path_for("bulk_update_users_route_admin")
        response = await client.put(
            url,
            json=test_bulk_update_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "successful" in response.json()
        assert len(response.json()["successful"]) > 0

        # Verify the changes by getting the updated users
        for user_update in test_bulk_update_data:
            get_url = fastapi_app.url_path_for("get_user_route_admin", id=user_update["id"])
            get_response = await client.get(get_url, headers={"Authorization": f"Bearer {admin_token}"})
            assert get_response.status_code == status.HTTP_200_OK
            assert get_response.json()["first_name"] == user_update["first_name"]
            assert get_response.json()["last_name"] == user_update["last_name"]

    @pytest.mark.anyio
    async def test_bulk_update_users_admin_partial_success(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        admin_token,
        test_user: UserCreateAdminDTO,
        test_bulk_update_data,
        confirmed_user,
    ):
        """Test bulk updating users with some failures as admin"""
        # Arrange

        user_data = test_user.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route_admin")
        create_response = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        valid_id = create_response.json()["id"]

        # One valid ID and one invalid ID
        test_bulk_update_data[0]["id"] = valid_id
        test_bulk_update_data[1]["id"] = 9999  # Assuming this ID doesn't exist

        # Act
        url = fastapi_app.url_path_for("bulk_update_users_route_admin")
        response = await client.put(
            url,
            json=test_bulk_update_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert "successful" in response.json()
        assert "failed" in response.json()
        assert len(response.json()["successful"]) == 1
        assert len(response.json()["failed"]) == 1

    @pytest.mark.anyio
    async def test_delete_user_admin_success(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        admin_token,
        test_admin,
        test_user: UserCreateAdminDTO,
        confirmed_user,
    ):
        """Test deleting a user as admin"""
        # Arrange

        # Create a regular user first
        user_data = test_user.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route_admin")
        create_response = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        created_user_id = create_response.json()["id"]

        # Mock the password verification since the test is using the
        # validate_active_user_password_dependency

        with patch(
            "BMC_API.src.application.interfaces.authentication.auth.authenticate_user",
            return_value=True,
        ):
            # Act
            url = fastapi_app.url_path_for("delete_user_route_admin", id=created_user_id)
            response = await client.request(
                "DELETE",
                url,
                params={"active_user_password": test_admin.password},
                headers={"Authorization": f"Bearer {admin_token}"},
            )

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert "User deleted" in response.json()["detail"]

            # Verify the user is deleted
            get_url = fastapi_app.url_path_for("get_user_route_admin", id=created_user_id)
            get_response = await client.get(get_url, headers={"Authorization": f"Bearer {admin_token}"})

            assert get_response.status_code == status.HTTP_404_NOT_FOUND
            assert "not found" in get_response.json()["detail"].lower()

    @pytest.mark.anyio
    async def test_delete_user_admin_not_found(
        self, client: AsyncClient, fastapi_app: FastAPI, admin_token, test_admin
    ):
        """Test deleting a non-existent user as admin"""
        # Arrange
        non_existent_id = 9999  # Assuming this ID doesn't exist

        # Mock the password verification
        with patch(
            "BMC_API.src.application.interfaces.authentication.auth.authenticate_user",
            return_value=True,
        ):
            # Act
            url = fastapi_app.url_path_for("delete_user_route_admin", id=non_existent_id)

            response = await client.request(
                "DELETE",
                url,
                params={"active_user_password": test_admin.password},
                headers={"Authorization": f"Bearer {admin_token}"},
            )

            # Assert
            assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.anyio
    async def test_delete_user_admin_without_password(
        self, client: AsyncClient, fastapi_app: FastAPI, test_user: UserCreateAdminDTO, confirmed_user, admin_token
    ):
        """Test deleting a user without providing password as admin"""
        # Arrange

        # Create a regular user first
        user_data = test_user.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route_admin")
        create_response = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        created_user_id = create_response.json()["id"]

        # Act - Don't provide the password
        url = fastapi_app.url_path_for("delete_user_route_admin", id=created_user_id)
        response = await client.delete(url, headers={"Authorization": f"Bearer {admin_token}"})

        # Assert
        assert response.status_code in [
            status.HTTP_401_UNAUTHORIZED,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        ]

    @pytest.mark.anyio
    async def test_bulk_delete_users_admin_success(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        test_user: UserCreateAdminDTO,
        confirmed_user,
        admin_token,
        test_admin,
    ):
        """Test bulk deleting users as admin"""
        # Arrange

        # Create users first
        user_data = test_user.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route_admin")
        create_response1 = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        user_data["email"] = "another_bulk_test@example.com"
        create_response2 = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )

        user_ids = [create_response1.json()["id"], create_response2.json()["id"]]

        # Mock the password verification
        with patch(
            "BMC_API.src.application.interfaces.authentication.auth.authenticate_user",
            return_value=True,
        ):
            # Act
            url = fastapi_app.url_path_for("bulk_delete_users_route_admin")
            response = await client.request(
                "DELETE",
                url,
                params={"active_user_password": test_admin.password},
                json=user_ids,
                headers={"Authorization": f"Bearer {admin_token}"},
            )

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert "successful" in response.json()
            assert len(response.json()["successful"]) == 2

            # Verify the users are deleted
            for user_id in user_ids:
                get_url = fastapi_app.url_path_for("get_user_route_admin", id=user_id)
                get_response = await client.get(get_url, headers={"Authorization": f"Bearer {admin_token}"})
                assert get_response.status_code == status.HTTP_404_NOT_FOUND
                assert "not found" in get_response.json()["detail"].lower()

    @pytest.mark.anyio
    async def test_bulk_delete_users_admin_partial_success(
        self,
        client: AsyncClient,
        fastapi_app: FastAPI,
        test_user: UserCreateAdminDTO,
        confirmed_user,
        admin_token,
        test_admin,
    ):
        """Test bulk deleting users with some failures as admin"""
        # Arrange

        user_data = test_user.model_dump()
        create_url = fastapi_app.url_path_for("create_user_route_admin")
        create_response = await client.post(
            create_url,
            json=user_data,
            headers={"Authorization": f"Bearer {admin_token}"},
        )
        valid_id = create_response.json()["id"]

        # One valid ID and one invalid ID
        user_ids = [valid_id, 9999]  # Assuming 9999 doesn't exist

        # Mock the password verification
        with patch(
            "BMC_API.src.application.interfaces.authentication.auth.authenticate_user",
            return_value=True,
        ):
            # Act
            url = fastapi_app.url_path_for("bulk_delete_users_route_admin")
            response = await client.request(
                "DELETE",
                url,
                params={"active_user_password": test_admin.password},
                json=user_ids,
                headers={"Authorization": f"Bearer {admin_token}"},
            )

            # Assert
            assert response.status_code == status.HTTP_200_OK
            assert "successful" in response.json()
            assert "failed" in response.json()
            assert len(response.json()["successful"]) == 1
            assert len(response.json()["failed"]) == 1
