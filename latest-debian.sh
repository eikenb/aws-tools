#!/bin/sh

latest_debian_ami() {
    version=stretch
    aws --region us-west-2 ec2 describe-images --owners 379101102735 \
        --filters Name=name,Values=debian-$version-\* \
            Name=root-device-type,Values=ebs \
        --query 'Images[].[CreationDate,ImageId]' --output text \
        | sort | tail -1 | cut -f 2
}

