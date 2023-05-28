import datetime
from typing import List

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .setup import Base


class Document(Base):
    __tablename__ = 'documents'

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    created: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now)
    updated: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now)
    
    files: Mapped[List['File']] = relationship('File',
                                            back_populates='document',
                                            foreign_keys=[],
                                            cascade="all, delete")
    numbers: Mapped[List['UniqueNumber']] = relationship('UniqueNumber',
                                                back_populates='document',
                                                foreign_keys=[], 
                                                cascade="all, delete")

    def __repr__(self):
        return f'''
        <Document 
        id:{self.id}, 
        name:{self.name}, 
        created:{self.created},
        updated:{self.updated}>
        '''


class File(Base):
    __tablename__ = 'files'

    id: Mapped[int] = mapped_column(primary_key=True)

    path: Mapped[str] = mapped_column(nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now)
    updated: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now)
    document_id: Mapped[int] = mapped_column(ForeignKey('documents.id'), nullable=False)

    document: Mapped['Document'] = relationship('Document',
                                                    back_populates='files',
                                                    foreign_keys=[document_id])
        
    def __repr__(self):
        return f'''
        <File 
        id:{self.id}, 
        path:{self.path}, 
        created:{self.created},
        updated:{self.updated}>
        '''

                                                
class UniqueNumber(Base):
    __tablename__ = 'unique_numbers'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # name: Mapped[str] = mapped_column(nullable=False, unique=True)
    number: Mapped[str] = mapped_column(nullable=False)
    created: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now)
    updated: Mapped[datetime.datetime] = mapped_column(nullable=False, default=datetime.datetime.now)
    document_id: Mapped[int] = mapped_column(ForeignKey('documents.id'), nullable=False)

    document: Mapped['Document'] = relationship('Document',
                                                    back_populates='numbers',
                                                    foreign_keys=[document_id])

    def serialize(self, exclude_keys: list[str]):
        print(self.metadata)

    def __repr__(self):
        return f'''
        <Uniq_number 
        id:{self.id}, 
        number:{self.number}, 
        created:{self.created},
        updated:{self.updated}>
        '''