import json
import boto3
from PIL import Image, ImageFilter
import io

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # Configurar el bucket y los nombres de archivo
    source_bucket = 'imagen-aaron'
    target_bucket = 'imagen-resize-aaron'
    source_key = 'aws.png'  # Cambia esto al nombre de tu imagen de origen en S3
    target_key = 'aws-blur.png'  # Cambia esto al nombre de tu imagen con desenfoque en S3
    
    # Descargar la imagen desde S3
    response = s3_client.get_object(Bucket=source_bucket, Key=source_key)
    image_data = response['Body'].read()
    
    # Leer la imagen usando Pillow
    image = Image.open(io.BytesIO(image_data))
    
    # Convertir la imagen al modo 'RGB' si no lo está
    if image.mode not in ('RGB', 'L'):
        image = image.convert('RGB')
    
    # Aplicar desenfoque Gaussian usando Pillow
    blurred_image = image.filter(ImageFilter.GaussianBlur(5))  # Cambia el valor según sea necesario
    
    # Guardar la imagen desenfocada en un buffer en memoria
    buffer = io.BytesIO()
    blurred_image.save(buffer, format='PNG')
    buffer.seek(0)
    
    # Subir la imagen desenfocada a S3
    s3_client.put_object(Bucket=target_bucket, Key=target_key, Body=buffer, ContentType='image/png')
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Image blurred and uploaded successfully',
            'source_bucket': source_bucket,
            'target_bucket': target_bucket,
            'source_key': source_key,
            'target_key': target_key
        })
    }
