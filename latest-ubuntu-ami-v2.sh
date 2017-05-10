#!/bin/sh

remove_last_comma() { sed '
        $x;$G;/\(.*\),/!H;//!{$!d
    };  $!x;$s//\1/;s/^\n//'
}

curl -s "https://cloud-images.ubuntu.com/locator/ec2/releasesTable" \
    | remove_last_comma \
    | jq -c '.aaData[] | select(contains(["16.04", "us-west-2", "hvm:ebs"]))' \
    | grep -o 'ami-[a-z0-9]\+' | head -1

