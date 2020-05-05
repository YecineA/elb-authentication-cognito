#  Build a Website Login page with AWS ELB and AWS Cognito 

This lab is provided as part of [AWS Builders Online Series](https://aws.amazon.com/events/builders-online-series/).

ℹ️ You will run this lab in your own AWS account. Please follow directions at the end of the lab to remove resources to minimize costs.
https://aws.amazon.com/events/builders-online-series/

## **Overview**
In this lab, you will be building a website with a simple Login button. The goal is to have a public website available to everyone, and another page only visible for authenticated users. To achieve this, we are using AWS Application Load Balancer (ALB)  which integrates with AWS Cognito. AWS ALB provides authentication through social Identity Providers (IdP) which here will be AWS Cognito. If a user tries to click on the logging button, ALB redirects him to Cognito which will handle the Login and will redirect him back to ALB to access the restricted content. 


## **Architecture**
<p align="center">
  <img width="600" height="350" src="https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/AWS_ALB_Cognito.png">
</p>


## **Website** 

After deploying the solution, you will have a website hosted behind your ALB. This website shows a login page. This login button will trigger a redirection which will match an ALB Listener rule. This rule will be used to authenticate the user, this authentication is made through Cognito.


<p align="center">
  <img width="600" height="350" src="https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-04-13+at+3.29.09+PM.png">
</p>


Please refer to this website for a slideshow demonstrating the Authentication workflow :
https://www.exampleloadbalancer.com/auth_detail.html


## **Requirements** 

1. Own a public domain name that will be used by your ALB

2. Generate a SSH Key-pair in the region where you will run the lab. (We will not actually need to ssh in the instance, but this is always a best practice to be able to ssh in your instance). 
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html

3. Generate an ACM Certificate that will be used to secure communication between the browser and ALB using HTTPS. The certificate must secure the domain name you own. (let's say , if you own the domain example.com, you should create a certificate that secure both example.com and *.example.com)
https://docs.aws.amazon.com/acm/latest/userguide/gs-acm-request-public.html


4. Write down the Full Qualified Domain Name (FQDN) you will use to point your domain name to your ALB. (In my scenario I am using elbdevlabs.yecine.myinstance.com). **Note this down as this will be used in the CloudFormation Template**

## **Walkthrough**

1. Run the Cloudformation template 
1. Configure Cognito User pool
2. Configure Authentication rule on ALB


## **Run the Cloudformation template**

1. The Cloudformation template will deploy :

- VPC with Public and Private Subnet
- ALB with an HTTPS Listener using your ACM certificate
- Cognito User pool that will be used for the authentication 
- EC2 Instance with a Web server running in the Private Subnet
  
**Please note that once the Stack is deployed, the content of the website is not yet restricted to authenticated user yet. We need to configure it first to make it restricted.** 

To deploy the stack, you can either copy/paste following link in the CloudFormation Console or use the second link that will open the CloudFormation console in sydney region directly 

https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Template/ELBAuthCognito.json

https://ap-southeast-2.console.aws.amazon.com/cloudformation/home?region=ap-southeast-2#/stacks/create/review?stackName=AWSALBAuthentication&templateURL=https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Template/ELBAuthCognito.json

![StackURL](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-04-23+at+3.35.30+PM.png)

The stack requires few inputs from you.  Some are self explanatory, but others are **crucial** for the lab to be working. I will clarify this below : 

![StackDetails](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-04-29+at+6.50.47+PM.png)



-  Stack Name : Any name you want to give to the stack

- ACMCertificate : This is the certificate that ALB will use to secure the communication with your browser. You would need to copy the ARN from the ACM console :

![ACMARN](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-04-23+at+3.39.06+PM.png)


- AuthName : This will be the name of the Cognito User pool we will use to create our users. You can give any name. 

-ELBAlias : This is the FQDN of your website you will use. You should have noted this down in the requirement. In my own lab I have used the DNS name elbdevlabs.yecine.myinstance.com and created a CNAME pointing to the ALB FQDN accordingly.  
**We need this value to be exact as we will configure the Web server accordingly.**


Once the template is deployed, take the ALB FQDN in the output tab, and create a DNS CNAME to point your own domain to your ALB. 
If you are using Route 53 for your Domain, you can follow the link below :

https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-elb-load-balancer.html


**At this point, you should have a Cloudformation template deployed and a CNAME created for your website pointing to your ALB. Before going further, you should check that your website is accessible. Browse to https://yourwebsite.com (replace yourwebsite.com by your CNAME). Please note the Login button will not force you to authenticate yet. This part will be covered below. 


### **Configure Cognito User pool**

Web developers want to use federated identities from social networks to allow their users to sign-in. ALB’s new authentication action provides authentication through social Identity Providers (IdP) like Google, Facebook, and Amazon through Amazon Cognito.
We will use Cognito to act as an identity provider (IdP) which will authenticate users through the user pools supported by Amazon Cognito. 

1. Open the Amazon Cognito Console in Asia Pacific(Sydney) Region at https://ap-southeast-2.console.aws.amazon.com/cognito/
2. Click on Manage User Pools and select the User Pool created by the CloudFormation Template "ELBDevlabs-user-pool". A user pool is a user directory in Amazon Cognito and we will refer to this when we will configure the Authentication on the Load Balancer.

![CognitoUserPool](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-02-24+at+3.12.11+PM.png)

3. Create user in the Users and groups navigation pane and fill out the user form (you can choose either phone or email). This where all the Users related information will be stored

![UserCreation](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-02-24+at+3.17.25+PM.png)

4. After you create a user pool, you can create an app to use the built-in webpages for signing up and signing in your users.

Configure the App client settings from the App integration navigation pane :


  a. Select "Cognito User Pool"
  
  b. Configure the callback URL(s) l: https://yourdomain.com/oauth2/idpresponse
  
This tells Cognito where to redirect the User once authenticated, Cognito needs to redirect the authenticated user back to the LoadBalancer. Your Application Load Balancer (ALB) was created as part of a template and a DNS Alias record was created using a custom domain name.

In my environment, I am using my own domain name yecine.myinstance.com. as such my callback URL will be :
https://elbdevlabs.yecine.myinstance.com/oauth2/idpresponse 
  
  c. Allowed  OAuth Flows: Authorization code grant
  
  d. Allowed OAuth Scopes : openid
  
  e. Save changes

![AppConf](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-02-24+at+3.34.41+PM.png)


5. Configure the Domain name for your Cogntio endpoint and check its availability with the "Check availability" button, then hit "Save changes". You can choose any Domain name as long as it is unique. In the example below I was using "elbdevlabs"

![Domain](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-02-24+at+3.39.18+PM.png)

At this stage, we have an IdP configured with a user. This IdP will be used by ALB to force your user to login and to allow ALB to validate and verify your user access as part of the authentication flow. Now we need to configure ALB to authenticate the clients browsing to the website.


### **Configure ALB Authentication rule**

1. Open the Amazon EC2 Console in Asia Pacific (Sydney) Region at https://ap-southeast-2.console.aws.amazon.com/ec2/
2. Select the Load Balancers menu from the navigation pane
3. Select the Load Balancer that was created as part of the CloudFormation template 
4. At the bottom, select the Listener Tab and select the "View/Edit rules" 

![ELBAuthRule](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-03-05+at+10.04.28+AM.png)


5. We will add a new Path based rule, which will be matched when the user click on the "Login" button. This button redirects the user to the /users/users.html page. We need to configure a rule to authenticate the users when this Path is used. 

  a. Click on the "+" button at the top to insert a rule 
  
  ![AddPathRule](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-04-13+at+3.46.44+PM.png)
  
  b. Under the Conidtion (IF), Click on the "+ Add condition" to select Path and use the "/users/*" path. 
  
  ![Path](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-04-13+at+5.57.29+PM.png)
  
  c. Under the Action (THEN), add an action : AUTHENTICATE and refer to the Cognito User pool ID (It should be visible from the drop down list). You can leave the other default parameters 
  
![Forward](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-04-14+at+12.22.09+PM.png)
  
  d. We need to add an action once the user is authenticated, the action will be FORWARD to forward to the Target group where our Instance is running the website (it should be visible from the drop down list) 
  

 ![UserpoolID](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-04-14+at+12.30.40+PM.png)



10. Validate the settings and click on the Update button

![Validate](https://customsolutions.s3-ap-southeast-2.amazonaws.com/Yecine-Devlab/Screen+Shot+2020-04-14+at+12.33.31+PM.png)


### **Try it***
Browse to your ALB Domain name configured for the website : https://yourdomain.com


### **Delete Stack** 

Once you have done the lab and would like to delete the resources, you can delete the stack. However, the Userpool and Auto-scaling group and Auto scaling launch configuration need to be deleted manually.   

https://aws.amazon.com/premiumsupport/knowledge-center/cloudformation-stack-delete-failed/



