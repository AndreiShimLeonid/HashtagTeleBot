import datetime


def format_date(date_str):
    """
    Format date from YYYY-MM-DD to D month YYYY
    :param date_str: date format YYYY-MM-DD
    :return:string - formatted date
    """
    months = {
        1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
        5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
        9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
    }
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    day = date_obj.day
    month = months[date_obj.month]
    year = date_obj.year
    formatted_date = f"{day} {month} {year}"
    return formatted_date


def format_month(date_str):
    """
        Format date from YYYY-MM to Month YYYY
    :param date_str: date format YYYY-MM-DD
    :return: string - formatted date
    """
    months = {
        1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель',
        5: 'Май', 6: 'Июнь', 7: 'Июль', 8: 'Август',
        9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
    }
    date_obj = datetime.datetime.strptime(date_str, '%Y-%m')
    month = months[date_obj.month]
    year = date_obj.year
    formatted_date = f"{month} {year}"
    return formatted_date

