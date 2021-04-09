#!/bin/bash


# builds all artifacts and re-deploys the full CDK stack
./deployment_utils/build_zip.sh;
./deployment_utils/build_lambda_layers.sh;

cdk deploy --require-approval never;