from src.database.config import supabase
import bcrypt
from functools import lru_cache
from postgrest.exceptions import APIError
def check_teacher_exists(username: str) -> bool:
    response = supabase.table("teachers").select("username").eq("username", username).execute()
    return len(response.data) > 0
def create_teacher(username: str, name: str, password: str) -> bool:
    if check_teacher_exists(username):
        return False
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    supabase.table("teachers").insert({"username": username, "name": name, "password": hashed_password.decode('utf-8')}).execute()
    return True
def teacher_login(username: str, password: str):
    response = supabase.table("teachers").select("*").eq("username", username).execute()

    if len(response.data) == 0:
        return None

    teacher = response.data[0]
    stored_hashed_password = teacher["password"].encode('utf-8')

    if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
        return teacher

    return None
def get_all_students():
    response = supabase.table("students").select("*").execute()
    return response.data


@lru_cache(maxsize=1)
def students_auth_supported() -> bool:
    try:
        supabase.table("students").select("username,password").limit(1).execute()
        return True
    except APIError as e:
        if getattr(e, "code", None) == "42703":
            return False
        raise


def check_student_exists(username: str) -> bool:
    if students_auth_supported():
        response = supabase.table("students").select("username").eq("username", username).execute()
        return len(response.data) > 0
    # Fallback for schema without username column.
    response = supabase.table("students").select("name").eq("name", username).execute()
    return len(response.data) > 0


def student_login(username: str, password: str):
    if not students_auth_supported():
        return None
    response = supabase.table("students").select("*").eq("username", username).execute()
    if len(response.data) == 0:
        return None

    student = response.data[0]
    stored_hashed_password = student.get("password")
    if not stored_hashed_password:
        return None

    # Preferred path: bcrypt hash verification.
    try:
        if bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password.encode("utf-8")):
            return student
    except ValueError:
        # Backward compatibility: some existing rows may store plain-text password.
        # If plain-text matches, transparently upgrade it to bcrypt.
        if stored_hashed_password == password:
            new_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            supabase.table("students").update({"password": new_hash}).eq("student_id", student["student_id"]).execute()
            student["password"] = new_hash
            return student
    return None


def create_student(new_name, username=None, password=None, face_embedding=None, voice_embedding=None):
    payload = {
        "name": new_name,
        "face_embedding": face_embedding,
        "voice_embedding": voice_embedding,
    }
    if students_auth_supported() and username and password:
        if check_student_exists(username):
            return None
        payload["username"] = username
        payload["password"] = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    res = supabase.table("students").insert(payload).execute()
    return res.data


def get_teacher_subjects(teacher_id):
    try:
        response = (
            supabase.table("subjects")
            .select("*")
            .eq("teacher_id", teacher_id)
            .order("created_at", desc=True)
            .execute()
        )
        data = response.data or []
        normalized = []
        for row in data:
            item = dict(row)
            item.setdefault("subject_code", item.get("code", "NA"))
            item.setdefault("code", item.get("subject_code", "NA"))
            item.setdefault("section", "C")
            item.setdefault("total_students", 0)
            item.setdefault("total_classes", 0)
            normalized.append(item)
        return normalized
    except APIError:
        # Allows UI to continue even if subjects table is not yet created.
        return []


def get_teacher_subject(teacher_id):
    return get_teacher_subjects(teacher_id)


def create_subject(teacher_id, subject_name, subject_code=None):
    clean_name = subject_name.strip()
    clean_code = (subject_code or "").strip().upper()
    if not clean_code:
        clean_code = f"{clean_name[:3].upper()}-001" if clean_name else "SUB-001"

    payload = {
        "teacher_id": teacher_id,
        "name": clean_name,
        "subject_code": clean_code,
        "section": "C",
    }

    response = supabase.table("subjects").insert(payload).execute()
    return response.data
def enroll_student_to_subject(student_id, subject_id):
    payload = {
        "student_id": student_id,
        "subject_id": subject_id,
    }
    response = supabase.table("subject_students").insert(payload).execute()
    return response.data
def unenroll_student_from_subject(student_id, subject_id):
    response = supabase.table("subject_students").delete().eq("student_id", student_id).eq("subject_id", subject_id).execute()
    return response.data
def get_student_subjects(student_id):
    response = (
        supabase.table("subject_students")
        .select("*,subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )
    return response.data
def get_student_attendance(student_id):
    response = (
        supabase.table("attendance_logs")
        .select("*,subjects(*)")
        .eq("student_id", student_id)
        .execute()
    )
    return response.data