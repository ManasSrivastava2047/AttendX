import numpy as np
import dlib
import face_recognition_models
import streamlit as st
from sklearn.svm import SVC
from src.database.db import get_all_students


def _normalize_embedding(embedding):
    if embedding is None:
        return None

    emb = np.array(embedding, dtype=np.float64)

    # Handles legacy nested storage like [[...128 values...]].
    if emb.ndim == 2 and emb.shape[0] == 1:
        emb = emb[0]
    elif emb.ndim > 1:
        emb = emb.reshape(-1)

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


def get_trained_model():
    students = get_all_students()
    X = []
    y = []

    for student in students:
        embedding = student.get('face_embedding')
        if embedding:
            normalized_embedding = _normalize_embedding(embedding)
            if normalized_embedding is not None and normalized_embedding.size > 0:
                X.append(normalized_embedding)
                y.append(student.get('student_id'))

    if len(X) == 0:
        return None  # ✅ better than 0

    X = np.array(X, dtype=np.float64)

    model = SVC(kernel='linear', probability=True, class_weight='balanced')

    try:
        model.fit(X, y)
    except ValueError as e:
        print(f"Error training face classifier: {e}")
        return None

    # ✅ FIXED DICTIONARY
    return {"clf": model, "X": X, "y": y}


def train_classifier():
    st.cache_resource.clear()
    model = get_trained_model()
    return bool(model)


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)
    detected_students = {}

    model_data = get_trained_model()

    if not model_data:
        st.warning("No face data available for training. Please ensure students have registered their faces.")
        return detected_students, [], len(encodings)

    # ✅ FIXED ACCESS (dict, not function)
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']

    all_students = sorted(list(set(y_train)))

    if not all_students:  # ✅ safety check
        return detected_students, [], len(encodings)

    for encoding in encodings:
        encoding = _normalize_embedding(encoding)
        if encoding is None or encoding.size == 0:
            continue

        if len(all_students) >= 2:
            predicted_id = int(clf.predict([encoding])[0])
        else:
            predicted_id = int(all_students[0])

        student_embedding = X_train[y_train.index(predicted_id)]
        best_match_score = np.linalg.norm(student_embedding - encoding)

        resemblance_threshold = 0.6

        if best_match_score < resemblance_threshold:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(encodings)