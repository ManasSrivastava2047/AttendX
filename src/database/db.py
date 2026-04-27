from src.database.config import supabase
import bcrypt
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