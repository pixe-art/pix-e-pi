import requests

def is_connected():
    try:
        r = requests.get("https://knark.club", timeout=10)
        if r.status_code == 200:
            return True
    except Exception as e:
        print("connectivity check failed:", e)
    return False