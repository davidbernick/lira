import connexion
import requests
from requests.auth import HTTPBasicAuth
import logging
import json
import subprocess
import green_config
import time

def post(body):
    # Check authentication
    if not is_authenticated(connexion.request.args, green_config.notification_token):
        time.sleep(1)
        return None, 401

    logger = logging.getLogger('green-box')
    logger.info("Notification received")
    logger.info(body)

    # Get bundle uuid and version
    uuid, version = extract_uuid_version(body)

    # Prepare inputs
    inputs = compose_inputs(uuid, version, green_config.provenance_script)
    with open('cromwell_inputs.json', 'w') as f:
        json.dump(inputs, f)

    # Start workflow
    logger.info("Launching smartseq2 workflow in Cromwell")
    result = subprocess.check_output(['gsutil', 'cp', green_config.mock_smartseq2_wdl, '.'])
    response = start_workflow('mock_smartseq2.wdl', 'cromwell_inputs.json')

    # Respond
    if response.status_code > 201:
        logger.error(response.text)
        return json.dumps(dict(result=response.text)), 500
    logger.info(response.json())
    return dict(result=response.json())

def is_authenticated(args, token):
    if not 'auth' in args:
        return False
    elif args['auth'] != token:
        return False
    return True

def extract_uuid_version(msg):
    uuid = msg["match"]["bundle_uuid"]
    version = msg["match"]["bundle_version"]
    return uuid, version

def compose_inputs(uuid, version, provenance_script):
    inputs = {}
    inputs['mock_smartseq2.bundle_uuid'] = uuid
    inputs['mock_smartseq2.bundle_version'] = '"{0}"'.format(version)
    inputs['mock_smartseq2.provenance_script'] = provenance_script
    return inputs

def start_workflow(wdl, inputs):
    with open('mock_smartseq2.wdl', 'rb') as wdl, open('cromwell_inputs.json', 'rb') as inputs:
        files = {
          'wdlSource': wdl,
          'workflowInputs': inputs
        }
        response = requests.post(green_config.cromwell_url, files=files, auth=HTTPBasicAuth(green_config.cromwell_user, green_config.cromwell_password))
        return response
