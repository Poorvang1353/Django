# -------- handel Static Files In dajngo --------

# Steps:
    # 1 - Create (static) folder in Root Directory of Project
    # 2 - Paste Your Static Files Folder in (static) Folder (js,css,images...etc)
    # 3 - Now Do Setting in (setting.py)
           STATIC_URL = '/static/'

           STATICFILES_DIRS = [
                BASE_DIR /'static'
            ]
    # 4 - add {% load static %} tag on top of html page
    # 5 - Now use ({% static 'assets/image.jpg' %}) tag in HTML File for calling static files
    # 6 - Done              