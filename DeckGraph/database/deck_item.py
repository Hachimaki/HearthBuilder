from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

node2arch = Table('node2arch',
                  Base.metadata,
                  Column('archetype_id', Integer, ForeignKey('Archetype.id')),
                  Column('node_id', Integer, ForeignKey('Node.id'))
                 )

card2arch = Table('card2arch',
                  Base.metadata,
                  Column('archetype_id', Integer, ForeignKey('Archetype.id')),
                  Column('card_id', Integer, ForeignKey('Card.id'))
                 )


class Archetype(Base):
    __tablename__ = "Archetype"
    id = Column(Integer, primary_key=True)
    node = relationship("Node", secondary=node2arch, back_populates="archetype")
    card = relationship("Card", secondary=card2arch, back_populates="archetype")


class Edge(Base):
    __tablename__ = "Edge"

    node1_id = Column(Integer, ForeignKey('Node.id'), primary_key=True)
    node2_id = Column(Integer, ForeignKey('Node.id'), primary_key=True)

    node1 = relationship("Node", primaryjoin='Edge.node1_id == Node.id')
    node2 = relationship("Node", primaryjoin='Edge.node2_id == Node.id')

    weight = Column(Integer)


class Node(Base):
    __tablename__ = "Node"
    id = Column(Integer, primary_key=True, autoincrement=True)
    dbfId = Column(Integer, ForeignKey('Card.id'))
    count = Column(Integer)

    archetype = relationship("Archetype", secondary=node2arch, back_populates="node")
    card = relationship("Card", primaryjoin='Node.dbfId == Card.id')


class Card(Base):
    __tablename__ = "Card"
    id = Column(Integer, primary_key=True)
    name = Column(String)

    archetype = relationship("Archetype", secondary=card2arch, back_populates="card")
    nodes = relationship('Node', back_populates="card")
