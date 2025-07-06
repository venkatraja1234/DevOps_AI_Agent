import subprocess

def fetch_logs():
    result = subprocess.getoutput("docker logs stress-test  --tail 100")
    return result
