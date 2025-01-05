from calendar import month

from sqlalchemy import (Column, Integer, String, Date, Double, Text,
                        ForeignKey, UniqueConstraint, CheckConstraint)
from sqlalchemy import or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()


# 定义标签
class Keywords(Base):
    __tablename__ = 'Keywords'
    Id = Column(Integer, primary_key=True, autoincrement=True)
    key_name = Column(String(50), nullable=False, unique=True)
    # 如果有其他列或关系，请在这里继续定义
    __table_args__ = (UniqueConstraint('key_name', name='Keywords_UNIQUE'),)

    # 添加反向关联
    key_assoc = relationship("KeywordsAssociation",
                                foreign_keys="[KeywordsAssociation.keyword_id]",
                                back_populates="keyword")


class CombinedData(Base):
    __tablename__ = 'CombinedData'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    Id_txt = Column(String(100), nullable=False, unique=True)
    Author_Name = Column(String(100), nullable=False)
    Author_Id = Column(String(100), nullable=True)
    Author_Type = Column(String(50), nullable=True)
    Content = Column(Text, nullable=True)
    Domain = Column(String(100), nullable=True)
    Rank = Column(Double, nullable=True)
    Title = Column(String(200), nullable=True)
    ReadCount = Column(Integer, nullable=True)
    LikeCount = Column(Integer, nullable=True)
    Url = Column(String(200), nullable=True)
    Date = Column(Date, nullable=False)
    CommentCount = Column(Integer, nullable=True)
    ForwardCount = Column(Integer, nullable=True)
    Text = Column(String(500), nullable=True)

    # 关联关系
    data_assoc = relationship("KeywordsAssociation",
                                foreign_keys="[KeywordsAssociation.data_id]",
                                back_populates="data")

    def __init__(self, row):
        # 直接从row字典中提取值
        self.Id_txt = row.get('Id_txt')
        self.Author_Name = row.get('Author_Name')
        self.Author_Id = row.get('Author_Id')
        self.Author_Type = row.get('Author_Type')
        self.Domain = row.get('Domain')
        self.Rank = row.get('Rank')
        self.Title = row.get('Title')
        self.Text = row.get('Text')
        self.Content = row.get('Content')
        self.Url = row.get('Url')
        self.Date = row.get('Date')
        self.LikeCount = row.get('LikeCount')
        self.ReadCount = row.get('ReadCount')
        self.CommentCount = row.get('CommentCount')
        self.ForwardCount = row.get('ForwardCount')


class KeywordsAssociation(Base):
    __tablename__ = 'keywords_association'

    Id = Column(Integer, primary_key=True, autoincrement=True)
    keyword_id = Column(Integer, ForeignKey('Keywords.Id'), nullable=False)
    data_id = Column(Integer, ForeignKey('CombinedData.Id'), nullable=False)

    # 添加约束条件
    __table_args__ = (UniqueConstraint('keyword_id', 'data_id', name='association_UNIQUE'),)
    # 添加关联关系
    keyword = relationship("Keywords", foreign_keys=[keyword_id], back_populates="key_assoc")
    data = relationship("CombinedData", foreign_keys=[data_id], back_populates="data_assoc")

