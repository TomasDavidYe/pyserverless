#!/bin/bash


# Clean Up of Old layer
rm -rf ./output/build/python;
rm ./output/build/data-science-lambda-layer.zip;

# Creating Directories
mkdir ./output/build/python;
mkdir ./output/build/python/lib;
mkdir ./output/build/python/lib/python3.8;
mkdir ./output/build/python/lib/python3.8/site-packages;

# Copying 3rd party libraries (like pandas, numpy etc...) from local environment to layer zip folder
cp -r ./path_to_python_interpreter/site-packages/sqlalchemy ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/pymysql ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/dateutil ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/pandas ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/pytz ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/six.py ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/numpy ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/numpy.libs ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/yfinance ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/requests ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/lxml ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/requests ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/multitasking ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/chardet ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/certifi ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/idna ./output/build/python/lib/python3.8/site-packages/;
cp -r ./path_to_python_interpreter/site-packages/dependency_injector ./output/build/python/lib/python3.8/site-packages/;


# Zipping up packages into layer
cd ./output/build/;
zip -r ./data-science-lambda-layer.zip ./python/*;
cd ../..;
