docker build -t image2audio -f image2audio.dockerfile .
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 608506721320.dkr.ecr.us-east-1.amazonaws.com
docker tag image2audio:latest 608506721320.dkr.ecr.us-east-1.amazonaws.com/image2audio:latest
docker push 608506721320.dkr.ecr.us-east-1.amazonaws.com/image2audio:latest
# pause