import requests
import time


def get_wallet_data(wallet_address):
    global totalvolume
    global last_occurence
    global first_occurence
    global mintbluechip

    headers = {
        'accept': 'application/json',
        'X-API-Key': 'Jz4hOYxGXFXQP7J7ZjSNvJUaduJIxO3cXkX8XcJMUHIXQeNuzPlmxV5UrL3LxAwL',
        # 'Authorization: Bearer': '269:c4594vx1s5t6g0a4stnlicl3fsbx6mqfiuxuk5t6pgu8qrt9', #Auth token for compass.
    }

    params = {
        'chain': 'eth',
        'format': 'decimal',
    }
    get_wallet_transctions = requests.get(
        'https://deep-index.moralis.io/api/v2/' + wallet_address + '?from_date=2017-03-01T12:21:03.000Z',
        headers=headers)
    response_moralis = requests.get(
        'https://deep-index.moralis.io/api/v2/' + wallet_address + '/nft/transfers?chain=eth&format=decimal&direction=both',
        headers=headers)  # Moralis API
    get_eth_balance = requests.get('https://deep-index.moralis.io/api/v2/' + wallet_address + '/balance',
                                   headers=headers)
    get_erc20_balance = requests.get('https://deep-index.moralis.io/api/v2/' + wallet_address + '/erc20',
                                     headers=headers)
    get_erc20_price = requests.get(
        'https://deep-index.moralis.io/api/v2/' + wallet_address + '/erc20/0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2/price',
        headers=headers)
    x = response_moralis.json()
    y = x

    marektplaces_address = ["0x7be8076f4ea4a4ad08075c2508e481d6c946d12b", "0x7f268357a8c2552623316e2562d90e642bb538e5",
                            "0x59728544b08ab483533076417fbbb2fd0b17ce3a"]
    # print (y)

    # Get_WEI_BALANCE
    a = get_eth_balance.json()
    amount = a['balance']
    eth_balance = int(amount) / (10 ** 18)  # conver wei to ether
    print("Eth Balance:", eth_balance)
    b = get_erc20_balance.json()
    # print (b)
    # print (get_erc20_price)

    # c = get_erc20_price.json()
    # print (c)

    # ------------------------------------#
    WALLET_NAME = {"id": wallet_address}
    query = {
        "query": "query wallet($where: WalletWhereUniqueInput!) {\n  wallet(where: $where) {\n    id\n    name\n    openseaProfile\n    updatedAt\n    displayName\n    totalPortfolioValue\n    passBalance\n  }\n}",
        "variables": {"where": WALLET_NAME}, "operationName": "wallet"}

    res = requests.post("https://api.compass.art/graphql", json=query, headers={
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7InVzZXJJZCI6MzgzODZ9LCJpYXQiOjE2NjUxMzA5NzksImV4cCI6MTY2NTczNTc3OX0.vcns3BGc6g1XJRS0FaWrU4E21qpBiPGZkjvkoEt037E"})
    c = res.json()
    portfolio_value = c['data']['wallet']['totalPortfolioValue']
    print("NFT Portfolio Value:", portfolio_value)

    # Total Volume
    def get_transctions(cursor):
        global totalvolume
        global last_occurence
        global first_occurence
        url = 'https://deep-index.moralis.io/api/v2/' + wallet_address + '?from_date=2017-03-01T12:21:03.000Z'
        if cursor:
            url = url + "&cursor=%s" % cursor

        statusResponse = requests.request("GET", url, headers=headers)

        data = statusResponse.json()

        for item in data["result"]:
            if item["to_address"] in marektplaces_address:
                # print(item["value"])
                totalvolume += int(item["value"])

        cursor = data['cursor']
        # print(data['page'], data['total'])
        return cursor

    totalvolume = 0
    cursor = -2
    while cursor is not None:
        if cursor == -2:
            cursor = None

        cursor = get_transctions(cursor)
        time.sleep(1.1)

    totalvolume = totalvolume / (10 ** 18)
    print("Total Trading Volume:", totalvolume)

    # Checking First/Last Mint date

    def get_nft_transctions_date(cursor):
        global last_occurence
        global first_occurence
        url = 'https://deep-index.moralis.io/api/v2/' + wallet_address + '/nft/transfers?chain=eth&format=decimal&direction=both'  # Moralis API
        if cursor:
            url = url + "&cursor=%s" % cursor

        statusResponse = requests.request("GET", url, headers=headers)

        data = statusResponse.json()
        # print (data)
        for item in data["result"]:
            if item["from_address"] == "0x0000000000000000000000000000000000000000":
                if item["block_timestamp"] > last_occurence:
                    last_occurence = item["block_timestamp"]
                if item["block_timestamp"] < first_occurence:
                    first_occurence = item["block_timestamp"]

        cursor = data['cursor']
        # print(data['page'], data['total'])
        return cursor

    last_occurence = "1990-03-01T12:21:03.000Z"
    first_occurence = "2030-03-01T12:21:03.000Z"
    cursor = -2
    while cursor is not None:
        if cursor == -2:
            cursor = None

        cursor = get_nft_transctions_date(cursor)
        time.sleep(1.1)

    print("First Mint Date:", first_occurence)

    # Checking if you minted a bluechip

    def get_nft_transctions(cursor):
        global mintbluechip
        url = 'https://deep-index.moralis.io/api/v2/' + wallet_address + '/nft/transfers?chain=eth&format=decimal&direction=both'  # Moralis API
        if cursor:
            url = url + "&cursor=%s" % cursor

        statusResponse = requests.request("GET", url, headers=headers)

        data = statusResponse.json()
        # print (data)
        for item in data["result"]:
            if item["from_address"] == "0x0000000000000000000000000000000000000000":  # mint addres
                if item[
                    "token_address"] == "0xc8adfb4d437357d0a656d4e62fd9a6d22e401aa0":  # token address = the collection address
                    mintbluechip = 1

        cursor = data['cursor']
        # print(data['page'], data['total'])
        return cursor

    mintbluechip = 0
    cursor = -2
    while cursor is not None:
        if cursor == -2:
            cursor = None

        cursor = get_nft_transctions(cursor)
        time.sleep(1.1)

    print("Did you mint a bluechip?", mintbluechip)

    alldate_response = {"nft_protfolio_value:": portfolio_value, "first_mint_date": first_occurence,
                        "mint_bluechip:": mintbluechip, "total_trading_value": totalvolume}

    return alldate_response


# check trading volume


# {'data': {'wallet': {'id': '0x2749ccb49b16e53c956ebb28162bb66089f78806', 'name': None, 'openseaProfile': None, 'updatedAt': '2022-01-17T17:52:59.563Z', 'displayName': '0x2749', 'totalPortfolioValue': 1.12692, 'passBalance': 0}}}

"""


#get block number 
block_number = y['result'][-1]['block_number']
print (block_number)


#value sumup
counter = 0 

for item in y["result"]:
    counter = counter + int(item["value"])

print (counter)


#how many mints

countermint = 0 
for item in y["result"]:
    if item["from_address"] == "0x0000000000000000000000000000000000000000":
        countermint += 1
print (countermint)

"""