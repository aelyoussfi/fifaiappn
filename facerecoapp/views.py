from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PhotoForm
from .models import Photo
from PIL import Image
from io import BytesIO
import base64
from brain import test
import numpy as np
from django.contrib.auth.decorators import login_required
import os
from django.core.files.storage import default_storage as storage
from io import BytesIO
import boto3

def list_photo_names(directory):
    """
    Lists the names of photo files in the specified directory, without file extensions.

    :param directory: The directory to search in.
    :return: A list of photo names without extensions.
    """
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
    photo_names = []

    for file in os.listdir(directory):
        name, ext = os.path.splitext(file)
        if ext.lower() in image_extensions:
            photo_names.append(name)

    return photo_names

def find_image_extension(directory, filename):
    """
    Find the extension of an image file in the specified directory based on its filename.

    :param directory: The directory to search in.
    :param filename: The base name of the image file, without extension.
    :return: The extension of the image file if found, None otherwise.
    """
    for file in os.listdir(directory):
        name, ext = os.path.splitext(file)
        if name == filename and ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
            return ext
    return None

def about(request):
    return render(request,'facerecoapp/about.html')

@login_required
def index(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save()
            # Store the uploaded photo's information in the session
            request.session['uploaded_photo_id'] = photo.id
            return JsonResponse({'success': True, 'photo_url': photo.image.url})
    else:
        form = PhotoForm()
    return render(request, 'facerecoapp/index.html', {'form': form})

@login_required
def get_trated_photo(request):
    # Retrieve the uploaded photo's ID from the session
    uploaded_photo_id = request.session.get('uploaded_photo_id')

    if uploaded_photo_id is None:
        return JsonResponse({'message': 'Try again', 'success': False})
    else:
        try:
            # Retrieve the photo object using the ID
            photo = Photo.objects.get(pk=uploaded_photo_id)
            if storage.exists(photo.image.name):
                with storage.open(photo.image.name, 'rb') as image_file:
                    with Image.open(image_file) as im:
                        #im = Image.open(photo.image.path)
                        im = im.convert("RGB")
                        # im = im.convert("RGB")
                        treated_photo_name = test.similar(im)
                        print(treated_photo_name[0] )
                        if  treated_photo_name == "⚠️ Please take a selfie with clear sight for your face.":
                            return JsonResponse({'message': treated_photo_name, 'success': False})
                        else:
                            if str(treated_photo_name[0]).split('.')[0] in list_photo_names("./coolPlayers/"):
                                ext = find_image_extension("./coolPlayers/", str(treated_photo_name[0]).split('.')[0])
                                treated_photo = "./coolPlayers/"+ str(treated_photo_name[0]).split('.')[0]+ext
                            treated_photo = Image.open(treated_photo)
                            diction = treated_photo_name[2]
                            #extract name
                            name = str(treated_photo_name[0]).split('.')[0] 
                            score = treated_photo_name[1]
                            print(score)
                            # Convert the treated photo to Base64
                            # Convert the image to RGB mode
                            if treated_photo.mode != "RGB":
                                treated_photo = treated_photo.convert("RGB")
                            buffered = BytesIO()
                            treated_photo.save(buffered, format='JPEG')
                            treated_photo_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

                            # Create a JSON response with the Base64 encoded image
                            response_data = {
                                'success': True,
                                'photo_url': photo.image.url,
                                'treated_photo_base64': treated_photo_base64,
                                'treated_photo_name':name,
                                'score' : score,
                                'dict': diction
                            }
                            
                            return JsonResponse(response_data)
        except Photo.DoesNotExist:
            return JsonResponse({'message': 'Uploaded photo not found.', 'success': False})
        

def home(request):
    return render(request,"facerecoapp/home.html")