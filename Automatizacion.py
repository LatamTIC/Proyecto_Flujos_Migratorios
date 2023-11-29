import os
import boto3
from datetime import datetime

# Configura las credenciales de AWS
aws_access_key_id = 'secret'
aws_secret_access_key = 'secret'

# Crea un cliente de S3
s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

# Lista de buckets
bucket = "bucket-flujos-migratorios"

def obtener_fecha_modificacion_local(archivo):
    return os.path.getmtime(archivo)

def obtener_fecha_modificacion_s3(bucket, key):
    try:
        response = s3.head_object(Bucket=bucket, Key=key)
        return response['LastModified'].timestamp()
    except Exception as e:
        print(f"Error al obtener la fecha de modificación en S3: {e}")
        return None

def subir_a_s3(archivo_local):
    try:
        with open(archivo_local, 'rb') as file:
            s3.upload_fileobj(file, bucket, archivo_local)
            print(f"Archivo subido a S3: {archivo_local}")
    except Exception as e:
        print(f"Error al subir a S3: {e}")

def obtener_archivos_finales_en_bucket(bucket):
    try:
        response = s3.list_objects_v2(Bucket=bucket)

        archivos_finales = [objeto['Key'] for objeto in response.get('Contents', []) if not objeto['Key'].endswith('/')]

        return archivos_finales
    except Exception as e:
        print(f"Error al obtener archivos en S3: {e}")
        return None

archivos_finales = obtener_archivos_finales_en_bucket(bucket)

if archivos_finales:
    for archivo_local in archivos_finales:
        print(archivo_local)
        try:            
            fecha_modificacion_local = obtener_fecha_modificacion_local(f"{os.getcwd()}/{archivo_local}")
            fecha_modificacion_s3 = obtener_fecha_modificacion_s3(bucket, archivo_local)
            if fecha_modificacion_local is not None and fecha_modificacion_s3 is not None:
                if fecha_modificacion_local > fecha_modificacion_s3:
                    subir_a_s3(archivo_local)
                else:
                    print("El archivo local no ha sido modificado desde la última carga a S3.")
            else:
                print("No se pudieron obtener las fechas de modificación.")
        except:
            continue
else:
    print("No se encontraron archivos finales en el bucket.")
