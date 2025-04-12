from typing import Literal

VisibilityType = Literal["public", "private", "unlisted"]
SearchType = Literal["search"]
RetrieveType = Literal["retrieve"]
ActionType = VisibilityType | SearchType | RetrieveType
