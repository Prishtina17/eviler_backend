import uuid

import requests
import json

url = "https://fittest-palpable-energy.solana-mainnet.quiknode.pro/90c80e20b7f922353fcf54f7fd222daf16a8f742/"

payload = json.dumps({
  "id": 67,
  "jsonrpc": "2.0",
  "method": "qn_fetchNFTs",
  "params": {
    "wallet": "HZdoqGiwv7iihzDJvAnoYtMg65n3P4VQoD9HjV7m1DT6",


  }
})
headers = {
  'Content-Type': 'application/json',
  'x-qn-api-version': '1'
}

print(uuid.uuid4())