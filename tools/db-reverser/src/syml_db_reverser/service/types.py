from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional


class ForeignKeyOptions(Enum):
    RESTRICT = 'RESTRICT'
    CASCADE = 'CASCADE'
    NO_ACTION = 'NO_ACTION'
    SET_NULL = 'SET_NULL'
    SET_DEFAULT = 'SET_DEFAULT'


@dataclass
class CheckConstraintType:
    name: str
    condition: str


@dataclass
class ForeignKeyConstraintType:
    name: str
    columnNames: List[str]
    elements: List[str]  # table.columnKey
    onDelete: ForeignKeyOptions
    onUpdate: ForeignKeyOptions
    matchFull: bool


@dataclass
class Constraints:
    nullable: Optional[List[str]] = None
    primaryKey: Optional[List[str]] = None
    unique: Optional[List[str]] = None
    autoincrement: Optional[List[str]] = None
    foreignKeys: Optional[List[ForeignKeyConstraintType]] = None
    check: Optional[List[CheckConstraintType]] = None


@dataclass
class ColumnEntity:
    name: str
    type: str


@dataclass
class SpecTable:
    columns: List[ColumnEntity]
    constraints: Constraints


@dataclass
class TableEntity:
    name: str
    description: str
    spec: SpecTable
