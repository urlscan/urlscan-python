from typing import Literal

VisibilityType = Literal["public", "private", "unlisted"]
SearchType = Literal["search"]
RetrieveType = Literal["retrieve"]
ActionType = VisibilityType | SearchType | RetrieveType
LiveScanResourceType = Literal["result", "screenshot", "dom", "response", "download"]
SavedSearchDataSource = Literal["hostnames", "scans"]
TLPType = Literal["red", "amber+strict", "amber", "green", "clear"]
PermissionType = Literal["public:read", "team:read", "team:write"]
