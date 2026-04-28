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

    if bcrypt.checkpw(password.encode("utf-8"), stored_hashed_password.encode("utf-8")):
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