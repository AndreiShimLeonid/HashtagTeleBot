import datetime

def check_message(text: str, hastags: list, content_type: str, username:str):
    for hashtag in hastags:
        if hashtag in text.split():
            if content_type == "text":
                # TODO сделать функцию для логирования
                print(datetime.datetime.now(),
                      f'-- Failed to update database - no picture with hashtag from @{username}')
                return [0, "Не верю. Где ваши доказательства?", hashtag]
            else:
                print(datetime.datetime.now(), f'-- DB is updated - visual content with hashtag from @{username}')
                return [1, "👍", hashtag]
