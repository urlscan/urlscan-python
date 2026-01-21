::: urlscan.Pro

::: urlscan.pro.Brand

::: urlscan.pro.Channel

::: urlscan.pro.DataDump

Note: you can use `extract` function in the utils module to extract a downloaded data dump file.

```py
import os

from urlscan import Pro
from urlscan.utils import extract

with Pro("<your_api_key>") as pro:
    # get a list of hourly API data dump files
    res = pro.datadump.get_list("hours/api/20260101/")

    # download & extract them one by one
    for f in res["files"]
        path: str = f["path"]

        basename = os.path.basename(path)
        with open(basename, "wb") as file:
            pro.datadump.download_file(path, file=file)

        extract(basename, "/tmp")
```

::: urlscan.pro.HostnameIterator

::: urlscan.pro.Incident

::: urlscan.pro.LiveScan

::: urlscan.pro.SavedSearch

::: urlscan.pro.Subscription
