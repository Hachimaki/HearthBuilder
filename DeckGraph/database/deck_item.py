from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


# class Association(Base):
#     __tablename__ = "Association"
#     left_dbfId = Column(Integer, ForeignKey('DeckItem.dbfId'), primary_key=True)
#     left_count = Column(Integer, ForeignKey('DeckItem.count'), primary_key=True)
#     left_arch = Column(Integer, ForeignKey('DeckItem.archtype'), primary_key=True)
#
#     right_dbfId = Column(Integer, ForeignKey('DeckItem.dbfId'), primary_key=True)
#     right_count = Column(Integer, ForeignKey('DeckItem.count'), primary_key=True)
#     right_arch = Column(Integer, ForeignKey('DeckItem.archtype'), primary_key=True)
#
#     associates = relationship("DeckItem", back_populates="associates")

class Edge(Base):
    __tablename__ = "Edge"

    node1_id = Column(Integer, ForeignKey('Node.id'), primary_key=True)
    node2_id = Column(Integer, ForeignKey('Node.id'), primary_key=True)

    weight = Column(Integer)

    node1 = relationship("Node", primaryjoin='Edge.node1_id == Node.id', backref="edges")
    node2 = relationship("Node", primaryjoin='Edge.node2_id == Node.id')

    # nodes = relationship("Node",
    #                      foreign_keys=[node1_id, node2_id],
    #                      back_populates="edges")

    # nodes = relationship("Node", primaryjoin='and_(Edge.node1_id == Node.id, Edge.node2_id == Node.id)', backref="edges")


class Node(Base):
    __tablename__ = "Node"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dbfId = Column(Integer)
    count = Column(Integer)
    archetype = Column(Integer)

