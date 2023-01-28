#!/bin/bash


apt-get update
apt-get -y install imagemagick

# Use the metadata server to get the configuration specified during
# instance creation. Read more about metadata here:
# https://cloud.google.com/compute/docs/metadata#querying
IMAGE_URL=$(curl http://metadata/computeMetadata/v1/instance/attributes/url -H "Metadata-Flavor: Google")
TEXT=$(curl http://metadata/computeMetadata/v1/instance/attributes/text -H "Metadata-Flavor: Google")
CS_BUCKET=$(curl http://metadata/computeMetadata/v1/instance/attributes/bucket -H "Metadata-Flavor: Google")

mkdir image-output
cd image-output
wget $IMAGE_URL
convert * -pointsize 30 -fill white -stroke black -gravity center -annotate +10+40 "$TEXT" output.png

# Create a Google Cloud Storage bucket.
gsutil mb gs://$CS_BUCKET

# Store the image in the Google Cloud Storage bucket and allow all users
# to read it.
gsutil cp -a public-read output.png gs://$CS_BUCKET/output.png

sudo apt-get update
sudo apt-get install -y python3 python3-pip
curl http://metadata/computeMetadata/v1/instance/attributes/vm2-startup-script -H "Metadata-Flavor: Google" > vm2startupscript.sh
curl http://metadata/computeMetadata/v1/instance/attributes/service-credentials -H "Metadata-Flavor: Google" > servicecredentials.json
curl http://metadata/computeMetadata/v1/instance/attributes/vm1-launch-vm2-code -H "Metadata-Flavor: Google" > vm1launchvm2code.py
pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
python3 ./vm1launchvm2code.py