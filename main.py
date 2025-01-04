import json
import pandas as pd
from datetime import date
from comm_tools import data_tools
from comm_tools.data_tools import upload_data, upload_data_plus
from comm_tools.model import WebData, WeiboData, KeywordAssociation


def print_json(data, indent=0):
    if isinstance(data, dict):
        for key, value in data.items():
            print(" " * indent + f"{key}:")
            print_json(value, indent + 4)
    elif isinstance(data, list):
        for i, item in enumerate(data):
            print(" " * indent + f"[{i}]")
            print_json(item, indent + 4)
    else:
        print(" " * indent + f"{data}")


def retrieve_web_data(url=""):
    # process web data
    # web_data_json = data_tools.retrieve_json(url)
    web_data_json = data_tools.retrieve_json_demo1('./web.json')
    web_data_df, key_words_list = data_tools.transform_web_data(web_data_json)
    upload_data_plus(web_data_df, key_words_list, WebData)


def retrieve_weibo_data(url=""):
    # process weibo data
    # weibo_data_json = data_tools.retrieve_json(url)
    weibo_data_json = data_tools.retrieve_json_demo1('./weibo.json')
    weibo_data_df, key_words_list = data_tools.transform_weibo_data(weibo_data_json)
    upload_data_plus(weibo_data_df, key_words_list, WeiboData)

def retrieve_wechat_data(url=""):
    # process weibo data
    # wechat_data_json = data_tools.retrieve_json(url)
    wechat_data_json = data_tools.retrieve_json_demo1('./wechat.json')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # retrieve_web_data()

    # retrieve_weibo_data()

    # retrieve_wechat_data()
    #with open('weibo.json', 'r') as file:
    #    json_data = json.load(file)
    #    print_json(json_data)




# See PyCharm help at https://www.jetbrains.com/help/pycharm/
