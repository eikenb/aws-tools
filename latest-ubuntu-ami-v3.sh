#!/bin/sh

latest_ubuntu_ami() {
    version=zesty
    case "$1" in
        lts) version=xenial ;;
        bionic|artful|zesty|yakkety|xenial) version="$1" ;;
    esac
    aws --region us-west-2 ec2 describe-images --owners 099720109477 \
        --filters Name=name,Values=\*/ubuntu-$version-\* \
            Name=root-device-type,Values=ebs \
        --query 'Images[].[CreationDate,ImageId]' --output text \
        | sort | tail -1 | cut -f 2
}

