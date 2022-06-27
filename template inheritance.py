# Dajngo HTML Tamplate inheritance
# -------------------------------------------------------- 
# Step:
   # 1 - Create (base.html) ---> Put Repated Code in this files 
   # 2 - Make block like
      --> for page title
        {% block title %}

        {% endblock title %} 
      
      --> for body
        {% block body %}


        {% endblock body %}

# -------------------------------------------------------- 
    # 3 - Now Make Other html page
    # 4 - Add billow tag on top of other html page 
        {% extends "base.html" %}
        
    # 5 - Now Put Your Page title in (title block)
        {% block title %}
            Shop |
        {% endblock title %}

    # 6 - Now Put Your body code in (body block)
        {% block body %}
            <h1>Heading</h1>
            <p>This is the content.</p>
        {% endblock body %}