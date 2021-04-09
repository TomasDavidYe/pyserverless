#!/bin/bash


# Just zip the file and update function without updating the full CDK stack. Nice for quick changes to the source code
./deployment_utils/build_zip.sh;
aws lambda update-function-code --function-name lambda-function-1 --zip-file fileb://./output/build/your-project-name.zip;
aws lambda update-function-code --function-name lambda-function-2 --zip-file fileb://./output/build/your-project-name.zip;
