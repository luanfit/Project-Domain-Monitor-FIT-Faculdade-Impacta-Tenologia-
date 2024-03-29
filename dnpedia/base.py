# -*- coding: utf-8 -*-
import requests
import json

class DnPediaAPIBase(object):
    BASE_URL = "https://dnpedia.com/tlds/ajax.php"

    BASE_HEADER = {
        "User-Agent": "DnPedia API wrapper for Python",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://dnpedia.com/tlds/search.php",
        "X-Requested-With": "XMLHttpRequest"
    }

    MODE_TYPE = {
        "recentlyAdded": "added",
        "recentlyDeleted": "deleted",
        "currentZones": "full"
    }

    MATCH_TYPE = {
        "startswith": "~{keyword}%",
        "endswith": "~%{keyword}",
        "contains": "~%{keyword}%"
    }

    COLUMNS_TYPE = {
        "recentlyAdded": "name,zoneid,thedate,",
        "recentlyDeleted": "name,zoneid,thedate,",
        "currentZones": "name,zoneid,"
    }

    def __init__(self):
        pass

    def create_query(self, keyword, columns, days, mode):
        return {
            "cmd": "search",
            "columns": columns,
            "ecf": "name",
            "ecv": keyword,
            "days": days,
            "mode": mode,
            "_search": "false",
            "nd": "1575288353190",
            "rows": "500",
            "page": "1",
            "sidx": "length",
            "sord": "asc"
        }
    
    def search(self, keyword, match_type="contains", days=7, mode_type="recentlyAdded"):
        """
        Arguments:
            keyword {str} -- search keyword
        
        Keyword Arguments:
            match_type {str} -- [startswith/endswith/contains (default: {"contains"})
            days {int} -- Where (default: {1})
            mode_type {str} -- recentlyAdded/recentlyDeleted/currentZones (default: {"recentlyAdded"})
        
        Returns:
            [type] -- json
        """
        query = self.create_query(
            keyword=self.MATCH_TYPE[match_type].format(keyword=keyword),
            columns=self.COLUMNS_TYPE[mode_type],
            days=days,
            mode=self.MODE_TYPE[mode_type]
        )

        r = requests.get(
            url=self.BASE_URL,
            params=query,
            headers=self.BASE_HEADER
        )

        if r.status_code == 200:
            r.encoding = r.apparent_encoding
            return r.json()
        else:
            return {}
