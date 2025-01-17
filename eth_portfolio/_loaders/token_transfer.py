import asyncio
import decimal
import logging
from contextlib import suppress
from decimal import Decimal
from typing import Optional

from brownie import chain
from brownie.exceptions import ContractNotFound
from brownie.network.event import _EventItem
from dank_mids.semaphores import BlockSemaphore
from pony.orm import TransactionIntegrityError
from y import ERC20, Contract
from y.decorators import stuck_coro_debugger
from y.exceptions import ContractNotVerified, NonStandardERC20
from y.utils.events import decode_logs

from eth_portfolio._db import utils as db
from eth_portfolio._loaders.utils import get_transaction_receipt
from eth_portfolio._shitcoins import SHITCOINS
from eth_portfolio.structs import TokenTransfer
from eth_portfolio.utils import _get_price

logger = logging.getLogger(__name__)

token_transfer_semaphore = BlockSemaphore(5_000, name='eth_portfolio.token_transfers')  # Some arbitrary number

shitcoins = SHITCOINS.get(chain.id, set())

@stuck_coro_debugger
async def load_token_transfer(transfer_log: dict, load_prices: bool) -> Optional[TokenTransfer]:
    if transfer_log['address'] in shitcoins:
        return None
    
    if transfer := await db.get_token_transfer(transfer_log):
        if load_prices and transfer.price is None:
            await db.delete_token_transfer(transfer)
        else:
            return transfer
    
    async with token_transfer_semaphore[transfer_log["blockNumber"]]:
        decoded = await _decode_token_transfer(transfer_log)
        if decoded is None:
            return None
        token = ERC20(decoded.address, asynchronous=True)
        coros = [token.scale, get_symbol(token), get_transaction_index(decoded.transaction_hash)]
        if load_prices:
            coros.append(_get_price(token.address, decoded.block_number))
            scale, symbol, transaction_index, price = await asyncio.gather(*coros)
        else:
            scale, symbol, transaction_index = await asyncio.gather(*coros)
        
        sender, receiver, value = decoded.values()
        value = Decimal(value) / Decimal(scale)
        
        token_transfer = {
            'chainid': chain.id,
            'block_number': decoded.block_number,
            'transaction_index': transaction_index,
            # TODO figure out why it comes in both ways
            'hash': hash.hex() if isinstance((hash := decoded.transaction_hash), bytes) else hash,
            'log_index': decoded.log_index,
            'token': symbol,
            'token_address': decoded.address,
            'from_address': str(sender),
            'to_address': str(receiver),
            'value': value,
        }
        if load_prices:
            try:
                price = round(Decimal(price), 18) if price else None
            except Exception as e:
                logger.error(f"{e.__class__.__name__} {e} for {symbol} {decoded.address} at block {decoded.block_number}.")
                price = None
            token_transfer['price'] = price
            token_transfer['value_usd'] = round(value * price, 18) if price else None
        
        transfer = TokenTransfer(**token_transfer)
        with suppress(decimal.InvalidOperation):  # Not entirely sure why this happens, probably some crazy uint value
            try:
                await db.insert_token_transfer(transfer)
            except TransactionIntegrityError:
                if load_prices:
                    await db.delete_token_transfer(transfer)
                    await db.insert_token_transfer(transfer)
        return transfer

@stuck_coro_debugger
async def get_symbol(token: ERC20) -> Optional[str]:
    try:
        return await token.__symbol__(sync=False)
    except NonStandardERC20:
        return None

@stuck_coro_debugger
async def get_transaction_index(hash: str) -> int:
    receipt = await get_transaction_receipt(hash)
    return receipt.transactionIndex

@stuck_coro_debugger
async def _decode_token_transfer(log) -> _EventItem:
    try:
        await Contract.coroutine(log['address'])
    except ContractNotFound:
        logger.warning(f"Token {log['address']} cannot be found. Skipping. If the contract has been self-destructed, eth-portfolio will not support it.")
    except ContractNotVerified:
        logger.warning(f"Token {log['address']} is not verified and is most likely a shitcoin. Skipping. Please submit a PR at github.com/BobTheBuidler/eth-portfolio if this is not a shitcoin and should be included.")
        return
    try:
        try:
            event = decode_logs(
                [log]
            )  # NOTE: We have to decode logs here because NFTs prevent us from batch decoding logs
        except Exception as e:
            raise e
        try:
            events = event['Transfer']
        except Exception as e:
            logger.error(event)
            raise e
        try:
            return events[0]
        except Exception as e:
            logger.error(event)
            raise e
    except Exception as e:
        logger.error('unable to decode logs, dev figure out why')
        logger.error(e)
        logger.error(log)