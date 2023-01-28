#!/usr/bin/env python3

import argparse
import os
import time
from pprint import pprint

import googleapiclient.discovery
import google.auth

credentials, project = google.auth.default()
service = googleapiclient.discovery.build('compute', 'v1', credentials=credentials)
project = "datacenterlab5-365403"
zone = "us-west1-b"
disk = "part1"
def list_instances(compute, project, zone):
    result = compute.instances().list(project=project, zone=zone).execute()
    return result['items'] if 'items' in result else None

print("Your running instances are:")
instances = list_instances(service, project, 'us-west1-b')
if instances: 
    for instance in instances:
        print(instance['name'])
    
def create_instance(compute, project, zone, name, snap):
    getSnapshot = compute.snapshots().get(project = project,snapshot = snap).execute()
    source_snap = getSnapshot['selfLink']
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
                    'sourceSnapshot': source_snap,
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
instance1="part21"
instance2="part22"
instance3="part23"
time_log = []

snapshot_body = { 'name' : 'base-snapshot-part1' }

request = service.disks().createSnapshot(project=project, zone=zone, disk=disk, body=snapshot_body)
response = request.execute()
pprint(response)

tstart1 = time.time()
operation1 = create_instance(service, project, zone, instance1, snapshot_body["name"])
wait_for_operation(service, project, zone, operation1['name'])
request_instance = service.instances().get(project=project, zone=zone, instance=instance1)
response_instance = request_instance.execute()
fingerprint = response_instance["tags"]["fingerprint"]
tags_body = {
    "items":["allow-5000"],
    "fingerprint": fingerprint
}
request = service.instances().setTags(project=project, zone=zone, instance=instance1, body=tags_body)
response = request.execute()
time_log.append(time.time() - tstart1)

tstart2 = time.time()
operation2 = create_instance(service, project, zone, instance2, snapshot_body["name"])
wait_for_operation(service, project, zone, operation2['name'])
request_instance = service.instances().get(project=project, zone=zone, instance=instance2)
response_instance = request_instance.execute()
fingerprint = response_instance["tags"]["fingerprint"]
tags_body = {
    "items":["allow-5000"],
    "fingerprint": fingerprint
}
request = service.instances().setTags(project=project, zone=zone, instance=instance2, body=tags_body)
response = request.execute()
time_log.append(time.time() - tstart2)

tstart3 = time.time()
operation3 = create_instance(service, project, zone, instance3, snapshot_body["name"])
wait_for_operation(service, project, zone, operation3['name'])
request_instance = service.instances().get(project=project, zone=zone, instance=instance3)
response_instance = request_instance.execute()
fingerprint = response_instance["tags"]["fingerprint"]
tags_body = {
    "items":["allow-5000"],
    "fingerprint": fingerprint
}
request = service.instances().setTags(project=project, zone=zone, instance=instance3, body=tags_body)
response = request.execute()
wait_for_operation(service, project, zone, operation3['name'])
time_log.append(time.time() - tstart3)

print("Time elapsed in creating 3 instances using snapshot are", time_log, "respectively.")
file_name = 'TIMING.md'
f = open(file_name, 'w+')
for i,t in enumerate(time_log):
    f.write(f'Time elapsed in creating instance {i+1} : {t}\n')
f.close()