def simulate_iot_data(door_status="closed", motion_status="inactive", fingerprint_status="unknown"):
    """Simulate IoT sensor data with validation and default values."""
    valid_door_statuses = ["closed", "forced_open"]
    valid_motion_statuses = ["inactive", "active"]
    valid_fingerprint_statuses = ["authorized", "unauthorized", "unknown"]

    if door_status not in valid_door_statuses:
        raise ValueError(f"Invalid door_status: {door_status}")
    if motion_status not in valid_motion_statuses:
        raise ValueError(f"Invalid motion_status: {motion_status}")
    if fingerprint_status not in valid_fingerprint_statuses:
        raise ValueError(f"Invalid fingerprint_status: {fingerprint_status}")

    return {
        "door_sensor": door_status,
        "motion_sensor": motion_status,
        "fingerprint_status": fingerprint_status
    }