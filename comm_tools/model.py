from calendar import month

from sqlalchemy import (Column, Integer, String, Date, Float,
                        ForeignKey, UniqueConstraint, CheckConstraint)
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()


# 定义网络版内容
class WebData(Base):
    __tablename__ = 'WebData'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Author_Name = Column(String(100), nullable=False)
    Author_Id = Column(String(100), nullable=True)
    Content = Column(String(8000), nullable=True)
    Domain = Column(String(100), nullable=True)
    Rank = Column(String(100), nullable=True)
    Title = Column(String(200), nullable=False)
    ReadCount = Column(Integer, nullable=True)
    Url = Column(String(200), nullable=True)
    Date = Column(Date, nullable=False)

    __table_args__ = (UniqueConstraint('Author_Name',
                                       'Title',
                                       'Date',
                                       name='WebData_UNIQUE'),)

    # 添加反向关联
    web_assoc = relationship("KeywordAssociation",
                                  foreign_keys="[KeywordAssociation.web_id]",
                                  back_populates="web")

    def __init__(self, row):
        # 直接从row字典中提取值
        self.Author_Name = row.get('Author_Name')
        self.Author_Id = row.get('Author_Id')
        self.Content = row.get('Content')
        self.Domain = row.get('Domain')
        self.Rank = row.get('Rank')
        self.Title = row.get('Title')
        self.ReadCount = row.get('ReadCount')
        self.Url = row.get('Url')
        # 假设Date应该是在创建对象时获取的当前日期
        self.Date = date.today()


class WeiboData(Base):
    __tablename__ = 'WeiboData'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Author_Name = Column(String(100), nullable=False)
    Author_Id = Column(String(50), nullable=True)
    Author_Type = Column(String(50), nullable=True)
    CommentCount = Column(Integer, nullable=True)
    Domain = Column(String(100), nullable=True)
    ForwardCount = Column(Integer, nullable=True)
    Rank = Column(Float, nullable=True)
    Text = Column(String(500), nullable=False)
    Url = Column(String(200), nullable=True)
    Date = Column(Date, nullable=False)

    __table_args__ = (UniqueConstraint('Author_Name',
                                       'Text',
                                       'Date',
                                       name='WeiboData_UNIQUE'),)
    # 关联关系
    weibo_assoc = relationship("KeywordAssociation",
                                        foreign_keys="[KeywordAssociation.weibo_id]",
                                        back_populates="weibo")

    def __init__(self, row):
        # 直接从row字典中提取值
        self.Author_Name = row.get('Author_Name')
        self.Author_Id = row.get('Author_Id')
        self.Author_Type = row.get('Author_Type')
        self.CommentCount = row.get('CommentCount')
        self.Domain = row.get('Domain')
        self.ForwardCount = row.get('ForwardCount')
        self.Rank = row.get('Rank')
        self.Text = row.get('Text')
        self.Url = row.get('Url')
        # 假设Date应该是在创建对象时获取的当前日期
        self.Date = date(year=2025, month=1, day=2) #date.today()


class WechatData(Base):
    __tablename__ = 'WechatData'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    Author_Name = Column(String(100), nullable=False)

    # 关联关系
    wechat_assoc = relationship("KeywordAssociation",
                                        foreign_keys="[KeywordAssociation.wechat_id]",
                                        back_populates="wechat")

# 定义标签
class Keywords(Base):
    __tablename__ = 'Keywords'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    key_name = Column(String(50), nullable=False, unique=True)
    # 如果有其他列或关系，请在这里继续定义
    __table_args__ = (UniqueConstraint('key_name', name='Keywords_UNIQUE'),)

    # 添加反向关联
    key_assoc = relationship("KeywordAssociation",
                                foreign_keys="[KeywordAssociation.keyword_id]",
                                back_populates="keyword")


class KeywordAssociation(Base):
    __tablename__ = 'Keyword_association'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    keyword_id = Column(Integer, ForeignKey('Keywords.Id'), nullable=False)
    web_id = Column(Integer, ForeignKey('WebData.Id'), nullable=True)
    weibo_id = Column(Integer, ForeignKey('WeiboData.Id'), nullable=True)
    wechat_id = Column(Integer, ForeignKey('WechatData.Id'), nullable=True)


    # 添加约束条件
    chk_constraint = CheckConstraint(or_(web_id.isnot(None), weibo_id.isnot(None), wechat_id.isnot(None)), name='Keyword_association_chk_1')

    # 添加关联关系
    keyword = relationship("Keywords", foreign_keys=[keyword_id], back_populates="key_assoc")
    web = relationship("WebData", foreign_keys=[web_id], back_populates="web_assoc")
    weibo = relationship("WeiboData", foreign_keys=[weibo_id], back_populates="weibo_assoc")
    wechat = relationship("WechatData", foreign_keys=[wechat_id], back_populates="wechat_assoc")