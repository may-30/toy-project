import boto3
import os
from datetime import datetime

# VARIABLES : lambda function environment
tag_name = os.environ['Tag_Name']
tag_value = os.environ['Tag_Value']
root_directory = os.environ['Root_Directory']
default_id = int(os.environ['Default_ID'])

# FUNCTION : delete efs access point
def delete_efs(username, efs_access_point_id):
    efs_client = boto3.client('efs')
    efs_response = efs_client.delete_access_point(
        AccessPointId=efs_access_point_id
    )
    
    time_log = datetime.now()
    print(f'[ {time_log.strftime("%Y-%m-%d %H:%M:%S")} ] [ ID : {username} ] {efs_access_point_id} is successfully deleted!')
    return

# FUNCTION : mount efs
def mount_efs(username, commands):
    # LOGIC : ec2 search
    ec2_client = boto3.client('ec2')
    ec2_response = ec2_client.describe_instances(
        Filters=[
            {
                'Name': f'tag:{tag_name}',
                'Values': [
                    f'{tag_value}'
                ]
            }
        ]
    )
    
    # LOGIC : ec2 search (status is running) and (instance id)
    instance_id = ""
    ec2_response_len = len(ec2_response['Reservations'])

    if ec2_response_len > 1:
        for i in range(0, ec2_response_len):
            if ec2_response['Reservations'][i]['Instances'][0]['State']['Name'] != 'running':
                continue
        
            instance_id = [ec2_response['Reservations'][i]['Instances'][0]['InstanceId']]
    else:
        instance_id = [ec2_response['Reservations'][0]['Instances'][0]['InstanceId']]
    
    # LOGIC : ssm document (AWS-RunShellScript)
    ssm_client = boto3.client('ssm')
    ssm_response = ssm_client.send_command(
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': commands},
        InstanceIds=instance_id,
    )
    
    time_log = datetime.now()
    print(f'[ {time_log.strftime("%Y-%m-%d %H:%M:%S")} ] [ ID : {username} ] {commands} is done!')
    return

def lambda_handler(event, context):
    username = event['detail']['userIdentity']['arn'].split('/')[-1]
    time_log = datetime.now()
    print(f'[ {time_log.strftime("%Y-%m-%d %H:%M:%S")} ] [ ID : {username} ] EFS Access Point Lambda Start!')
    
    uid = event['detail']['requestParameters']['posixUser']['uid']
    gid = event['detail']['requestParameters']['posixUser']['gid']
    secondary_gid = event['detail']['requestParameters']['posixUser']['secondaryGids'][0]
    path = event["detail"]["requestParameters"]["rootDirectory"]["path"]
    
    # LOGIC : compare uid, gid, secondary_gid with default_id
    if uid != default_id or gid != default_id or secondary_gid != default_id:
        efs_access_point_id = event['detail']['responseElements']['accessPointId']
        delete_efs(username, efs_access_point_id)
    
    commands = [f'mkdir -p {root_directory}{path} && chown -R {uid}:{gid} {root_directory}']
    mount_efs(username,commands)
    
    time_log = datetime.now()
    print(f'[ {time_log.strftime("%Y-%m-%d %H:%M:%S")} ] [ ID : {username} ] EFS Access Point Lambda Done!')
    return