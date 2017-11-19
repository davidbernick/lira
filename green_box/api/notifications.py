import connexion
import logging
import json
import time
from flask import current_app
from green_box_utils import gcs_utils
from green_box_utils import cromwell_utils
from green_box_utils import listener_utils
import read_utils

def post(body):
    # Check authentication
    logger = logging.getLogger('green-box')
    green_config = current_app.config

    if not listener_utils.is_authenticated(connexion.request.args, green_config.notification_token):
        time.sleep(1)
        return listener_utils.response_with_server_header(dict(error='Unauthorized'), 401)

    logger.info("Notification received")
    logger.info(body)

    # Get bundle uuid, version and subscription_id
    uuid, version, subscription_id = listener_utils.extract_uuid_version_subscription_id(body)

    # Find wdl config where the subscription_id matches the notification's subscription_id
    id_matches = [wdl for wdl in green_config.wdls if wdl.subscription_id == subscription_id]
    if len(id_matches) == 0:
        return listener_utils.response_with_server_header(
            dict(error='Not Found: No wdl config found with subscription id {}'
                       ''.format(subscription_id)), 404)
    wdl = id_matches[0]
    logger.info(wdl)
    logger.info('Launching {0} workflow in Cromwell'.format(wdl.workflow_name))

    # Prepare inputs
    inputs = listener_utils.compose_inputs(wdl.workflow_name, uuid, version)
    cromwell_inputs_file = json.dumps(inputs)

    # Read files into memory
    wdl_file = read_utils.download(wdl.wdl_link)
    wdl_default_inputs_file = read_utils.download(wdl.wdl_default_inputs_link)
    options_file = read_utils.download(wdl.options_link)

    # Create zip of analysis and submit wdls
    url_to_contents = read_utils.download_to_map([wdl.analysis_wdl, green_config.submit_wdl])
    wdl_deps_file = read_utils.make_zip(url_to_contents)

    cromwell_response = cromwell_utils.start_workflow(
        wdl_file, wdl_deps_file, cromwell_inputs_file,
        wdl_default_inputs_file, options_file, green_config)

    # Respond
    if cromwell_response.status_code > 201:
        logger.error(cromwell_response.text)
        return listener_utils.response_with_server_header(dict(result=cromwell_response.text), 500)
    logger.info(cromwell_response.json())
    return listener_utils.response_with_server_header(cromwell_response.json())
