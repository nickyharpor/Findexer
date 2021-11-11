import requests


class Findora:

    def __init__(self, rest_url):
        self.rest_url = rest_url

    def get_rest_block(self, num):
        res=requests.get(self.rest_url+"block", headers={"height": str(num)})
        return res.json()

    def get_status(self):
        res = requests.get(self.rest_url+"status")
        return res.json()

    def get_height(self):
        res = requests.get(self.rest_url+"status")
        block = res.json()["result"]["sync_info"]["latest_block_height"]
        return int(block)
