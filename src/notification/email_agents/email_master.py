#WorkflowTeamCodeStarted-3c48e1ed2f594049
import os
import logging
from flask import request
import requests
import datetime
import json

LOG_DIR = "/data/logs/3c48e1ed2f594049/"
LOG_FILE = os.path.join(LOG_DIR, "workflow.log")
os.makedirs(LOG_DIR, exist_ok=True)
# Creating output folder
os.makedirs("/data/output/3c48e1ed2f594049/", exist_ok=True)
logging.basicConfig(filename=LOG_FILE, filemode="a", format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

def main():
    logging.info("***************Workflow code is triggered***************")
    data = request.get_json(force=True)
    logging.info("request data: %s", data)

    user_id = data.get("user_id", "guest")
    FOLDER_NAME = "sample_audits"
    input_path = "/data/" + FOLDER_NAME
    org_group = data.get("org_group")
    output_path = "/data/output/3c48e1ed2f594049/"
    
    # Agent 1: File Reader Agent
    logging.info("Calling File Reader Agent")
    agent1_url = "http://router.accure-momentum.svc.cluster.local:80/3c48e1ed2f594049-1"
    agent1_request_data = {"input_path": input_path}
    agent1_response = requests.post(agent1_url, json=agent1_request_data)
    agent1_response_data = agent1_response.json()
    logging.info("Finished Calling File Reader Agent")
    if agent1_response_data.get("status") != "success":
        return {
            "status": "failed",
            "message": "File Reader Agent failed"
        }
    file_contents = agent1_response_data.get("file_contents")
    
    output_file_path = os.path.join(output_path,"input_text.json")
    
    with open(output_file_path,"w") as f:
        json.dump(file_contents,f,indent=4)
        
    # Agent 2: Compliance and Summarization Agent
    logging.info("Calling Compliance and Summarization Agent")
    agent2_url = "http://router.accure-momentum.svc.cluster.local:80/cognitive_agent_runner"
    agent2_request_data = {
        "prompt": data.get("2_prompt", ""),
        "input_data": file_contents
    }
    agent2_response = requests.post(agent2_url, json=agent2_request_data)
    agent2_response_json = agent2_response.json()
    logging.info("Finished Calling Compliance and Summarization Agent")
    if agent2_response_json.get("status") != "success":
        return {
            "status": "failed",
            "message": "Compliance and Summarization Agent failed"
        }
    compliance_status = agent2_response_json.get("response")
    output_file_path = os.path.join(output_path,"report.json")
    
    with open(output_file_path,"w") as f:
        json.dump(compliance_status,f,indent=4)
        
    # Agent 3: Email Summary Agent
    logging.info("Calling Email Summary Agent")
    agent3_url = "http://router.accure-momentum.svc.cluster.local:80/3c48e1ed2f594049-2"
    agent3_request_data = {"compliance_status": compliance_status}
    agent3_response = requests.post(agent3_url, json=agent3_request_data)
    agent3_response_json = agent3_response.json()
    logging.info("Finished Calling Email Summary Agent")
    if agent3_response_json.get("status") != "success":
        return {
            "status": "failed",
            "message": "Email Summary Agent failed"
        }
    return {
        "status": "success"
    }
#WorkflowTeamCodeEnded-3c48e1ed2f594049