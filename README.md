Collection of small tools for use with AWS. Added here to enable sharing.

aws-console.py + add-sts-role.sh
--------------------------------------
The aws-console.py script will launch a web browser to the AWS console using
your (boto accessible) API credentials. It requires a special role in your
account, the ./add-sts-console-w-api/add-sts-role.sh script will do this for
you.


grant-aws-access
------------------
This script will add your current IP to the security group for all ports. It
then waits for a key-press and proceeds to delete the IP from the security
group. This lets you grant yourself access temporarily from home without
leaving your (possibly changing) IP everywhere.

cf-invalidator
--------------
A few scripts thrown together to invalidate _large_ numbers of cloudfront
paths.

latest-ubuntu-ami.sh
--------------------
Shell snippet to get latest Ubuntu AMI. Handy for use with CI systems when you
are automating building AMIs.

