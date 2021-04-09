from aws_cdk import core, aws_iam, aws_lambda, aws_apigatewayv2, aws_events, aws_events_targets
from aws_cdk.aws_apigatewayv2 import HttpMethod
from aws_cdk.aws_apigatewayv2_integrations import LambdaProxyIntegration
from aws_cdk.aws_events import Schedule


class ExampleLambdaStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, stage: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.stage = stage
        self.app_prefix = 'your-app-prefix'

        self.layer = self.lambda_layer()

        self.stock_update_lambda = self.lambda_function(
            function_name='update-stock-prices',
            handler='update_stock_prices.handler',
            duration_in_seconds=60,
            memory_size=1024
        )

        self.get_stock_prices = self.lambda_function(
            function_name='get-stock-prices',
            handler='get_stock_prices.handler',
            duration_in_seconds=60,
            memory_size=1024
        )

        self.schedule_stock_update_rule = self.cron_rule(
            rule_name='daily-stock-update',
            rule_description='To trigger update-stock-prices lambda 4 times during the day.',
            cron_expression='cron(0 5,11,17,23 * * ? *)',
            targets=[aws_events_targets.LambdaFunction(handler=self.stock_update_lambda)]
        )

        self.api = self.http_api()

    def cron_rule(self, rule_name, rule_description, cron_expression, targets):
        full_rule_name = self.generate_id_for_name(
            name=rule_name,
            service='cron-rule'
        )
        return aws_events.Rule(scope=self,
                               id=full_rule_name,
                               rule_name=full_rule_name,
                               description=rule_description,
                               schedule=Schedule.expression(cron_expression),
                               targets=targets)

    def lambda_layer(self):
        return aws_lambda.LayerVersion(
            scope=self,
            id=self.generate_id_for_name(name='data-science', service='lambda-layer'),
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_8],
            code=aws_lambda.Code.from_asset('./output/build/data-science-lambda-layer.zip'))

    def http_api(self):
        api_name = self.generate_id_for_name(
            name='trading-engine',
            service='api'
        )

        http_api = aws_apigatewayv2.HttpApi(scope=self,
                                            id=api_name,
                                            api_name=api_name,
                                            description="Entry point for your app",
                                            cors_preflight=aws_apigatewayv2.CorsPreflightOptions(allow_origins=['*']))

        get_stock_prices_integration = LambdaProxyIntegration(handler=self.get_stock_prices)
        http_api.add_routes(path='/get-stock-prices',
                            methods=[HttpMethod.GET],
                            integration=get_stock_prices_integration)


        return http_api

    def lambda_function(self, function_name, handler, duration_in_seconds=120, memory_size=128) -> aws_lambda.Function:
        full_function_name = self.generate_id_for_name(name=function_name, service='lambda')
        function = aws_lambda.Function(scope=self,
                                       id=full_function_name,
                                       function_name=full_function_name,
                                       runtime=aws_lambda.Runtime.PYTHON_3_8,
                                       handler=handler,
                                       layers=[self.layer],
                                       memory_size=memory_size,
                                       timeout=core.Duration.seconds(duration_in_seconds),
                                       code=aws_lambda.Code.from_asset('./output/build/your-project-name.zip'))

        # S3 Full Access for lambdas
        function.add_to_role_policy(statement=aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=["s3:*"],
            resources=["*"]
        ))

        # AWS SES Full Access for lambdas
        function.add_to_role_policy(statement=aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=["ses:*"],
            resources=["*"]
        ))

        core.CfnOutput(scope=self,
                       id=full_function_name + '-name',
                       value=function.function_name)

        return function

    def generate_id_for_name(self, name, service):
        return f'{self.app_prefix}-{name}-{service}-{self.stage}'
