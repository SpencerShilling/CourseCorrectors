#AgentCodeStarted
import os
import logging
from flask import request

LOG_DIR = "/data/logs/3c48e1ed2f594049/3c48e1ed2f594049_1"
LOG_FILE = os.path.join(LOG_DIR, "3c48e1ed2f594049-1.log")
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs("/data/output/3c48e1ed2f594049", exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

def main():
    try:
        logging.info("***************File Reader Agent triggered***************")
        data = request.get_json(force=True)
        logging.info("Request Data %s", data)
        input_path = data.get("input_path")

        with open(input_path + "/example_audit_report2.txt", 'r') as f:
            file_contents = f.read()

        logging.info("Agent finished reading file")
        output = {
            "status": "success",
            "file_contents": file_contents
        }
        return output
    except Exception as e:
        logging.error("Exception: %s", str(e))
        return {
            "status": "error",
            "message": str(e)
        }
#AgentCodeEnded