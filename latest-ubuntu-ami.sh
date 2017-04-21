#!/bin/sh

# Simple shell script to fetch latest ubuntu AMI I find handy currently.
# Probably still end up going to alestic.com, but for when I need to script it.

name=$(\
    aws --region us-west-2 ec2 describe-images --owners 099720109477 \
        --filters Name=root-device-type,Values=ebs \
            Name=architecture,Values=x86_64 \
            Name=name,Values='*hvm-ssd/ubuntu-xenial-16.04-amd64*' \
    | awk -F ': ' '/"Name"/ { print $2 | "sort" }' \
    | tr -d '",' | tail -1)

ami_id=$(\
    aws --region us-west-2 ec2 describe-images --owners 099720109477 \
        --filters Name=name,Values="$name" \
        --query "Images[0].ImageId" --output "text")

echo "Latest AMI: $ami_id"
