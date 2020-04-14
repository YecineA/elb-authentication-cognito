import boto3
import json

#Ask what is the CF stack

stack =  raw_input("Enter the stack name : ")

#Get the list of resources from CF
client = boto3.client('cloudformation')
response = client.list_stack_resources(StackName=stack)

print "Listing the Stack resources..."
#Get the Cognito UserPool Id resources from CF
cognito=response['StackResourceSummaries'][7] 
userpool=cognito['PhysicalResourceId'] 

print "Getting the Cognito UserPool Id resources from CF..."
print userpool
# Delete domain in Cognito

client = boto3.client('cognito-idp')

domain = client.describe_user_pool(UserPoolId=userpool) 
domain = domain['UserPool']['Domain']

deletedomain = client.delete_user_pool_domain(Domain=domain,UserPoolId=userpool)

print 'Domain ' domain ' Deleted'

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

print 'All users have been deleted'
#Delete the userpool



#If needed to delete the Cognito User pool
#cognitoID=cognito['PhysicalResourceId']  

#response = client.delete_user_pool(
#    UserPoolId=cognitoID
#)
