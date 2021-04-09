#!/usr/bin/env python3
from aws_cdk import core
from aws.cdk_constructs.ExampleLambdaStack import ExampleLambdaStack

app = core.App()
ExampleLambdaStack(app, "trading-engine-cdk", stage='alpha')

app.synth()
