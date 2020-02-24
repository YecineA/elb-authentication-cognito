# ** Build a website that requires user to authenticate with AWS ELB/Cognito **

## **Overview**
In this lab we, you will be building a website where users need to be authenticate before accessing the content using Amazon Application Load Balancer (ALB)  and integrating with Amazon Cognito. AWS ALB provides authentication through social Identity Providers (IdP) which will be Amazon  Cognito. When a user browse to your website, ALB redirects them to Cognito which will handle the Login and redirect them back to your ALB. 


## **Architecture**
![Architecture](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/aws-security-week-cloudscale-authentication-advanced-authorization-with-amazon-cognito-amazon-cloud-directory-18-638.jpg)

## **Walkthrough**
1. Configure Cognito User pool
2. Congigure Authentication rule on ALB

### **Configure Cognito User pool**

1. Open the Amazon Cognito Console in Asia Pacific(Sydney) Region at https://ap-southeast-2.console.aws.amazon.com/cognito/
2. Click on Manage User Pools and select the User Pool created by the CloudFormation Template "ELBDevlabs-user-pool" 

![CognitoUserPool](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-02-24+at+3.12.11+PM.png)

3. Create user in the Users and groups navigation pane and fill out the user form (you can choose either phone or email)

![UserCreation] (https://github.com/YecineA/elb-authentication-cognito/edit/master/README.md)

4. Configure the App client settings from the App integration navigation pane :
  a. Select "Cognito User Pool"
  b. Configure the callback URL(s) : https://elbdevlabs.yecine.myinstance.com/oauth2/idpresponse
  c. Allowed  OAuth Flows: Authorization code grant
  d. Allowed OAuth Scopes : openid
  e. Save changes
5. Configure the Domain name for your Cogntio endpoint and check its availability with the "Check availability" button, then hit "Save changes"

### **Configure ALB Authentication rule**

1. Open the Amazon EC2 Console in Asia Pacific (Sydney) Region at https://ap-southeast-2.console.aws.amazon.com/ec2/
2. Select the Load Balancers menu from the navigation pane
3. Select the Load Balancer that was created as part of the CloudFormation template 
4. At the bottom, select the Listener Tab and select the "View/Edit rules" 
5. Edit the default rule and delete the default action. Replace "Forward" by with "Authenticate"
6. Select Amazon Cognito and choose the Pool Id that we configured previously 
7. Select App Client we configured (there should only one App Client)
8. Leave by default the other parameters and click on the Validation Box
9. After the first Authenticate rule, add a new action "Forward to" and select the Target group that was created as part of CloudFormation 
10. Validate the settings and click on the Update button


### **Try it***
Browse to your ALB Domain name configured for the website : https://devlabs.yecine.myinstance.com
