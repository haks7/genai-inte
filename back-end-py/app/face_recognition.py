mock_face_db = {
    "authorized_faces": ["owner_face_id_1", "owner_face_id_2"],
    "unauthorized_attempts": []
}

def recognize_face(face_id):
    """Mock face recognition."""
    if face_id in mock_face_db["authorized_faces"]:
        return True, "Authorized access"
    else:
        mock_face_db["unauthorized_attempts"].append(face_id)
        return False, "Unauthorized access detected"