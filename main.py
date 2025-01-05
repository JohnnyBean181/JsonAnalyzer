import json
from comm_tools import data_tools
from comm_tools.data_tools import upload_data_plus
from comm_tools.model import CombinedData

def retrieve_data(url=""):
    # process weibo data
    # data_json = data_tools.retrieve_json(url)
    data_json = data_tools.retrieve_json_demo1('./wechat-20250103.json')
    data_df, key_words_list = data_tools.transform_data(data_json)
    upload_data_plus(data_df, key_words_list, CombinedData)

if __name__ == '__main__':

    retrieve_data()

