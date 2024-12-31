import enum
import json
import time
from datetime import datetime, timedelta, timezone

import requests
import yaml



class ColNameStruct(enum.Enum):
    COIN_NAME = 'Name'
    COIN_ID_NAME = 'api id'
    LIVE_PRICE = 'Current Price'
    LAST_UPDATED = 'Last Updated'
    LAST_24H_CHANGE = '24H change'

class MyIntegration:

    def __init__(self):
        """
        Gets required variable data from config yaml file.
        """
        with open("my_variables.yml", 'r') as stream:
            try:
                self.my_variables_map = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print("[Error]: while reading yml file", exc)
        self.my_variables_map["NOTION_ENTRIES"] = {}
        self.getDatabaseId()
        self.getNotionDatabaseEntities()

    def getDatabaseId(self):
        # url = f'https://api.notion.com/v1/databases/{self.my_variables_map["DATABASE_ID"]}'
        # headers = {
        #     'Notion-Version': '2022-06-28',
        #     'Authorization':
        #         'Bearer ' + self.my_variables_map["MY_NOTION_SECRET_TOKEN"]
        # }
        # response = requests.request("GET", url, headers=headers)
        # print (response.json())
        # self.my_variables_map["DATABASE_ID"] = response.json()["id"]
        print (self.my_variables_map["DATABASE_ID"])
        

    def getNotionDatabaseEntities(self):
        url = f"https://api.notion.com/v1/databases/{self.my_variables_map['DATABASE_ID']}/query"
        headers = {
            'Notion-Version': '2022-06-28',
            'Authorization': 'Bearer ' + self.my_variables_map["MY_NOTION_SECRET_TOKEN"],
            'Content-Type': 'application/json',
        }
        response = requests.request("POST", url, headers=headers)
        resp = response.json()
        print ('getNotionDatabaseEntities', json.dumps(resp, indent=4))
        for v in resp["results"]:
            try:
                coin_name = v["properties"][ColNameStruct.COIN_NAME.value]["title"][0]["text"]["content"]
                # buy_price = v["properties"][ColNameStruct.COST_BASIS.value]["number"]
                coin_id_name = v["properties"][ColNameStruct.COIN_ID_NAME.value]["rich_text"][0]["text"]["content"]
            except Exception as e:
                print (e)
                continue
            self.my_variables_map["NOTION_ENTRIES"].update(
                {
                    coin_name: 
                        {
                            "page": v["id"], 
                            # "price": float(buy_price) if buy_price else None,
                            f"{ColNameStruct.COIN_ID_NAME.value}": coin_id_name,
                        }
            })
        print ('Notion Entries: ', json.dumps(self.my_variables_map["NOTION_ENTRIES"], indent=4) )



    def getCryptoPrices(self):
        """
        Download the required crypto prices using Binance API.
        Ref: https://github.com/binance/binance-api-postman
        """
        for name, data in self.my_variables_map["NOTION_ENTRIES"].items():
            coin_id_name = data[ColNameStruct.COIN_ID_NAME.value]
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {  
                    "ids": coin_id_name,
                    "vs_currencies": "USD",
                    "include_24hr_change": "true",
                    "precision": 4,
            }
            headers = { 'x-cg-demo-api-key': self.my_variables_map["COIN_API_KEY"]}
            response = requests.get(url, params = params, headers = headers)
            try:
                print (response.json())
                if response.status_code == 200:
                    content = response.json()
                    data[ColNameStruct.LIVE_PRICE.value] = content[coin_id_name]['usd']
                    data[ColNameStruct.LAST_24H_CHANGE.value] = content[coin_id_name]['usd_24h_change']
                    data[ColNameStruct.LAST_UPDATED.value] = datetime.now(timezone(timedelta(hours=-5), 'EST')).isoformat()
                    print (json.dumps(data, indent=1))
                if response.status_code == 400:
                    print(f"Invalid symbol: {name}USDT")
                    continue
            except Exception as e:
                print ('Exception : getCryptoPrices : ', e)
                continue



    def updateNotionDatabase(self, pageId, metadata):
        """
        A notion database (if integration is enabled) page with id `pageId`
        will be updated with the data `coinPrice`.
        """
        url = "https://api.notion.com/v1/pages/" + str(pageId)
        headers = {
            'Authorization':
                'Bearer ' + self.my_variables_map["MY_NOTION_SECRET_TOKEN"],
            'Notion-Version': '2021-05-13',
            'Content-Type': 'application/json'
        }
        # Construct the properties payload
        coinPrice = metadata[ColNameStruct.LIVE_PRICE.value]
        last24hChange = metadata[ColNameStruct.LAST_24H_CHANGE.value]
        lastUpdatedTime = metadata[ColNameStruct.LAST_UPDATED.value]
        properties = {
            f"{ColNameStruct.LIVE_PRICE.value}": {
                "type": "number",
                "number": float(coinPrice),
            }
        }
        if last24hChange:
            # percentage, so divide / 100, for 0.xx = xx %
            print (float(last24hChange))
            properties[f"{ColNameStruct.LAST_24H_CHANGE.value}"] = {
                "type": "number",
                "number": round(last24hChange/100, 4),
            }

        if lastUpdatedTime:
            properties[f"{ColNameStruct.LAST_UPDATED.value}"] = {
                "type": "date",
                "date": {"start": lastUpdatedTime},
            }
        payload = json.dumps({"properties": properties})
        print ('\n\n')
        print(requests.request(
                "PATCH", url, headers=headers, data=payload
            ).text)

    def UpdateIndefinitely(self):
        """
        Orchestrates downloading prices and updating the same
        in notion database.
        """
        while True:
            try:
                self.getCryptoPrices()
                for _, data in self.my_variables_map["NOTION_ENTRIES"].items():
                    if ColNameStruct.LIVE_PRICE.value in data and 'page' in data:
                        self.updateNotionDatabase(
                            pageId=data['page'],
                            metadata=data
                        )
                    # Sleep 1 second after updating a coin
                    time.sleep(1)
                # Sleep 60 seconds after updating all coins
                time.sleep(5 * 60)
                self.getNotionDatabaseEntities()
            except Exception as e:
                print(f"[Error encountered]: {e}")


if __name__ == "__main__":
    # With 😴 sleeps to prevent rate limit from kicking in.
    MyIntegration().UpdateIndefinitely()