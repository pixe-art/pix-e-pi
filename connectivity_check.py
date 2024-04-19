import requests

def is_connected():
    try:
        r = requests.get("http://192.168.1.157:1180", timeout=10)
        if r.status_code == 200:
            return True
    except Exception as e:
        print("connectivity check failed:", e)
    return False

print("a")
is_connected()
print("b")