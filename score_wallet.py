import requests
from datetime import datetime

def get_wallet_data(wallet_address):
    headers = {
        'accept': 'application/json',
        'X-API-Key': 'Jz4hOYxGXFXQP7J7ZjSNvJUaduJIxO3cXkX8XcJMUHIXQeNuzPlmxV5UrL3LxAwL',
        #'Authorization: Bearer': '269:c4594vx1s5t6g0a4stnlicl3fsbx6mqfiuxuk5t6pgu8qrt9', #Auth token for compass.
    }
    #wallet_address = '0x2749ccb49b16E53C956ebB28162BB66089f78806'
    marektplaces_address = ["0x7be8076f4ea4a4ad08075c2508e481d6c946d12b","0x7f268357a8c2552623316e2562d90e642bb538e5","0x59728544b08ab483533076417fbbb2fd0b17ce3a"]
    bluechip_address = ["0xed5af388653567af2f388e6224dc7c4b3241c544","0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d","0x49cf6f5d44e70224e2e23fdcdd2c053f30ada28b","0x8a90cab2b38dba80c64b7734e58ee1db38b8992e","0x1a92f7381b9f03921564a437210bb9396471050c"]
    api_key = '59NZ15ZA5D5MD5UNMQ6ZRU8P257U71XJD2'
    get_wallet_transctions= requests.get('https://api.etherscan.io/api?module=account&action=txlist&address=' + wallet_address + '&startblock=0&endblock=99999999&offset=10&sort=asc&apikey=' + api_key, headers=headers)
    a = get_wallet_transctions.json()
    totalvolume = 0
    for item in a["result"]:
            if item["to"] in marektplaces_address:
                #print(item["value"])
                totalvolume += int(item["value"])

    totalvolume = totalvolume / (10**18)
    print ("Total Volume:", totalvolume)


    mintbluechip = 0



    for i in range(len(bluechip_address)):
        erc721 = requests.get('https://api.etherscan.io/api?module=account&action=tokennfttx&contractaddress=' + bluechip_address[i] + '&address=' + wallet_address + '&page=1&offset=100&startblock=0&endblock=99999999&sort=asc&apikey=' + api_key, headers=headers)
        b = erc721.json()
        if (b["status"] > '0'):
            mintbluechip = 1
            #print (bluechip_address[i]) this will print the contract of the bluechip collection


    print ("Did you mint a bluechip?", mintbluechip)


    erc721_date = requests.get('https://api.etherscan.io/api?module=account&action=tokennfttx&address=' + wallet_address + '&page=1&offset=100&startblock=0&endblock=99999999&sort=asc&apikey=' + api_key, headers=headers)
    c = erc721_date.json()
    last_occurence = '0'
    first_occurence = '9999999999'

    for item in c["result"]:
        if item["from"] == "0x0000000000000000000000000000000000000000":
            if item["timeStamp"] > last_occurence:
                last_occurence = item["timeStamp"]
            if item["timeStamp"] < first_occurence:
                first_occurence = item["timeStamp"]

    first_occurence = int(first_occurence)
    dt_object = datetime.fromtimestamp(first_occurence)
    print("First Mint Date:", dt_object)






    get_eth_balance = requests.get('https://deep-index.moralis.io/api/v2/' + wallet_address + '/balance',headers=headers)
    #Get_WEI_BALANCE
    a = get_eth_balance.json()
    amount = a['balance']
    eth_balance = int(amount) / (10 ** 18)  # conver wei to ether
    print("Eth Balance:", eth_balance)

    WALLET_NAME = {"id": wallet_address}
    query = {
        "query": "query wallet($where: WalletWhereUniqueInput!) {\n  wallet(where: $where) {\n    id\n    name\n    openseaProfile\n    updatedAt\n    displayName\n    totalPortfolioValue\n    passBalance\n  }\n}",
        "variables": {"where": WALLET_NAME}, "operationName": "wallet"}

    res = requests.post("https://api.compass.art/graphql", json=query, headers={
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InVzZXJJZCI6MzgzODZ9LCJpYXQiOjE2NjU3NDI0NjUsImV4cCI6MTY2NjM0NzI2NX0.Ea7_MoNiNHhcZ16xqr0rTqogfiIDy_MWDFEYHHxW48A"})
    c = res.json()
    portfolio_value = c['data']['wallet']['totalPortfolioValue']

    print("NFT Portfolio Value:", portfolio_value)

    alldate_response = {"nft_protfolio_value": portfolio_value, "first_mint_date": dt_object,"mint_bluechip": mintbluechip, "total_trading_value": totalvolume, "eth_balance": eth_balance}

    return alldate_response