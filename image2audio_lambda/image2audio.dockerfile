FROM public.ecr.aws/lambda/python:3.8

# Install the function's dependencies using file requirements.txt
# from your project folder.

RUN yum install libsndfile -y
COPY requirements.txt .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code and its required files
COPY edge_detection_model ${LAMBDA_TASK_ROOT}/edge_detection_model
COPY default.png ${LAMBDA_TASK_ROOT}
COPY processors.py ${LAMBDA_TASK_ROOT}
COPY app.py ${LAMBDA_TASK_ROOT}


# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.lambda_handler" ]