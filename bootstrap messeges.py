# Django display Bootstrap Messges in Web Page

# Steps:
   # 1 - Add Code in (setting.py)
   from django.contrib.messages import constants as messages

    MESSAGE_TAGS = {
        messages.DEBUG: 'alert-info',
        messages.INFO: 'alert-info',
        messages.SUCCESS: 'alert-success',
        messages.WARNING: 'alert-warning',
        messages.ERROR: 'alert-danger',
    }

    # 2 - Add Code in (html.py) for message display
        {% for message in messages %}
            <div class="alert {{ message.tags }} alert-dismissible" role="alert">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                <span aria-hidden="true">&times;</span>
                </button>
                {{ message }}
            </div>
        {% endfor %}




