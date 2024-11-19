import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_fargate_deploy.cdk_fargate_deploy_stack import CdkFargateDeployStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_fargate_deploy/cdk_fargate_deploy_stack.py
@pytest.fixture
def CdkFargateDeployStack():
    app = core.App()
    stack = CdkFargateDeployStack(app, "cdk-fargate-deploy")
    template = assertions.Template.from_stack(stack)
    return template


def test_vpc_creation(stack_template):
    """Test if VPC is created with correct properties"""
    stack_template.resource_count_is("AWS::EC2::VPC", 1)
    stack_template.has_resource("AWS::EC2::VPC", {
        "Properties": {
            "EnableDnsHostnames": True,
            "EnableDnsSupport": True,
            "MaxAzs": 2
        }
    })

def test_ecs_cluster_creation(stack_template):
    """Test if ECS Cluster is created"""
    stack_template.resource_count_is("AWS::ECS::Cluster", 1)

def test_fargate_service_creation(stack_template):
    """Test if Fargate Service is created with correct properties"""
    stack_template.resource_count_is("AWS::ECS::Service", 1)
    stack_template.has_resource("AWS::ECS::Service", {
        "Properties": {
            "DesiredCount": 1,
            "LaunchType": "FARGATE"
        }
    })

def test_task_definition_properties(stack_template):
    """Test Task Definition configuration"""
    stack_template.has_resource("AWS::ECS::TaskDefinition", {
        "Properties": {
            "Cpu": "256",
            "Memory": "512",
            "NetworkMode": "awsvpc",
            "RequiresCompatibilities": ["FARGATE"]
        }
    })

def test_alb_creation(stack_template):
    """Test if Application Load Balancer is created"""
    stack_template.resource_count_is("AWS::ElasticLoadBalancingV2::LoadBalancer", 1)

def test_target_group_health_check(stack_template):
    """Test Target Group health check configuration"""
    stack_template.has_resource("AWS::ElasticLoadBalancingV2::TargetGroup", {
        "Properties": {
            "HealthCheckPath": "/",
            "HealthCheckIntervalSeconds": 30,
            "HealthCheckTimeoutSeconds": 5,
            "HealthyThresholdCount": 5,
            "UnhealthyThresholdCount": 2,
            "Matcher": {
                "HttpCode": "200"
            }
        }
    })

def test_security_group_creation(stack_template):
    """Test if security groups are created"""
    # Should have security groups for ALB and Fargate service
    stack_template.resource_count_is("AWS::EC2::SecurityGroup", 2)

def test_container_definition(stack_template):
    """Test container definition properties"""
    stack_template.has_resource("AWS::ECS::TaskDefinition", {
        "Properties": {
            "ContainerDefinitions": assertions.Match.array_with([
                assertions.Match.object_like({
                    "PortMappings": assertions.Match.array_with([
                        assertions.Match.object_like({
                            "ContainerPort": 80,
                            "Protocol": "tcp"
                        })
                    ])
                })
            ])
        }
    })
