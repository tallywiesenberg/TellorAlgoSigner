'''DataSource class'''

class DataSource:
    def __init__(self, asset, url, request_parsers, subgraph=False):
        self.asset = (asset,)
        self.url = (url,)
        self.request_parsers = (request_parsers,)
        self.subgraph = subgraph