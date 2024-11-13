from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from PIL import Image
import numpy as np
import pickle
import os
from django.conf import settings

model_path = os.path.join(settings.BASE_DIR, 'DjangoDeepfakeProject', 'new_resnetcnn_model.pkl')
with open(model_path, 'rb') as f:
    model = pickle.load(f)

def home(request):
    return render(request, 'index.html')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
        img = Image.open(image).convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        prediction = model.predict(img_array)
        is_real = prediction[0] > 0.5
        result = "Real" if is_real else "Deepfake"

        print(prediction[0])

        upload_dir = os.path.join(settings.BASE_DIR, 'media')
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        image_path = os.path.join(upload_dir, 'uploaded_image.jpeg')

        img.save(image_path)

        return JsonResponse({
            'message': f'The image is classified as {result}.',
            'image_url': '/media/uploaded_image.jpeg' ,
            'c_value': float(prediction[0]),
            'result': result
        })

    return JsonResponse({'message': 'Invalid request'}, status=400)

def show_result(request):
    image_url = request.GET.get('image_url')
    result = request.GET.get('result')
    c_value = request.GET.get('c_value')
    return render(request, 'result.html', {'image_url': image_url, 'result': result, 'c_value': c_value})











# Connecting with AWS
# import boto3
# from django.conf import settings
# from django.http import JsonResponse
# from PIL import Image
# import numpy as np
# import os
# from django.shortcuts import render
#
# # Initialize S3 client
# s3_client = boto3.client(
#     's3',
#     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
#     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
#     region_name=settings.AWS_S3_REGION_NAME
# )
#
# @csrf_exempt
# def upload_image(request):
#     if request.method == 'POST':
#         image = request.FILES['image']
#         img = Image.open(image).convert('RGB')
#         img = img.resize((224, 224))
#         img_array = np.array(img) / 255.0
#         img_array = np.expand_dims(img_array, axis=0)
#
#         prediction = model.predict(img_array)
#         is_real = prediction[0] > 0.5
#         result = "Real" if is_real else "Deepfake"
#
#         print(prediction[0])
#
#         # Save the image temporarily and upload to S3
#         image_name = 'uploaded_image.jpeg'
#         image_path = os.path.join('images', image_name)  # S3 object path
#
#         with open(image_name, 'wb') as f:
#             img.save(f, format='JPEG')
#
#         # Upload image to S3 with no public access (private)
#         with open(image_name, 'rb') as data:
#             s3_client.upload_fileobj(
#                 data,
#                 settings.AWS_STORAGE_BUCKET_NAME,
#                 image_path,
#                 ExtraArgs={'ACL': 'private'}  # Private access (default)
#             )
#
#         # Generate a pre-signed URL for temporary access
#         s3_url = s3_client.generate_presigned_url(
#             'get_object',
#             Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': image_path},
#             ExpiresIn=3600  # URL expires in 1 hour
#         )
#
#         return JsonResponse({
#             'message': f'The image is classified as {result}.',
#             'image_url': s3_url,
#             'result': result,
#             'c_value': float(prediction[0])
#         })
#
#     return JsonResponse({'message': 'Invalid request'}, status=400)
#
#
# def show_result(request):
#     image_url = request.GET.get('image_url')
#     c_value = request.GET.get('c_value')
#     print(c_value)
#     # c_value = round(float(c_value), 10)
#     result = request.GET.get('result')
#     return render(request, 'result.html', {'image_url': image_url, 'result': result, 'c_value': c_value})
