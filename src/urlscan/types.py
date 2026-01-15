from typing import Literal

VisibilityType = Literal["public", "private", "unlisted"]
SearchType = Literal["search"]
RetrieveType = Literal["retrieve"]
ActionType = VisibilityType | SearchType | RetrieveType
LiveScanResourceType = Literal["result", "screenshot", "dom", "response", "download"]
SavedSearchDataSource = Literal["hostnames", "scans"]
TLPType = Literal["red", "amber+strict", "amber", "green", "clear"]
PermissionType = Literal["public:read", "team:read", "team:write"]
SubscriptionFrequencyType = Literal["live", "hourly", "daily"]
WeekDaysType = Literal[
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]
SubscriptionPermissionType = Literal["team:read", "team:write"]
IncidentVisibilityType = Literal["unlisted", "private"]
IncidentCreationModeType = Literal["none", "default", "always", "ignore-if-exists"]
IncidentWatchKeyType = Literal[
    "scans/page.url",
    "scans/page.domain",
    "scans/page.ip",
    "scans/page.apexDomain",
    "hostnames/hostname",
    "hostnames/ip",
    "hostnames/domain",
]
ScanIntervalModeType = Literal["automatic", "manual"]
WatchedAttributeType = Literal[
    "detections", "tls", "dns", "labels", "page", "meta", "ip"
]
