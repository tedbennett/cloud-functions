# Creating a Python Lambda function behind an API

- Can either create a zip file or a container (easier but need to upload the container to AWS)

- Create a python file, and add a handler function that looks like:

```
import boto3
import json

def lambda_handler(event, context):
    body = json.loads(event["body"])
    # Do something with the body

    return {"statusCode": 200, "body": json.dumps({"message": "success"})}
```

## Zip file

- In this case, the Python file must be named `lambda_function.py` and the function must be named `lambda_handler(event, context)`
- You need to install packages locally, and bundle them into a zip
- Install via: `python3 -m pip install --target ./package {package}`
- Bundle them into a zip with `zip -r ./{bundle}.zip ./package`
- Then add the python function with `zip -g {bundle}.zip lambda_function.py`

## Container

- Create a dockerfile like:

```
FROM public.ecr.aws/lambda/python:3.8

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
```

- With this file, the Python file should be called `app.py` and the handler `handler()`
- Build the image with `docker build -t {image name} .`
- Follow the steps in AWS ECR for tagging and pushing the image
