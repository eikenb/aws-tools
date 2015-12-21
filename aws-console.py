#!/usr/bin/env python

# Python 2 and Python 3 compatible.

# Requires base python install + requests module.
# http://docs.python-requests.org/en/latest/

import argparse
import json
import os
import requests
import webbrowser
import boto.iam
from boto.sts import STSConnection

import urllib
# Python 3 compatibility (python 3 has urlencode in parse sub-module)
urlencode = getattr(urllib, 'parse', urllib).urlencode

# Requires this role to exist.
ROLE_NAME = "StsConsoleAccess"
# see ./add-sts-console-w-api/ for script to create this role using the API

def parseArgs():
    """ Do the argument parsing and return arg dict.
    """
    browser_name = webbrowser.get().name
    parser = argparse.ArgumentParser("Open " +
            browser_name + " to AWS console of account based on credentials.")
    # only chrom{e,ium} support incognito mode
    parser.add_argument('-i', '--incognito', action='store_true',
            help='Open browser in incognito/private mode.')

    return parser.parse_args()

_cache = []
def getArgs():
    """ Return ArgumentParser Namespace instance for parsed arguments.
    """
    if not _cache:
        _cache.append(parseArgs())
    return _cache[0]

def accountId():
    """ Return account-id based on credentials in environment.
    """
    # save the lookup if we set the account to the environment
    if os.environ.has_key("AWS_ACCOUNT_ID"):
        return os.environ["AWS_ACCOUNT_ID"]
    conn = boto.iam.connect_to_region("us-east-1")
    arn = conn.get_user().get('get_user_response')\
            .get('get_user_result').get('user').get('arn')
    return arn.split(':')[4]


def openConsole():
    """ Get STS token and open AWS console.
    """
    # Create an ARN out of the information provided by the user.
    role_arn = "arn:aws:iam::" + accountId() + ":role/" + ROLE_NAME

    # Connect to AWS STS and then call AssumeRole.
    # Returns temporary security credentials.
    sts_connection = STSConnection()
    assumed_role_object = sts_connection.assume_role(
        role_arn=role_arn,
        role_session_name="AssumeRoleSession"
    )

    # Format resulting credentials into a JSON block.
    tmp_creds = {
        "sessionId": assumed_role_object.credentials.access_key,
        "sessionKey": assumed_role_object.credentials.secret_key,
        "sessionToken": assumed_role_object.credentials.session_token,
    }
    json_temp_credentials = json.dumps(tmp_creds)

    # Make a request to the AWS federation endpoint to get a sign-in
    # token, passing parameters in the query string.
    params = {
        "Action": "getSigninToken",
            "Session": json_temp_credentials,
    }
    request_url = "https://signin.aws.amazon.com/federation"
    r = requests.get(request_url, params=params)

    # The return value from the federation endpoint, the token.
    sign_in_token = json.loads(r.text)["SigninToken"]
    # Token is good for 15 minutes.

    # Create the URL to the console with token.
    params = {
        "Action": "login",
        "Issuer": "",
        "Destination": "https://console.aws.amazon.com/",
        "SigninToken": sign_in_token,
    }
    request_url = "https://signin.aws.amazon.com/federation?"
    request_url += urlencode(params)

    # Use the default browser to sign in to the console using the
    # generated URL.
    browser = webbrowser.get()
    if getArgs().incognito:
        webbrowser.Chromium.raise_opts = ["", "--incognito"]
        webbrowser.Chrome.raise_opts = ["", "--incognito"]
        webbrowser.Mozilla.remote_args = ['--private-window', '%s']
    browser.open(request_url, new=1)

if __name__ == "__main__":
    openConsole()

