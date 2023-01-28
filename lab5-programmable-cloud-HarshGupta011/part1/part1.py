#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth
credentials, project = google.auth.default()
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


def create_instance(compute, project, zone, name):
    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-2204-lts').execute()
    source_disk_image = image_response['selfLink']

    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'startup-script.sh'), 'r').read()

    config = {
        'name': name,
        'machineType': machine_type,

        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        'metadata': {
            'items': [{
                'key': 'startup-script',
                'value': startup_script
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()

def delete_instance(compute, project, zone, name):
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()

def wait_for_operation(compute, project, zone, operation):
    print('Waiting for operation to finish...')
    while True:
        result = compute.zoneOperations().get(
            project=project,
            zone=zone,
            operation=operation).execute()

        if result['status'] == 'DONE':
            print("done.")
            if 'error' in result:
                raise Exception(result['error'])
            return result

        time.sleep(1)

print('Creating instance.')
project = "datacenterlab5-365403"
zone = "us-west1-b"
instance_name = "part1"

operation = create_instance(service, project, zone, instance_name)
wait_for_operation(service, project, zone, operation['name'])

instances = list_instances(service, project, zone)
firewall_body = {
    "name":'allow-5000',
    "description": 'firewall to allow TCP port 5000 to be accessed from anywhere ',
    "targetTags": ["allow-5000"],
    "allowed": [
    {
        "ports": [5000],
        "IPProtocol": "TCP"
    }
    ],
    "direction": "INGRESS"
}
firewalls_list = service.firewalls().list(project = project)
list_of_firewalls = firewalls_list.execute()
names_of_firewalls = []
if "items" in list_of_firewalls:
    for firewall in list_of_firewalls["items"]:
        names_of_firewalls.append(firewall["name"])

if("allow-5000" not in names_of_firewalls):
    request = service.firewalls().insert(project=project, body=firewall_body)
    response = request.execute()

request_instance = service.instances().get(project=project, zone=zone, instance=instance_name)
response_instance = request_instance.execute()
fingerprint = response_instance["tags"]["fingerprint"]
tags_body = {
    "items":["allow-5000"],
    "fingerprint": fingerprint
}
print(f"Go to http://{response_instance['networkInterfaces'][0]['accessConfigs'][0]['natIP']}:5000 to visit the flask app")

request = service.instances().setTags(project=project, zone=zone, instance=instance_name, body=tags_body)
response = request.execute()

input("Press any key to abort")
print('Deleting instance.')
operation = delete_instance(service, project, zone, instance_name)
wait_for_operation(service, project, zone, operation['name'])