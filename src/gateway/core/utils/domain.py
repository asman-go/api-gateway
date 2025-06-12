from urllib.parse import urlparse


def normalize_domain(asset: str) -> str | None:
    _parsed = urlparse(asset).netloc

    if not _parsed:
        return None

    if '@' in _parsed:
        # Убираем логин/пароль
        _parsed = _parsed.split('@')[1]

    if ':' in _parsed:
        # Убираем порт
        _parsed = _parsed.split(':')[0]

    if _parsed.startswith('*.'):
        # Убираем вайлдкард
        _parsed = _parsed[2:]

    if _parsed.startswith('.'):
        # Убираем вайлдкард
        _parsed = _parsed[1:]

    return _parsed
