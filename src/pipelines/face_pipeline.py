import numpy as np
import dlib
import face_recognition_models
import streamlit as st
from src.database.db import get_all_students

# dlib/face_recognition default same-person cutoff. Keep this so true matches still pass.
RESEMBLANCE_THRESHOLD = 0.6
# Reject when best and 2nd-best are too close (ambiguous / likely stranger).
MIN_MATCH_MARGIN = 0.1


def _normalize_embedding(embedding):
    if embedding is None:
        return None

    emb = np.array(embedding, dtype=np.float64)

    # Handles legacy nested storage like [[...128 values...]].
    if emb.ndim == 2 and emb.shape[0] == 1:
        emb = emb[0]
    elif emb.ndim > 1:
        emb = emb.reshape(-1)

    if emb.size == 0:
        return None
    return emb


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(face_recognition_models.pose_predictor_model_location())
    facerec = dlib.face_recognition_model_v1(face_recognition_models.face_recognition_model_location())
    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()
    faces = detector(image_np, 1)

    encodings = []
    for face in faces:
        shape = sp(image_np, face)
        face_descriptor = facerec.compute_face_descriptor(image_np, shape, 1)
        encodings.append(np.array(face_descriptor))

    return encodings


@st.cache_resource
def get_face_gallery():
    """Gallery of enrolled face embeddings for nearest-neighbor matching."""
    students = get_all_students()
    X = []
    y = []

    for student in students:
        normalized_embedding = _normalize_embedding(student.get("face_embedding"))
        if normalized_embedding is not None:
            X.append(normalized_embedding)
            y.append(int(student.get("student_id")))

    if len(X) == 0:
        return None

    return {"X": np.array(X, dtype=np.float64), "y": y}


def get_trained_model():
    """Backward-compatible alias used by train_classifier / callers."""
    return get_face_gallery()


def train_classifier():
    st.cache_resource.clear()
    return get_face_gallery() is not None


def _match_face(encoding, X_train, y_train):
    """
    Nearest-neighbor match with distance + margin checks.
    Returns student_id or None if unknown / ambiguous.
    """
    distances = np.linalg.norm(X_train - encoding, axis=1)
    best_idx = int(np.argmin(distances))
    best_dist = float(distances[best_idx])

    if best_dist >= RESEMBLANCE_THRESHOLD:
        return None

    if len(distances) >= 2:
        second_dist = float(np.partition(distances, 1)[1])
        if (second_dist - best_dist) < MIN_MATCH_MARGIN:
            return None

    return int(y_train[best_idx])


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}

    gallery = get_face_gallery()
    if not gallery:
        st.warning("No face data available for training. Please ensure students have registered their faces.")
        return detected_students, [], len(encodings)

    X_train = gallery["X"]
    y_train = gallery["y"]
    all_students = sorted(set(y_train))

    if not all_students:
        return detected_students, [], len(encodings)

    for encoding in encodings:
        encoding = _normalize_embedding(encoding)
        if encoding is None:
            continue
        if encoding.shape[0] != X_train.shape[1]:
            continue

        predicted_id = _match_face(encoding, X_train, y_train)
        if predicted_id is not None:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)
