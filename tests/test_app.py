from urllib.parse import quote

import src.app as app_module


def test_get_activities(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert expected_activity in data
    assert "participants" in data[expected_activity]
    assert isinstance(data[expected_activity]["participants"], list)


def test_signup_activity(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"
    path = f"/activities/{quote(activity)}/signup"

    # Act
    response = client.post(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}
    assert email in app_module.activities[activity]["participants"]


def test_duplicate_signup_rejected(client):
    # Arrange
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    path = f"/activities/{quote(activity)}/signup"

    # Act
    first_response = client.post(path, params={"email": email})
    second_response = client.post(path, params={"email": email})

    # Assert
    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json() == {"detail": "Student already signed up"}


def test_delete_participant(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    path = f"/activities/{quote(activity)}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity}"}
    assert email not in app_module.activities[activity]["participants"]


def test_delete_missing_participant_returns_404(client):
    # Arrange
    activity = "Chess Club"
    email = "missing@mergington.edu"
    path = f"/activities/{quote(activity)}/participants"

    # Act
    response = client.delete(path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found"}
