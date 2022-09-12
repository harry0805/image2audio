# Use https://hub.docker.com/r/lambci/lambda as the base container
FROM public.ecr.aws/lambda/python:3.8 AS stage1
# set the working directory to /build
WORKDIR /
RUN echo "installing packages!!!!!"
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN yum -y install libsndfile

CMD ["/bin/bash"]
