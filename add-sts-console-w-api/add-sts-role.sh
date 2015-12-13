#!/bin/sh
# create StsConsoleAccess role for use with aws_console.py script

# script requires; awscli, jq (debian packages)

set -e

# Get our account-id based on loaded AWS creds
[ -n "$AWS_ACCESS_KEY" ] || { echo "No AWS credentials found."; exit 1; }
accountid=$(aws iam get-user | jq '.User.Arn' | cut -d: -f 5)

# create assume-policy.json with account-id
assume_policy=$(mktemp)
sed "s/XXXXXXXXXXXX/$accountid/" ./assume-policy.json > $assume_policy
trap "rm -f $assume_policy" 0 1

# add role with assume policy
aws iam create-role --role-name StsConsoleAccess \
    --assume-role-policy-document file://$assume_policy

## give role admin rights
aws iam put-role-policy --role-name StsConsoleAccess \
    --policy-name Admin --policy-document file://admin-role.json

