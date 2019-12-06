# Start/Stop EC2 instances on a Schedule

## Components

* Lambda Function
* IAM Policy
* IAM Role
* CloudWatch Logs
* CloudWatch Schedule

## How To

As you can see from the component list there are a few elements to set up. But it's all relatively simple.

### Set up IAM

An IAM policy and role need to be created. The policy dictates what access the Lambda function will have and the role applies the policy to the Lambda function when we create it.

#### IAM Policy

1. Log into AWS Console
2. Open the IAM Dashboard
3. Select Policy on the left hand side menu
4. Click 'Create policy'
5. Click 'JSON'
6. Paste in the JSON from below and click 'Review' in the botom right corner
7. Give it a name and description and click 'Create policy' in the botom right corner

```JSON
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ec2:DescribeInstances",
                "ec2:Start*",
                "ec2:Stop*"
            ],
            "Resource": "*"
        }
    ]
}
```

#### IAM Role

1. In the IAM Dashboard, click Roles
2. Click 'Create role'
3. Select 'Lambda'
4. Select 'Next: Permissions'
5. Type in the name of the Policy that you created, select it and click 'Next: Tags'
6. Add any tags you need, click 'Next: Review'
7. Give the Role a name and description and click 'Create role' in the botom left

### Create the Lambda funstions

We create two functions, one to stop and one to start.
The code is very similar between the two (just the start_instances and stop_instances mehods and log message that are different)
The code pulls a list of the ec2 resources and creates a client to execute commands with. The list of resources is used to loop through and use the instance id to stop/start the instance.

#### Start Function

1. Go to the Lambda Dashboard
2. Click 'Create function'
3. Give the function a name eg 'startEC2Instances'
4. Select the Python 3.7 runtime
5. Under permissions, change Execution role to 'Use and existing role' and select the role created in the previous step
6. Click 'Create function'
7. Scroll to the Function Code window and paste in the Python code below (start function)
8. Note the region variable, change to suit the region you are using
9. Click 'Save'

```Python
import boto3

# Define the region here, we use this to get the instances
region = 'eu-west-2'

# ec2 var to execute the stop/start commands,
# resource to get the instance descriptions including id's
ec2 = boto3.client('ec2', region_name=region)
resource = boto3.resource('ec2')

def lambda_handler(event, context):
    # loop through the instance collection getting the id's
    # and stopping/starting the instances
    for instance in resource.instances.all():
        instance_id = instance.id
        ec2.start_instances(InstanceIds=[instance_id])
        # msg for the cloudwatch log
        print('start your instance: ' + instance_id)
```

#### Stop Function

Repeat the steps above to create a new function, but use the code below for the stop function

```Pyhton
import boto3

# Define the region here, we use this to get the instances
region = 'eu-west-2'

# ec2 var to execute the stop/start commands,
# resource to get the instance descriptions including id's
ec2 = boto3.client('ec2', region_name=region)
resource = boto3.resource('ec2')

def lambda_handler(event, context):
    # loop through the instance collection getting the id's
    # and stopping/starting the instances
    for instance in resource.instances.all():
        instance_id = instance.id
        ec2.stop_instances(InstanceIds=[instance_id])
        # msg for the cloudwatch log
        print('stop your instance: ' + instance_id)
```

### CloudWatch Schedule

To run the functions on a schedule we can do that within CloudWatch. Two schedules are needed, one to start and one to stop the instances.

1. Go to the CloudWatch Dashboard
2. Select 'Rules' under 'Events'
3. Click 'Create rule'
4. Select 'Schedule' and switch to 'Cron expression'
5. Enter the cron expression eg to run every Mon-Fri at 7am you'd add `0 7 ? * MON-FRI *`
6. Click 'Add target'
7. Select 'Lambda function' from the drop down
8. Select your function from the drop down
9. Click 'Configure details'
10. Give a name and description and click 'Create rule'
11. Repeat for the other schedule.

