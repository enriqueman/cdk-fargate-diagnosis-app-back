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


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
