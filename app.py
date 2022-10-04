print('start import')
import os
os.environ['NUMBA_CACHE_DIR'] = '/tmp/cache'
from processors import AudioProcessor, ImageProcessor
import base64
import boto3
import json


def image_to_audio(image_path, save_path=None, rotate=0, padding=3, inverse_color=False, volume=1, edge_detection=False, display_image=False, plot_spectrogram=False):
    # Image processing
    ip = ImageProcessor()
    ip.load_image(image_path, mode='RGB')
    ip.resize(600)
    if inverse_color:
        ip.inverse_color()
    if edge_detection:
        ip.edge_detection()
    if rotate:
        ip.rotate(rotate)
    ip.add_top_padding(padding)
    ip.convert_type('L')
    if display_image:
        ip.display_image()
    ip.flip()

    # Transform to Audio
    ap = AudioProcessor(44100)
    ap.load_image_form_array(ip.image_array)
    ap.image_to_spectrogram(inverse_transform=False)
    if plot_spectrogram:
        ap.plot_spectrogram()
    ap.spectrogram_to_wave()
    ap.normalize_audio()
    ap.change_volume(volume)
    ap.play_sound(save_path)


def lambda_handler(event, context):
    print('lambda is running!')
    print(event)
    image_path = '/tmp/image.png'
    audio_path = '/tmp/audio.wav'
    input_params: dict = json.loads(event.get('body', '{}'))
    print('Accepted input params:')
    print(input_params)

    # Receive the base64 string and convert to image
    if 'image' in input_params:
        b64_image = input_params.get('image')
        with open(image_path, 'wb') as file:
            file.write(base64.b64decode(b64_image))
        print('Using Input Image')
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
    image_to_audio(image_path, audio_path, inverse_color=inverse_color, edge_detection=edge_detection)

    # Save the converted audio to S3 bucket and creating a temporary link to the file
    s3bucket = 'image2audio'
    filepath = 'audio/1.wav'
    s3_resource = boto3.resource('s3')
    s3_client = boto3.client('s3', region_name="us-east-1", config=boto3.session.Config(signature_version='s3v4'))
    try:
        s3_resource.meta.client.upload_file(audio_path, s3bucket, filepath)
        download_url = s3_client.generate_presigned_url('get_object', Params={'Bucket': s3bucket, 'Key': filepath}, ExpiresIn=3600)
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(download_url)}
    except Exception as e:
        print(e)
        return {
            'statusCode': 500, 
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(e)}
