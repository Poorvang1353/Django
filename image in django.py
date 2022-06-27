#---------------------- Image & Files Handel in Dajngo ----------------------

# --------- Insert Image in Table  ---------
# Note:- You Need to install pillow module for handling image file (pip install pillow)
#      - You Need to write (request.FILES) for insert image or other files insert database
#      - You Need to write (enctype="multipart/form-data") in HTML Page in <form method="post" enctype="multipart/form-data"></form> tag
#      - You Need to write (<form method = 'POST' novalidate>) if you want to stop default HTML Form validation


# --------- Show Image in Html   ---------

# Add Code in Project (urls.py)
from django.contrib import admin
from django.urls import path,include

from django.conf import settings # --------> this
from django.conf.urls.static import static# --------> this



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # --------> this

# Add Code in Project (setting.py)
MEDIA_ROOT =  BASE_DIR / 'media' 
MEDIA_URL = '/media/'