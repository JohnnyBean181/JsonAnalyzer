import configparser


class Config:
    def __init__(self):
        # 创建 ConfigParser 对象
        config = configparser.ConfigParser()
        # 读取 ini 文件
        config.read('config.ini')
        # 提取数据库连接信息
        self.user = config['database']['user']
        self.password = config['database']['password']
        self.host = config['database']['host']
        self.port = config['database']['port']
        self.database = config['database']['database']
        self.table_web = config['database']['table_web']
        self.table_weibo = config['database']['table_weibo']
        self.table_wechat = config['database']['table_wechat']
