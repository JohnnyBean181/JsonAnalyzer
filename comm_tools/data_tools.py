import requests
import json
import pandas as pd
from datetime import date
from comm_tools.config import Config
from comm_tools.database_mysql import (open_mysql, open_mysql_plus,
                                       load_to_MySQL_on_Cloud)
from comm_tools.logger import log_progress
from comm_tools.model import Keywords, KeywordsAssociation


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


def retrieve_json(url):
    # 发送GET请求
    response = requests.get(url)

    # 检查请求是否成功（HTTP状态码为200表示成功）
    if response.status_code == 200:
        # 将响应内容解析为JSON格式
        json_data = response.json()

        # 返回获取到的JSON数据
        return json_data
    else:
        print(f"请求失败，状态码：{response.status_code}")

def retrieve_json_demo1(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    return data

def transform_data(json_data):
    news_df = None
    keywords_list = list()

    for i, data in enumerate(json_data):
        news_dict = dict()
        news_dict['Id'] = data.get('Id', None)
        news_dict['Author_Name'] = data.get('Author').get('DisplayName', None)
        news_dict['Author_Id'] = data.get('Author').get('Id', None)
        news_dict['Author_Type'] = data.get('Author').get('Type', None)
        news_dict['Domain'] = data.get('Domain', None)
        news_dict['Rank'] = data.get('Rank', None)
        news_dict['Title'] = data.get('Title', None)
        news_dict['Text'] = data.get('Text', None)
        news_dict['Content'] = data.get('Content', None)
        news_dict['Url'] = data.get('Url', None)
        news_dict['Date'] = date.today()
        news_dict['LikeCount'] = data.get('LikeCount', None)
        news_dict['ForwardCount'] = data.get('ForwardCount', None)
        news_dict['CommentCount'] = data.get('CommentCount', None)
        news_dict['ReadCount'] = data.get('ReadCount', None)
        keywords_list.append(data.get('TargetKeywords', []))
        if i == 0:
            news_df = pd.DataFrame(news_dict, index=[0])
        else:
            tmp_df = pd.DataFrame(news_dict, index=[0])
            news_df = pd.concat([news_df, tmp_df], ignore_index=True)
    return news_df, keywords_list

def upload_data(data_df, table_name):
    c = Config()

    with open_mysql(c) as engine:
        # 将 DataFrame 写入 MySQL
        load_to_MySQL_on_Cloud(data_df, engine, table_name)

def upload_data_plus(data_df, key_words_list, classname):
    """
    upload opinions, keywords into database, along with their correlations.
    :param data_df: opinions saved in dataframe.
    :param key_words_list: key_word list
    :param classname: either one of WebData, WeiboData, WechatData
    :return: None
    """
    c = Config()

    with open_mysql_plus(c) as session:
        # 将 DataFrame 写入 MySQL
        for index, row in data_df.iterrows():
            # print(f"Index: {index}, Data: {row}")
            data = classname(row)
            session.add(data)
            try:
                # verify whether the opinion is already in database.
                session.commit()
            except Exception as e:
                # if exists, load this opinion.
                if "Duplicate" in str(e):
                    log_progress(f"load opinion {row['Id']} due to duplicate entry")
                    session.rollback()
                    data = session.query(classname).filter_by(
                        Id=row['Id']).first()
                    if data is None:
                        print(f"get opinion error: {row['Id']}")
                else:
                    log_progress(str(e))

            # if there is no keywords, go to next opinion
            if len(key_words_list[index]) == 0:
                continue

            for key_word in key_words_list[index]:
                keyword = Keywords(key_name=key_word)
                session.add(keyword)
                try:
                    # verify whether the keyword is already in database.
                    session.commit()
                except Exception as e:
                    # if exists, pick up this keyword from the database.
                    if "Duplicate" in str(e):
                        log_progress(f"load keyword {key_word} due to duplication")
                        session.rollback()
                        keyword = session.query(Keywords).filter_by(key_name=key_word).first()
                    else:
                        log_progress(str(e))

                # 现在可以创建关联
                association = KeywordsAssociation(
                    keyword=keyword,  # 使用已经存在于session中或数据库中的Keyword实例
                    data=data # 使用已经存在于session中的WebData实例
                )

                session.add(association)
                try:
                    session.commit()
                except Exception as e:
                    if "Duplicate" in str(e):
                        log_progress("Skip association due to duplicate entry")
                        session.rollback()
                    else:
                        log_progress(str(e))





