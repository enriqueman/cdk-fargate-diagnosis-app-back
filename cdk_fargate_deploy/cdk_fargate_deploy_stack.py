from aws_cdk import (
    # Duration,
    Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct
from aws_cdk import (aws_ec2 as ec2, aws_ecs as ecs,
                     aws_ecs_patterns as ecs_patterns)

class CdkFargateDeployStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkFargateDeployQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
        
        vpc = ec2.Vpc(self, "VpcFargate", max_azs=2)
        
        
        cluster = ecs.Cluster(self, "ClusterFargate", vpc=vpc) 
        
        
        service = ecs_patterns.ApplicationLoadBalancedFargateService(self, "MyFargateService",
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
