# ElasticSearch Cleanup Curator Lambda
This lambda function is a basic template for cleaning up old indices using ES Curators.


## How to use
1. Add dependencies in the `package` directory, using pip.

Ubuntu:
```
pip3 install --target ./elasticsearch-curator --system
```

2. Zip up the packages

```
cd packages
zip -r9 ${OLDPWD}/function.zip .
```

3. Zip up the lambda function
```
cd ${OLDPWD}
zip -g function.zip lambda_function.py
```

4. Deploy
```
sudo aws lambda update-function-code --function-name LuaScannerService --zip-file fileb://function.zip
```