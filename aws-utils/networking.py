from . import EC2


class Network(EC2):

    def __init__(self, environment, security_group):
        self.eni = None
        self.enis = []

        super(Network, self).__init__(environment, security_group)

    def setup(self):
        self.enis = self.enis_for_security_group()
        self.eni = self.instance_assigned_eni(self.enis)

        if not self.eni:
            self.eni = self.assign_eni(self.enis)
        else:
            print 'Using already assigned ENI:%s on EC2:%s instance' % (self.eni, self.instance_id)

    def enis_for_security_group(self):
        filters = {
            'tag:Env': self.environment,
            'group-name': self.security_group,
        }
        return self.ec2.get_all_network_interfaces(filters=filters, dry_run=False)

    def get_private_subnets_for_env(self):
        filters = {
            'tag:Env': self.environment,
            'tag:Type': 'private'
        }
        return self.vpc.get_all_subnets(filters=filters)

    def availability_zones_for_region(self, region):
        return self.ec2.get_all_zones(filters={'region_name': region})

    def subnet_for_enis(self, enis):
        subnet_ids = [eni.subnet_id for eni in enis]
        return self.vpc.get_all_subnets(subnet_ids=subnet_ids)

    def instance_assigned_eni(self, enis):
        for eni in enis:
            if eni.attachment and \
               eni.attachment.instance_id == self.instance_id:
                return eni
        return None

    def available_enis(self, enis):
        available = []

        for eni in enis:
            if eni.availability_zone == self.aws_zone and \
               eni.status == 'available':
                available.append(eni)

        return available

    def assign_eni(self, enis):

        eni = None
        available_enis = self.available_enis(enis)

        if not available_enis:
            print "No free network devices (eni's) to assign to this EC2 instance."

        else:
            eni = available_enis[0]
            print "Attaching ENI:%s to EC2:%s instance" % (eni.id, self.instance_id)

            device_index = 1
            self.ec2.attach_network_interface(eni.id, self.instance_id, device_index, dry_run=False)

        return eni
