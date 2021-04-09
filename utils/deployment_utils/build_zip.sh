rm ./output/build/your-project-name.zip;
zip -r ./output/build/your-project-name.zip ./*_lambda.py  ./your-project-source/* -x "*.parquet*" "build/*" ".git/*" ".idea/*" "*__pycache__*";