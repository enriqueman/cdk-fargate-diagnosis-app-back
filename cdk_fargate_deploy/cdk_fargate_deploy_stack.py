from aws_cdk import (
    # Duration,
    Duration,
    Stack,
    CfnOutput,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk import (aws_ec2 as ec2, aws_ecs as ecs,
                     aws_ecs_patterns as ecs_patterns,
                     aws_apigateway as apigateway,
                    #  aws_apigatewayv2_integrations as apigwv2,
                     aws_apigatewayv2 as apigwv2,
                     aws_apigatewayv2_integrations as apigwv2_integrations,
                     )

class CdkFargateDeployStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        vpc = ec2.Vpc(self, "VpcFargate", max_azs=2)
        
        
        cluster = ecs.Cluster(self, "ClusterFargate", vpc=vpc) 
        
        
        service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "FargateService",
            cluster=cluster,            
            cpu=256,                   
            desired_count=1,            
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_asset("."),
                container_port = 80),
            
            memory_limit_mib=512,      
            public_load_balancer=True)  
        
          # Configure Health Check
        service.target_group.configure_health_check(
            port="traffic-port",
            path="/",
            interval=Duration.seconds(30), 
            timeout=Duration.seconds(5),
            healthy_threshold_count=5,
            unhealthy_threshold_count=2,
            healthy_http_codes="200"
        )
        
        
        # VPC Link
        vpc_link  = apigwv2.CfnVpcLink (self, "HttpVpcLink",
            name="V2 VPC Link",
            subnet_ids=[subnet.subnet_id for subnet in vpc.private_subnets]                       
        )
        
               
        api = apigwv2.HttpApi(self, "HttpApi",
            api_name="ApigwFargate",
            description="Integration between apigw and Application Load-Balanced Fargate Service"
        )
        
        # API Integration
        integration = apigwv2.CfnIntegration(self, "HttpApiGatewayIntegration",
            api_id=api.http_api_id,
            connection_id=vpc_link.ref,
            connection_type="VPC_LINK",
            description="API Integration with AWS Fargate Service",
            integration_method="ANY",
            integration_type="HTTP_PROXY",
            integration_uri= service.load_balancer.listeners[0].listener_arn,
            payload_format_version="1.0"
        )
        
         #service.load_balancer.load_balancer_dns_name,
        # API Route
        apigwv2.CfnRoute(self, "Route",
            api_id=api.http_api_id,
            route_key="ANY/{proxy+}",
            target=f"integrations/{integration.ref}"
        )
        
    
        # Output API Gateway URL
        CfnOutput(self, "APIGatewayUrl",
            description="API Gateway URL to access the GET endpoint",
            value=api.url
        )