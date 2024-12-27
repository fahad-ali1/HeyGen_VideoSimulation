import pytest
from fastapi.testclient import TestClient
from server.server import app

client = TestClient(app)

@pytest.fixture
def start_translation():
    """Test post request to start translation job. Fixture for rest of tests."""
    response = client.post("/start")
    assert response.status_code == 200
    job_id = response.json()["job_id"]
    return job_id

def test_start_translation(start_translation):
    """
    Test to ensure the start translation endpoint works as expected.
    """
    job_id = start_translation
    print("\n--- TEST 1 ---")
    # Ensure that the job ID returned is a valid UUID string
    assert isinstance(job_id, str)
    assert len(job_id) > 0
    print(f"Start translation test passed. Expected valid UUID string. Got: {job_id}\n")

def test_status_pending(start_translation):
    """
    Test to ensure the status endpoint returns 'pending' for an ongoing job.
    """
    job_id = start_translation
    print("--- TEST 2 ---")

    response = client.get(f"/status/{job_id}")
    print(f"Received status response: {response.json()['result']}")
    assert response.status_code == 200
    assert response.json()["result"] == "pending"
    print(f"Status 'pending' test passed. Expected: pending. Got: {response.json()["result"]}\n")

def test_status_completed():
    """
    Test to check if the job status is completed or error after a simulated delay.
    """
    job_id = client.post("/start").json()["job_id"]
    print("--- TEST 3 ---")    
    # Simulate a delay for job completion
    import time
    time.sleep(6)

    response = client.get(f"/status/{job_id}")
    print(f"Received status response: {response.json()['result']}")
    assert response.status_code == 200
    result = response.json()["result"]
    assert result in ["completed", "error"]
    print(f"Job status is: {result}")
    print("Status completed/error test passed.\n")

def test_special_pending_job():
    """
    Test to check the special job ID which always returns 'pending' status.
    """
    print("--- TEST 4 ---")
    print("\n--- Testing special job ID 'special-pending-job' ---")
    response = client.get(f"/status/special-pending-job")
    print(f"Received status response for special job: {response.json()['result']}")
    assert response.status_code == 200
    assert response.json()["result"] == "pending"
    print("Special pending job test passed.\n")

def test_status_not_found():
    """
    Test for a non-existing job ID to ensure the correct error is returned.
    """
    print("--- TEST 5 ---")
    print("\n--- Testing for non-existing job ID ---")
    response = client.get("/status/invalid-job-id")
    print(f"Received error response: {response.json()}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Job not found"
    print("Status not found test passed.\n")
