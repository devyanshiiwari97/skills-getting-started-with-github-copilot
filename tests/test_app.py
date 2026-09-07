def test_get_activities_returns_activity_details(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert {
        "description",
        "schedule",
        "max_participants",
        "participants",
    } <= activities["Chess Club"].keys()


def test_signup_adds_participant_and_is_reflected_in_activities(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert email in client.get("/activities").json()["Chess Club"]["participants"]


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_delete_removes_participant_and_is_reflected_in_activities(client):
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/Chess Club/participants/{email}")

    assert response.status_code == 200
    assert email not in client.get("/activities").json()["Chess Club"]["participants"]


def test_delete_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Club/participants/student@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_rejects_unregistered_participant(client):
    response = client.delete(
        "/activities/Chess Club/participants/not-registered@mergington.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"