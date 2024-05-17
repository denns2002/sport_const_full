from django.conf import settings


def translate_ru(eng="", ru=""):
    """
    Returns the English or Russian translation, depending on the LANGUAGE_CODE setting.

    If only one of the variables is specified, then returns it.
    If the eng and ru parameters are not specified, returns the boolean value of the settings LANGUAGE_CODE == "RU".

    :param eng: English word(s)
    :type eng: str or list or tuple
    :param ru: Russian translation
    :type ru: str or list or tuple
    :return: translation or bool LANGUAGE_CODE setting.
    :rtype: bool or str or list or tuple
    :raises ValueError: if length eng, ru does not match
    :raises TypeError: if eng, ru is not of str, list, tuple types
    """

    types = (str, list, tuple)

    if not (isinstance(eng, types) and isinstance(ru, types)):
        raise TypeError("Unsupported type!")

    if eng or ru:
        return ru if not eng or settings.LANGUAGE_CODE == "RU" and ru else eng

    else:
        return settings.LANGUAGE_CODE == "RU"
