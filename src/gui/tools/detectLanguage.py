import locale
import logging
import platform

def detect_language():
    """
    Reads the locale information and derives the language, e.g. de, en.
    If detection fails, always en will be returned, at the same time a warning is logged.
    :return: language information.
    """
    my_locale = locale.getdefaultlocale()
    logging.debug(f'Locale: {my_locale}')

    my_language = 'en'

    match platform.uname()[0]:
        case 'Linux':
            my_language = (my_locale[0].split('-'))[0]
        case 'Windows':
            my_language = (my_locale[0].split('_'))[0]
        case _:
            logging.warning('Unknown system, unable to determine language automatically.')
            pass

    logging.debug(f'Platform: {platform.uname()}')
    logging.info(f'Detected language |{my_language}|')

    return my_language
