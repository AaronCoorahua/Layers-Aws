import json
import requests
import pytz
from dateutil import parser
import uuid
from passlib.hash import pbkdf2_sha256
import io
import boto3
import jwt
from jsonschema import validate, ValidationError
import validators

s3_client = boto3.client('s3')

# Esquema JSON para validar
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
    },
    "required": ["name", "age"]
}

def lambda_handler(event, context):
    # Validar esquema JSON
    data = {"name": "John", "age": 30}
    try:
        validate(instance=data, schema=schema)
        schema_validation = "Valid JSON"
    except ValidationError as e:
        schema_validation = f"Invalid JSON: {e.message}"
    print("json ok")
    # Hacer una solicitud HTTP
    response = requests.get('https://api.github.com')
    print("request ok")
    # Manejar fechas y zonas horarias
    date_str = "2023-06-14T12:00:00Z"
    date = parser.parse(date_str)
    local_tz = pytz.timezone("America/New_York")
    local_date = date.astimezone(local_tz)
    print("fechas ok")
    # Generar un UUID
    unique_id = str(uuid.uuid4())
    print("UUID ok")
    # Manejar contraseñas
    password = "mysecretpassword"
    hashed_password = pbkdf2_sha256.hash(password)
    print("password ok")

    
    # Manejar tokens JWT
    token = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
    
    # Validar una URL
    url = "https://www.example.com"
    is_valid_url = validators.url(url)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'schema_validation': schema_validation,
            'github_api_status': response.status_code,
            'local_date': local_date.isoformat(),
            'unique_id': unique_id,
            'hashed_password': hashed_password,
            'jwt_token': token,
            'is_valid_url': is_valid_url,
        })
    }
