#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth
import google.oauth2.service_account as service_account

# pip install google-api-python-client
credentials = service_account.Credentials.from_service_account_file(filename='servicecredentials.json')
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)

#
# Stub code - just lists all instances
#
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None


def create_instance(compute, project, zone, name, bucket):
    # Get the latest Debian Jessie image.
    image_response = compute.images().getFromFamily(
        project='ubuntu-os-cloud', family='ubuntu-2204-lts').execute()
    source_disk_image = image_response['selfLink']

    # Configure the machine
    machine_type = "zones/%s/machineTypes/f1-micro" % zone
    startup_script = open(
        os.path.join(
            os.path.dirname(__file__), 'vm2startupscript.sh'), 'r').read()
    image_url = "http://storage.googleapis.com/gce-demo-input/photo.jpg"
    image_caption = "Ready for dessert?"

    config = {
        'name': name,
        'machineType': machine_type,

        # Specify the boot disk and the image to use as a source.
        'disks': [
            {
                'boot': True,
                'autoDelete': True,
                'initializeParams': {
                    'sourceImage': source_disk_image,
                }
            }
        ],

        # Specify a network interface with NAT to access the public
        # internet.
        'networkInterfaces': [{
            'network': 'global/networks/default',
            'accessConfigs': [
                {'type': 'ONE_TO_ONE_NAT', 'name': 'External NAT'}
            ]
        }],

        # Allow the instance to access cloud storage and logging.
        'serviceAccounts': [{
            'email': 'default',
            'scopes': [
                'https://www.googleapis.com/auth/devstorage.read_write',
                'https://www.googleapis.com/auth/logging.write'
            ]
        }],

        # Metadata is readable from the instance and allows you to
        # pass configuration from deployment scripts to instances.
        'metadata': {
            'items': [{
                # Startup script is automatically executed by the
                # instance upon startup.
                'key': 'startup-script',
                'value': startup_script
            }, {
                'key': 'url',
                'value': image_url
            }, {
                'key': 'text',
                'value': image_caption
            }, {
                'key': 'bucket',
                'value': bucket
            }]
        }
    }

    return compute.instances().insert(
        project=project,
        zone=zone,
        body=config).execute()
# [END create_instance]


# [START delete_instance]
def delete_instance(compute, project, zone, name):
    return compute.instances().delete(
        project=project,
        zone=zone,
        instance=name).execute()
# [END delete_instance]


# [START wait_for_operation]
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
# [END wait_for_operation]

print('Creating instance.')

# project = input("Project ID = ")
project = "datacenterlab5-365403"
zone = "us-west1-b"
instance_name = "part2"
bucket= "part2"
# instance_name = input("Instance name = ")
# bucket = input("bucket_name = ")

operation = create_instance(service, project, zone, instance_name, bucket)
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