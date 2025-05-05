def simulate_iot_data(door_status="closed", motion_status="inactive", fingerprint_status="unknown"):
    """Simulate IoT sensor data with validation and default values."""
    valid_door_statuses = ["closed", "forced_open"]
    valid_motion_statuses = ["inactive", "active"]
    valid_fingerprint_statuses = ["authorized", "unauthorized", "unknown"]

    # Validate and fallback for door_status
    if door_status not in valid_door_statuses:
        print(f"Invalid door_status: {door_status}. Defaulting to 'closed'.")
        door_status = "closed"

    # Validate and fallback for motion_status
    if motion_status not in valid_motion_statuses:
        print(f"Invalid motion_status: {motion_status}. Defaulting to 'inactive'.")
        motion_status = "inactive"

    # Validate and fallback for fingerprint_status
    if fingerprint_status not in valid_fingerprint_statuses:
        print(f"Invalid fingerprint_status: {fingerprint_status}. Defaulting to 'unknown'.")
        fingerprint_status = "unknown"

    return {
        "door_sensor": door_status,
        "motion_sensor": motion_status,
        "fingerprint_status": fingerprint_status
    }