import datetime

import service


def check_message(text: str, hashtags: list, content_type: str, username: str, user_id: int):
    """
    Checks message for content
    :param text: message text
    :param hashtags: list of hashtags
    :param content_type: message content type (photo, video etc)
    :param username: username in format @username
    :return: [0, "Не верю. Где ваши доказательства?", hashtag] - if right hashtag without photo/video
            [1, "👍", hashtag] - if right hashtag with right photo
            [2, None, None] - if there is no hashtags from the list in messsage
    """
    for hashtag in hashtags:
        if hashtag in text.lower().split():
            if content_type == "text":
                # TODO сделать функцию для логирования
                service.log_write(f'-- Failed to update database - no picture with hashtag from @{username} ID {user_id}')
                return [0, "Не верю. Где ваши доказательства?", hashtag]
            else:
                return [1, "👍", hashtag]
    return [2, None, None]
