# utils/settings.py
from django.conf import settings as dj_settings

def get_user_settings(params, user=None):
    def _get_param(param):
        # Сначала пробуем взять из БД
        if user and user.is_authenticated:
            db_value = user.settings.filter(name=param).values_list('value', flat=True).first()
            if db_value not in (None, ''):
                return db_value
        # Потом берём из settings.py
        return getattr(dj_settings, param, None)

    if isinstance(params, str):
        return _get_param(params)
    elif isinstance(params, (list, tuple)):
        return {param: _get_param(param) for param in params}
    else:
        raise TypeError("params должен быть строкой или списком строк")
