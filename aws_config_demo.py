import boto3
Access_key_ID=''
Secret_access_key=''
region=''  


instanceId_A=[]  #A账户下的实例id
instanceId_B=[]  #B账户下的实例id
def lambda_handler(event, context):
    
    sig=event['detail']['configurationItemDiff']['changeType']
    ec2= boto3.client('ec2', region=region,aws_access_key_id=Access_key_ID,aws_secret_access_key=Secret_access_key)
    print('sig : ',sig)
    if sig=='CREATE':
        instanceId_A.append(event['detail']['configurationItem']['configuration']['instanceId'])
        responese=ec2.run_instances(InstanceType=event['detail']['configurationItem']['configuration']['instanceType'], 
                         MaxCount=1, 
                         MinCount=1, 
                         ImageId=event['detail']['configurationItem']['configuration']['imageId'])
        
        instanceId_B.append(responese['Instances'][0]['InstanceId'])
        print('instanceId_A : ',instanceId_A)
        print('instanceId_B : ',instanceId_B)
        
    elif sig=='DELETE':
        ins_id=event['detail']['configurationItemDiff']['changedProperties']['Configuration']['previousValue']['instanceId']
        print('ins_id :',ins_id)
        if ins_id in instanceId_A:
            pos=instanceId_A.index(ins_id)
            print('ins_id_pos : ',pos)
            ec2.terminate_instances(InstanceIds=[
                instanceId_B[pos]
            ])
            instanceId_A.pop(pos)
            instanceId_B.pop(pos)
            print('instanceId_A : ',instanceId_A)
            print('instanceId_B : ',instanceId_B)
    





