import boto3
import json


#Get the list of resources from CF
client = boto3.client('cloudformation')
response = client.list_stack_resources(StackName='ELBdevlabs3')

#Get the Cognito UserPool Id resources from CF
cognito=response['StackResourceSummaries'][7] 
userpool=cognito['PhysicalResourceId'] 


# Delete domain in Cognito

client = boto3.client('cognito-idp')

domain = client.describe_user_pool(UserPoolId=userpool) 
domain = domain['UserPool']['Domain']

deletedomain = client.delete_user_pool_domain(Domain=domain,UserPoolId=userpool)

# List user for delete

listuser = client.list_users(UserPoolId=userpool)    

listuser['Users'][0]['Username']
## this return the username, we need to iterate on this to get all the user before deleting them all

##initialize variable to gather all the username
alluser=[]

#iterate through the list to get all the username
for x in listuser['Users']: 
     alluser.append(x['Username']) 

#Delete all the users 
for t in alluser: 
     deletepool = client.admin_delete_user(UserPoolId=userpool,Username=t) 
     
