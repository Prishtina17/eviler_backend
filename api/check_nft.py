import asyncio
import base64
import struct

import aiohttp
import base58
import requests
import json
import asn1
from solana.rpc.api import Client
from solana.rpc.async_api import AsyncClient
from solana.rpc.types import TokenAccountOpts
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from construct import Bytes, Int8ul, Int32ul, Int64ul, Pass, Switch
from construct import Struct as cStruct
from solders.signature import Signature
from spl.token._layouts import PUBLIC_KEY_LAYOUT
from spl.token.client import Token
from eviler.settings import MORALIS_API

from moralis import sol_api

#from eviler import settings

collection_symbol = "NB"
def moralis_get_nft(public_key: str) -> list[dict]:
    params = {
        "network": "devnet",
        "address": public_key
    }

    result = sol_api.account.get_nfts(
        api_key=MORALIS_API,
        params=params,
    )
    nfts_metadata = []
    for token in result:
        #print(token)
        if token["symbol"] == collection_symbol:
            params = {
                "network": "devnet",
                "address": str(token["mint"])
            }
            token_metadata = sol_api.nft.get_nft_metadata(
                api_key=MORALIS_API,
                params=params,
            )
            nfts_metadata.append(token_metadata)
    #print(nfts_metadata)
    return nfts_metadata

async def async_fetch_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await response.text()
                else:
                    return f"Error: {response.status}"
    except aiohttp.InvalidURL:
        return "Invalid URL"
def fetch_url(url):
  try:
    response = requests.get(url)
    if response.status_code == 200:
      return response.text
    else:
      raise requests.exceptions.RequestException
      #return f"Error: {response.status_code}"
  except requests.exceptions.RequestException as e:
    return e

#Deprecated methods to get nft metadata from solana api
"""

METADATA_PROGRAM_ID = Pubkey.from_string('metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s')

client = Client("https://api.mainnet-beta.solana.com")
token_client = Client("https://api.mainnet-beta.solana.com")


ACCOUNT_LAYOUT = cStruct(
    "mint" / PUBLIC_KEY_LAYOUT,
    "owner" / PUBLIC_KEY_LAYOUT,
    "amount" / Int64ul,
    "delegate_option" / Int32ul,
    "delegate" / PUBLIC_KEY_LAYOUT,
    "state" / Int8ul,
    "is_native_option" / Int32ul,
    "is_native" / Int64ul,
    "delegated_amount" / Int64ul,
    "close_authority_option" / Int32ul,
    "close_authority" / PUBLIC_KEY_LAYOUT,
)
def unpack_metadata_account(data):

    assert(data[0] == 4)
    i = 1
    source_account = base58.b58encode(bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
    i += 32
    mint_account = base58.b58encode(bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
    i += 32
    name_len = struct.unpack('<I', data[i:i+4])[0]
    i += 4
    name = struct.unpack('<' + "B"*name_len, data[i:i+name_len])
    i += name_len
    symbol_len = struct.unpack('<I', data[i:i+4])[0]
    i += 4
    symbol = struct.unpack('<' + "B"*symbol_len, data[i:i+symbol_len])
    i += symbol_len
    uri_len = struct.unpack('<I', data[i:i+4])[0]
    i += 4
    uri = struct.unpack('<' + "B"*uri_len, data[i:i+uri_len])
    i += uri_len
    fee = struct.unpack('<h', data[i:i+2])[0]
    i += 2
    has_creator = data[i]
    i += 1
    creators = []
    verified = []
    share = []
    if has_creator:
        creator_len = struct.unpack('<I', data[i:i+4])[0]
        i += 4
        for _ in range(creator_len):
            creator = base58.b58encode(bytes(struct.unpack('<' + "B"*32, data[i:i+32])))
            creators.append(creator)
            i += 32
            verified.append(data[i])
            i += 1
            share.append(data[i])
            i += 1
    primary_sale_happened = bool(data[i])
    i += 1
    is_mutable = bool(data[i])
    metadata = {
        "update_authority": source_account,
        "mint": mint_account,
        "data": {
            "name": bytes(name).decode("utf-8").strip("\x00"),
            "symbol": bytes(symbol).decode("utf-8").strip("\x00"),
            "uri": bytes(uri).decode("utf-8").strip("\x00"),
            "seller_fee_basis_points": fee,
            "creators": creators,
            "verified": verified,
            "share": share,
        },
        "primary_sale_happened": primary_sale_happened,
        "is_mutable": is_mutable,
    }
    return metadata



def get_nfts(user_public_key: str) -> list[dict]:
    #TODO: какого то хуя возвращает только 1 нфт, хотя должен 2
    a = client.get_token_accounts_by_owner(Pubkey.from_string(user_public_key),
                                          TokenAccountOpts(program_id=Pubkey.from_string("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")), )
    uris = []
    output = []
    for token in a.value:
        #print(token.to_json())
        bytes_data = base64.b64decode(json.loads(token.to_json())["account"]["data"][0])

        decoded_data = ACCOUNT_LAYOUT.parse(bytes_data)
        mint = Pubkey(decoded_data.mint)
        ttt = Pubkey.find_program_address([b'metadata', bytes(METADATA_PROGRAM_ID), bytes(mint)],
                                          METADATA_PROGRAM_ID)[0]
        b = client.get_account_info(ttt)
        metadata = ""
        try:
            metadata = unpack_metadata_account(bytes(json.loads(b.value.to_json())["data"]))
            uri = metadata["data"]["uri"]
        except AttributeError:
            continue
        try:
            token_metadata = unpack_metadata_account(bytes(json.loads(b.value.to_json())["data"]))

            uri = token_metadata["data"]["uri"]
            if uri != "":
                response = json.loads(fetch_url(uri))
                response["mint"] = str(mint)
                if response["collection"]["name"] == settings.NFT_COLLECTION_NAME:
                    output.append(response)


        except Exception:
            continue
    return output

def check_transaction():
    sol_value = "0.001"
    client = Client("http://186.233.184.93:8899")
    user = Pubkey.from_string("B2u6ibu8QQ71fcEVpPvwhG4wTU5rVF6KpZzDHcvgEnaX")
    sigs = client.get_signatures_for_address(user, limit =1)
    for sig in sigs.value:
        signature = json.loads(sig.to_json())["signature"]
        print(signature)
        tx = client.get_transaction(Signature.from_string(signature))
        eviler_account = json.loads(tx.value.to_json())["message"]["accountKeys"][1]
        if eviler_account != settings.SOLANA_ACCOUNT:
            continue
        values = json.loads(tx.value.to_json())["meta"]
        pre = values["preBalances"]
        post = values["postBalances"]

        if (post[1] - pre[1]) == sol_value:
            print("succes")

"""

#print(asyncio.run(get_nfts("DywvRGQzikkTfgakuh76WGKru7FWHX3HnFgS1CUGzGQt")))
#moralis_get_nft("DywvRGQzikkTfgakuh76WGKru7FWHX3HnFgS1CUGzGQt")