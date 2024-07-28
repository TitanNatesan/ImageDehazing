from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
import cv2
import numpy as np
from Dehaze import dhazei  # Adjust the import based on your module's structure

def upload_image(request):
    image_url = None
    dehazed_image_url = None

    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        image_url = fs.url(filename)
        
        # Read the uploaded image
        img_path = fs.path(filename)
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        
        # Apply dehazing
        dehazed_img = dhazei(img, 0)
        
        # Save the dehazed image
        dehazed_filename = 'dehazed_' + filename
        _, buffer = cv2.imencode('.jpg', dehazed_img)
        dehazed_img_file = ContentFile(buffer.tobytes())
        fs.save(dehazed_filename, dehazed_img_file)
        dehazed_image_url = fs.url(dehazed_filename)

    return render(request, 'image_upload.html', {'image_url': image_url, 'dehazed_image_url': dehazed_image_url})
