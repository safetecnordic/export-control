"Provides utility type aliases for easier type hinting."

from typing import TypeAlias, TypeVar, Union
from django.db import models
from django.db.models.expressions import Combinable


M = TypeVar("M")
ForeignKey: TypeAlias = models.ForeignKey[Union[M, Combinable], M]

CharField: TypeAlias = "models.CharField[Union[str, int, Combinable], str]"
TextField: TypeAlias = "models.TextField[Union[str, Combinable], str]"
BooleanField: TypeAlias = "models.CharField[Union[bool, int, Combinable], bool]"
IntegerField: TypeAlias = "models.IntegerField[Union[float, int, str, Combinable], int]"
DateTimeField: TypeAlias = "models.DateTimeField"
