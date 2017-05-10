#!/bin/sh

build=stable     # stable, beta, alpha
disk=hvm         # pv, hvm
region=us-west-2 # https://docs.aws.amazon.com/general/latest/gr/rande.html

[ -n "$1" ] && region="$1"

#### deprecated
#ami_id=$(curl --silent http://$build.release.core-os.net/amd64-usr/current/coreos_production_ami_all.json | grep -A 2 $1 | grep $disk | cut -d"\"" -f4)

#### Source from coreos.com now (h/t cswong)
ami_id=$(curl --silent https://coreos.com/dist/aws/aws-$build.json \
    | jq ".[\"$region\"][\"$disk\"]" | tr -d '"')

# jq can return null for failed lookups
[ -z "$ami_id" ] || [ "$ami_id" = "null" ] \
    && echo "ERROR: $region, $build, $disk, CoreOS AMI doesn't exist." \
    && exit 1

echo $ami_id
