import boto3
import os
from botocore.exceptions import ClientError

class CognitoAuthService:
    def __init__(self, region_name='us-east-1'):
        session = boto3.Session(region_name=region_name)
        self.cognito_client = session.client('cognito-idp',region_name=region_name, aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID_DOCKER'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY_DOCKER'))
        # self.client_id = "42rkk8nstluuocai1be6ob13s5"  # Add your Cognito App Client ID

    def sign_up(self, client_id: str,username: str, password: str, email: str, phone_number: str):
        try:
            return self.cognito_client.sign_up(
                # ClientId=self.client_id,
                ClientId=client_id,
                Username=username,
                Password=password,
                UserAttributes=[
                    {'Name': 'email', 'Value': email},
                    {'Name': 'phone_number', 'Value': phone_number}
                ],
                ValidationData=[
                    {'Name': 'otp_delivery', 'Value': 'sms'}
                ]
            )
        except ClientError as e:
            raise ValueError(str(e))

    def initiate_auth(self, client_id, username: str):
        try:
            return self.cognito_client.initiate_auth(
                AuthFlow='CUSTOM_AUTH',
                AuthParameters={'USERNAME': username},
                # ClientId=self.client_id
                ClientId=client_id
            )
        except ClientError as e:
            raise ValueError(str(e))

    def verify_login(self, client_id: str,code: str, username: str, session: str):
        try:
            response = self.cognito_client.respond_to_auth_challenge(
                # ClientId=self.client_id,
                ClientId=client_id,
                ChallengeName='CUSTOM_CHALLENGE',
                Session=session,
                ChallengeResponses={
                    'CODE': code,
                    'USERNAME': username,
                    'ANSWER': code
                }
            )
            return response.get('AuthenticationResult')
        except ClientError as e:
            raise ValueError(str(e))