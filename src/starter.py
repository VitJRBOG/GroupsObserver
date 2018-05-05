# coding: utf-8


import os
import logger
import datamanager
import vk_api
import core


def start():
    sender = "Start"

    try:

        if os.path.exists("path.txt") is False:
            file_text = open("path.txt", "w")
            file_text.write("")
            file_text.close()

            mess_for_log = "Was created file \"path.txt\"."
            logger.message_output(sender, mess_for_log)

        PATH = datamanager.read_path(sender)

        if os.path.exists(PATH + "data.json") is False:

            mess_for_log = "\nWARNING! File \"data.json\" not found!"
            logger.message_output(sender, mess_for_log)

            data_json = {
                "subjects": [
                    {
                        "name": "",
                        "topics": [],
                        "topic_notificator_settings": {
                            "post_count": 0,
                            "send_to": 0,
                            "check_topics": 0
                        },
                        "photo_notificator_settings": {
                            "photo_count": 0,
                            "check_photo": 0,
                            "send_to": 0,
                            "last_date": "0"
                        },
                        "send_to": 0,
                        "filter": "",
                        "last_date": "0",
                        "posts_count": 0,
                        "owner_id": 0
                    }
                ],
                "wiki_database_id": "-0_0",
                "total_last_date": "0"
            }

            user_answer = raw_input("USER [" + sender + " -> Wiki database URL]: ")

            wiki_full_id = str(user_answer[user_answer.rfind('page-') + 4:])

            data_json["wiki_database_id"] = wiki_full_id

            datamanager.write_json("Start", PATH, "data", data_json)

        #  Получение данных из файла JSON

        data_json = datamanager.read_json("Start", PATH, "data")

        # vk_admin_token = data_json["admin_token"]
        # vk_bot_token = data_json["bot_token"]

        user_answer = raw_input("USER [" + sender + " -> New token]: ")

        vk_admin_token = user_answer
        vk_bot_token = user_answer

        data_access_admin = {
            "token": vk_admin_token
        }
        data_access_bot = {
            "token": vk_bot_token
        }

        vk_admin_session = autorization(sender, data_access_admin, "token")
        vk_bot_session = autorization(sender, data_access_bot, "token")

        mess_for_log = "Program was started."
        logger.message_output(sender, mess_for_log)

        core.main(vk_admin_session, vk_bot_session)

    except Exception as var_except:
        logger.exception_handler(sender, var_except)
        return start()


def autorization(sender, data_access, auth_type):
    sender += " -> Authorization"

    try:

        if auth_type == "token":

            #  Авторизация по токену
            access_token = data_access["token"]
            vk_session = vk_api.VkApi(token=access_token)
            vk_session._auth_token()

        if auth_type == "login":

            #  Авторизация по имени пользователя и паролю
            vk_login = data_access["login"]
            vk_passwd = data_access["password"]
            vk_session = vk_api.VkApi(login=vk_login, password=vk_passwd)
            vk_session.auth()

        if auth_type != "token" and auth_type != "login":

            mess_for_log = "Error of authorization. Exit from program..."
            logger.message_output(sender, mess_for_log)

            exit(0)

        return vk_session

    except Exception as var_except:
        logger.exception_handler(sender, var_except)
        return autorization(data_access, auth_type)


start()
