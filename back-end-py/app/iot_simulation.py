mock_iot_data = {
    "door_sensor": "closed",  # Possible values: "closed", "forced_open"
    "motion_sensor": "inactive"  # Possible values: "inactive", "active"
}

def simulate_iot_data(door_status, motion_status):
    """Simulate IoT sensor data."""
    mock_iot_data["door_sensor"] = door_status
    mock_iot_data["motion_sensor"] = motion_status
    return mock_iot_data