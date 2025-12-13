{% extends "diary/base.html" %}

{% block content %}
<h2>Вхід у систему</h2>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}

    <button class="btn" type="submit">Увійти</button>
</form>

{% if form.errors %}
<p style="color:red;">Неправильний логін або пароль</p>
{% endif %}

{% endblock %}




