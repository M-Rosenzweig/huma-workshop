from typing import Any, Dict, List
import requests
import config
import json
from web3 import Web3
# from dotenv import load_dotenv
# import os

# load_dotenv()
# provider_url = os.getenv("ALCHEMY_API")



# test the connection by getting the latest block number
# latest_block = web3.eth.blockNumber
# print("Latest block number:", latest_block)



def fetch_signal(signal_names: List[str], adapter_inputs: Dict[str, Any]) -> Dict[str, Any]: 
   """Fetch signals from the decentralized signal portfolio service.
   THIS FUNCTION GETS SIGNALS FROM THE HUMA SIGNALS SERVICE.

   
   For more details about DSP service, see https://github.com/00labs/huma-signals/tree/main/huma_signals
   """
   request = {"signal_names": signal_names, "adapter_inputs": adapter_inputs}
   response = requests.post(config.signals_endpoint, json=request)
   if response.status_code != 200:
       raise ValueError(f"Error fetching signals: {response.text}")
   return {k: v for k, v in response.json().get("signals").items() if k in signal_names}


def get_credit_total(borrower_wallet_address: str) -> int:
    """
    Check the credit limit for the borrower based on the value returned by the TribeCredit smart contract.
    
    :param borrower_wallet_address: The borrower's wallet address.
    :return: The credit limit for the borrower.
    """
    web3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    with open('abi/TribeCredit.json') as f:


    
    # Connect to the TribeCredit smart contract and retrieve the credit limit.
        tribe_credit = web3.eth.contract(address=config.tribe_credit_address, abi= json.load(f))
        credit_limit = tribe_credit.functions.tribeDetails(borrower_wallet_address).call()
    
    # Calculate the underwrite amount based on the credit limit and return it.
    print(credit_limit)
    underwrite_amount = credit_limit * 0.2
    return underwrite_amount


def underwrite(huma_pool, **kwargs):
    """
    The interface function between an EA and Huma EA service.
    
    :param huma_pool: the object that represents huma pool contract.
    :param **kwargs:
        - poolAddress: str: the address for the destiny huma pool.
        - borrowerWalletAddress: str: the borrower's wallet address.
    :return: Returns corresponding fields to UI.
    """

    borrower_wallet_address = kwargs["borrowerWalletAddress"]
    underwrite_amount = get_credit_total(borrower_wallet_address)

    # 
    
    # # Creating a result dictionary based on the calculated underwrite amount.
    result = {
        "creditLimit": int(underwrite_amount),
        "intervalInDays": 30,
        "remainingPeriods": 12,
        "aprInBps": 0
    }

    # signal_names = [
    #     "TribeCredit.credit_total",
    #     # "TribeCredit.credit_available",
    # ]

    # adapter_inputs = {"borrower_wallet_address": borrower_wallet_address}

    # signals = fetch_signal(signal_names, adapter_inputs)
    # if signals.get("TribeCredit.credit_total") is > 0: {
    #     result = {
    #     "creditLimit": int(underwrite_amount),
    #     "intervalInDays": 30,
    #     "remainingPeriods": 12,
    #     "aprInBps": 0
    #     }
    # }
    
    
    return result