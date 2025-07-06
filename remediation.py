import os
from config import CONTAINER_NAME

def remediate():
    os.system("docker restart stress-test")
    return "Restarted stress-test"

