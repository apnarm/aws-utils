import re

import boto.ec2
import boto.vpc
import boto.route53


class EC2(object):

    def __init__(self, environment, security_group):
        self.environment = environment
        self.security_group = security_group

        instance_metadata = boto.utils.get_instance_metadata()

        self.instance_id = instance_metadata['instance-id']
        self.aws_zone = instance_metadata['placement']['availability-zone']
        self.aws_region = re.sub(r'[ab]$', '', self.aws_zone)

        self.ec2 = boto.ec2.connect_to_region(self.aws_region)
        self.vpc = boto.vpc.connect_to_region(self.aws_region)
        self.route53 = boto.route53.Route53Connection()
