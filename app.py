print('Starting import...')
import os
os.environ['NUMBA_CACHE_DIR'] = '/tmp/cache'
from processors import image_to_audio
import base64
import boto3
import json
from datetime import datetime

# Load S3
print('Loading S3...')
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3', region_name="us-east-1", config=boto3.session.Config(signature_version='s3v4'))


def save_to_s3(path, path_in_s3, s3bucket='image2audio', presigned_url=True, url_expire_time=3600):
    s3_resource.meta.client.upload_file(path, s3bucket, path_in_s3)
    if presigned_url:
        return s3_client.generate_presigned_url('get_object', Params={'Bucket': s3bucket, 'Key': path_in_s3}, ExpiresIn=url_expire_time)


def lambda_handler(event, context):
    print('Lambda is running!')
    print(event)
    audio_path = '/tmp/audio.wav'
    image_path = '/tmp/image.png'
    edge_detection_image_path = '/tmp/edge.png'
    input_params: dict = json.loads(event.get('body', '{}'))
    print('Accepted input params:')
    print(input_params)

    # Receive the base64 string and convert to image
    if 'image' in input_params:
        b64_image = input_params.get('image')
        with open(image_path, 'wb') as file:
            file.write(base64.b64decode(b64_image))
        print('Using input image')
    # If no image provided use the default image
    else:
        image_path = 'default.png'
        inverse_color = True
        print('Using Default Image')
    
    # Detect other input params
    inverse_color = bool(input_params.get('inverse', False))
    print(f'Inverse Color: {inverse_color}')
    edge_detection = bool(input_params.get('edge', False))
    print(f'Edge Detection: {edge_detection}')
    
    # Run the conversion function with the received params
    print('Converting audio...')
    image_to_audio(image_path, audio_path, inverse_color=inverse_color, edge_detection=edge_detection,
                   edge_detection_image_path=edge_detection_image_path)

    # Save the converted audio to S3 bucket and creating a temporary link to the file
    print('Saving data to S3...')
    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    audio_savepath = f'audio/{current_time}.wav'
    edge_detection_image_savepath = f'edge_detection/{current_time}.png'

    # Create the response data and return
    data = {
        'audio': save_to_s3(audio_path, audio_savepath),
        'edge_image': save_to_s3(edge_detection_image_path, edge_detection_image_savepath) if edge_detection is True else None
    }
    print('Response data:')
    print(data)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
        },
        'body': json.dumps(data)
    }
