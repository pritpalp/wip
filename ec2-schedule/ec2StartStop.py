import boto3

# Define the region here, we use this to get the instances
region = 'eu-west-2'

# ec2 var to execute the stop/start commands,
# resource to get the instance descriptions including id's
ec2 = boto3.client('ec2', region_name=region)
resource = boto3.resource('ec2')

def lambda_handler(event, context):
    # get the option from the calling schedule
    action = event["action"]
    # loop through the instance collection getting the id's
    # and stopping/starting the instances
    for instance in resource.instances.all():
        instance_id = instance.id
        if action == "stop":
            ec2.stop_instances(InstanceIds=[instance_id])
        else:
            ec2.start_instances(InstanceIds=[instance_id])
        print(action + ' your instance: ' + instance_id)