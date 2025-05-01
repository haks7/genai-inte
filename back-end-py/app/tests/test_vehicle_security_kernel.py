import pytest
from app.vehicle_security_kernel import run_vehicle_security_reasoning
import asyncio

@pytest.mark.asyncio
async def test_vehicle_security_reasoning_positive():
    """
    Test case for a positive scenario where no suspicious activity is detected.
    """
    # Mock inputs
    reasoning_prompt = """
    The vehicle is experiencing the following conditions:
    - Face recognition result: {face_recognition_result}.
    - Door sensor status: {door_sensor_status}.
    - Motion sensor status: {motion_sensor_status}.
    Provide recommendations to secure the vehicle.
    """
    face_recognition_result = "Authorized access"
    iot_data = {"door_sensor": "closed", "motion_sensor": "inactive"}

    # Run reasoning
    result = await run_vehicle_security_reasoning(reasoning_prompt, face_recognition_result, iot_data)

    # Assert the result
    assert "All systems are normal" in result
    print("Test passed: Positive scenario works as expected.")

@pytest.mark.asyncio
async def test_vehicle_security_reasoning_negative():
    """
    Test case for a negative scenario where suspicious activity is detected.
    """
    # Mock inputs
    reasoning_prompt = """
    The vehicle is experiencing the following conditions:
    - Face recognition result: {face_recognition_result}.
    - Door sensor status: {door_sensor_status}.
    - Motion sensor status: {motion_sensor_status}.
    Provide recommendations to secure the vehicle.
    """
    face_recognition_result = "Unauthorized access detected"
    iot_data = {"door_sensor": "forced_open", "motion_sensor": "active"}

    # Run reasoning
    result = await run_vehicle_security_reasoning(reasoning_prompt, face_recognition_result, iot_data)

    # Assert the result
    assert "Alert" in result
    print("Test passed: Negative scenario works as expected.")