import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor
from contextlib import suppress
from decimal import Decimal
from multiprocessing import get_context
from typing import Optional

import y._db.config as config
from a_sync import a_sync
from brownie import chain
from msgspec import json
from multicall.utils import get_event_loop
from pony.orm import BindingError, OperationalError, commit, db_session, flush

from eth_portfolio._db import entities
from eth_portfolio._db.decorators import (break_locks,
                                          requery_objs_on_diff_tx_err)
from eth_portfolio._db.entities import db
from eth_portfolio.structs import InternalTransfer, TokenTransfer, Transaction

logger = logging.getLogger(__name__)

def __bind():
    try:
        db.bind(**config.connection_settings)
    except BindingError as e:
        if not str(e).startswith('Database object was already bound to'):
            raise e

__bind()

try:
    db.generate_mapping(create_tables=True)
except OperationalError as e:
    if not str(e).startswith("no such column:"):
        raise e
    raise OperationalError("Since eth-portfolio extends the ypricemagic database with additional column definitions, you will need to delete your ypricemagic database at ~/.ypricemagic and rerun this script")

from y._db.decorators import retry_locked
from y._db.entities import Address, Block, Contract, Token, insert
# The db must be bound before we do this since we're adding some new columns to the tables defined in ypricemagic
from y._db.utils import ensure_chain
from y._db.utils.logs import insert_log
from y._db.utils.price import _set_price
from y._db.utils.traces import insert_trace
from y import ERC20
from y.constants import EEE_ADDRESS
from y.exceptions import NonStandardERC20
from y.contracts import is_contract

robust_db_session = lambda callable: retry_locked(break_locks(db_session(callable)))

@a_sync(default='async')
@robust_db_session
def get_block(block: int) -> entities.BlockExtended:
    ensure_chain()
    if b := entities.BlockExtended.get(chain=chain.id, number=block):
        return b
    elif b := Block.get(chain=chain.id, number=block):
        if isinstance(b, entities.BlockExtended):
            # in case of race cndtn
            return b
        raise ValueError(b, b.number, b.chain.id)
        hash = b.hash
        ts = b.timestamp
        prices = [(price.token.address, price.price) for price in b.prices]
        logs = [json.decode(log.raw) for log in b.logs]
        traces = [json.decode(trace.raw) for trace in b.traces]
        for p in b.prices:
            p.delete()
        for l in b.logs:
            l.delete()
        for t in b.traces:
            t.delete()
        flush()
        b.delete()
        commit()
        b = insert(type=BlockExtended, chain=get_chain(sync=True), number=block, hash=hash, timestamp=ts)
        try:
            for log in logs:
                insert_log(log)
            for trace in traces:
                insert_trace(trace)
        except Exception as e:
            raise e.__class__("This is really bad. Might need to nuke your db if you value your logs/traces", *e.args)
        for token, price in prices:
            _set_price(token, price, sync=True)
    elif b := insert(type=entities.BlockExtended, chain=chain.id, number=block):
        return b
    return entities.BlockExtended.get(chain=chain.id, number=block)

# TODO refactor this out, async is annoying sometimes
#process = ProcessPoolExecutor(
#  1, 
#  # NOTE: come on apple, what are you dooooin?
#  mp_context=get_context('fork'),
#)

def is_token(address) -> bool:
    if address == EEE_ADDRESS:
        return False
    #with suppress(NonStandardERC20):
    #    erc = ERC20(address)
    #    if all(erc.symbol, erc.name, erc.total_supply(), erc.scale):
    #    #if all(erc._symbol(), erc._name(), erc.total_supply(), erc._scale()):
    #        return True
    #return False
    return get_event_loop().run_until_complete(_is_token(address))
    
async def _is_token(address) -> bool:
    # just breaking a weird lock, dont mind me
    if retval := await asyncio.get_event_loop().run_in_executor(process, __is_token, address):
        logger.debug("%s is token")
    else:
        logger.debug("%s is not token")
    return retval

def __is_token(address) -> bool:
    with suppress(NonStandardERC20):
        erc = ERC20(address, asynchronous=True)
        if all(get_event_loop().run_until_complete(
            asyncio.gather(erc._symbol(), erc._name(), erc.total_supply_readable())
        )):
            return True
    return False
    

@a_sync(default='async')
@robust_db_session
def get_address(address: str) -> entities.Block:
    ensure_chain()
    
    entity_type = entities.TokenExtended
    entity = entities.Address.get(chain=chain.id, address=address)
    """ TODO: fix this later
    entity = entities.Address.get(chain=chain, address=address)
    if isinstance(entity, (Token, entities.TokenExtended)):
        entity_type = entities.TokenExtended
    elif isinstance(entity, (Contract, entities.ContractExtended)):
        entity_type = entities.ContractExtended
    elif isinstance(entity, (Address, entities.AddressExtended)):
        entity_type = entities.AddressExtended
    elif entity is None:
        # TODO: this logic should live in ypm, prob
        entity_type = entities.AddressExtended if not is_contract(address) else entities.TokenExtended if is_token(address) else entities.ContractExtended
    else:
        raise NotImplementedError(entity, entity_type)
        
    if isinstance(entity, entity_type):
        return entity
    
    elif entity:
        logger.debug("deleting %s", entity)
        entity.delete()
        commit()
    """
    entity = entities.Address.get(chain=chain.id, address=address)
    if entity:
        return entity
    
    return insert(type=entity_type, chain=chain.id, address=address) or entity_type.get(chain=chain.id, address=address)

@a_sync(default='async')
@robust_db_session
def get_token(address: str) -> entities.Block:
    ensure_chain()
    if t := entities.TokenExtended.get(chain=chain.id, address=address):
        return t
    kwargs = {}
    if t := Address.get(chain=chain.id, address=address):
        if isinstance(t, entities.TokenExtended):
            # double check due to possible race cntdn
            return t
        """
        with suppress(TypeError):
            if t.notes:
                kwargs['notes'] = t.notes
        if isinstance(t, Contract):
            with suppress(TypeError):
                if t.deployer:
                    kwargs['deployer'] = t.deployer
            with suppress(TypeError):
                if t.deploy_block:
                    kwargs['deploy_block'] = t.deploy_block
        if isinstance(t, Token):
            with suppress(TypeError):
                if t.symbol:
                    kwargs['symbol'] = t.symbol
            with suppress(TypeError):
                if t.name:
                    kwargs['name'] = t.name
            with suppress(TypeError):
                if t.bucket:
                    kwargs['bucket'] = t.bucket
        """
        
        try:
            flush()
            t.delete()
            commit()
        except KeyError as e:
            raise KeyError(f"cant delete {t}") from e
        
    
    return insert(type=entities.TokenExtended, chain=chain.id, address=address, **kwargs) or entities.TokenExtended.get(chain=chain.id, address=address)
        
    
@a_sync(default='async')
@robust_db_session
def get_transaction(sender: str, nonce: int) -> Optional[Transaction]:
    entity: entities.Transaction
    if entity := entities.Transaction.get(
        from_address = get_address(sender, sync=True),
        nonce = nonce
    ):
        return json.decode(entity.raw, type=Transaction)
    
    
@a_sync(default='async')
@robust_db_session
def delete_transaction(transaction: Transaction) -> None:
    if entity := entities.Transaction.get(
        from_address = get_address(transaction.from_address, sync=True),
        nonce = transaction.nonce,
    ):
        entity.delete()
    
    
@a_sync(default='async')
@requery_objs_on_diff_tx_err
@robust_db_session
def insert_transaction(transaction: Transaction) -> None:
    # Make sure these are in the db so below we can call them and use the results all in one transaction
    block = get_block(transaction.block_number, sync=True)
    from_address = get_address(transaction.from_address, sync=True)
    to_address = get_address(transaction.to_address, sync=True) if transaction.to_address else None
    
    # Now requery and use the values
    entities.Transaction(
        block = get_block(transaction.block_number, sync=True),
        transaction_index = transaction.transaction_index,
        hash = transaction.hash,
        nonce = transaction.nonce,
        from_address = get_address(transaction.from_address, sync=True),
        to_address = get_address(transaction.to_address, sync=True) if transaction.to_address else None,
        value = transaction.value,
        price = transaction.price,
        value_usd = transaction.value_usd,
        type = transaction.type,
        gas = transaction.gas,
        gas_price = transaction.gas_price,
        max_fee_per_gas = transaction.max_fee_per_gas, 
        max_priority_fee_per_gas = transaction.max_priority_fee_per_gas,
        input = transaction.input,
        r = transaction.r,
        s = transaction.s,
        v = transaction.v,
        access_list = json.encode(transaction.access_list) if transaction.access_list else None,
        raw = json.encode(transaction),    
    )
    
    
@a_sync(default='async')
@robust_db_session
def get_internal_transfer(trace: dict) -> Optional[InternalTransfer]:
    
    if entity := entities.InternalTransfer.get(
        block = get_block(trace['blockNumber'], sync=True),
        transaction_index = trace['transactionPosition'],
        hash = trace['transactionHash'],
        type = trace['type'],
        call_type = trace['call_type'],
        from_address = get_address(trace['from'], sync=True),
        to_address = get_address(trace['to'], sync=True),
        value = Decimal(int(trace['value'], 16)) / Decimal(1e18),
        trace_address = get_address(trace['trace_address'], sync=True),
        gas = int(trace['gas'], 16),
        gas_used = int(trace['gas_used'], 16) if 'gas_used' in trace else None,
        input = trace['input'],
        output = trace['output'],
        subtraces = trace['subtraces'],
        address = get_address(trace['address'], sync=True),
    ):
        return json.decode(entity.raw, type=InternalTransfer)
    
@a_sync(default='async')
@robust_db_session
def delete_internal_transfer(transfer: InternalTransfer) -> None:
    if entity := entities.InternalTransfer.get(
        block = get_block(transfer.block_number, sync=True),
        transaction_index = transfer.transaction_index,
        hash = transfer.hash,
        type = transfer.type,
        call_type = transfer.call_type,
        from_address = get_address(transfer.from_address, sync=True),
        to_address = get_address(transfer.to_address, sync=True),
        value = transfer.value,
        trace_address = get_address(transfer.trace_address, sync=True),
        gas = transfer.gas,
        gas_used = transfer.gas_used,
        input = transfer.input,
        output = transfer.output,
        subtraces = transfer.subtraces,
        address = get_address(transfer.address, sync=True),
    ):
        entity.delete()
    
@a_sync(default='async')
@requery_objs_on_diff_tx_err
@robust_db_session
def insert_internal_transfer(transfer: InternalTransfer) -> None:
    entities.InternalTransfer(
        block = get_block(transfer.block_number, sync=True),
        transaction_index = transfer.transaction_index,
        hash = transfer.hash,
        type = transfer.type,
        call_type = transfer.call_type,
        from_address = get_address(transfer.from_address, sync=True),
        to_address = get_address(transfer.to_address, sync=True),
        value = transfer.value,
        price = transfer.price,
        value_usd = transfer.value_usd,
        trace_address = get_address(transfer.trace_address, sync=True),
        gas = transfer.gas,
        gas_used = transfer.gas_used,
        input = transfer.input,
        output = transfer.output,
        subtraces = transfer.subtraces,
        address = get_address(transfer.address, sync=True),
        raw = json.encode(transfer),
    )
    
@a_sync(default='async')
@robust_db_session
def get_token_transfer(transfer_log) -> Optional[TokenTransfer]:
    entity: entities.TokenTransfer
    if entity := entities.TokenTransfer.get(
        block = get_block(transfer_log["blockNumber"], sync=True), 
        transaction_index = transfer_log["transactionIndex"],
        log_index = transfer_log["logIndex"],
    ):
        return json.decode(entity.raw, type=TokenTransfer)
   
    
@a_sync(default='async')
@robust_db_session
def delete_token_transfer(token_transfer: TokenTransfer) -> None:
    if entity := entities.TokenTransfer.get(
        block = get_block(token_transfer.block_number, sync=True), 
        transaction_index = token_transfer.transaction_index,
        log_index = token_transfer.log_index,
    ):
        entity.delete()


@a_sync(default='async')
@requery_objs_on_diff_tx_err
@robust_db_session
def insert_token_transfer(token_transfer: TokenTransfer) -> None:
    # Make sure these are in the db so below we can call them and use the results all in one transaction
    block = get_block(token_transfer.block_number, sync=True)
    token = get_token(token_transfer.token_address, sync=True)
    from_address = get_address(token_transfer.from_address, sync=True)
    to_address = get_address(token_transfer.to_address, sync=True)
    commit()
    
    try:
        # Now requery and use the values
        entities.TokenTransfer(
            block = get_block(token_transfer.block_number, sync=True), 
            transaction_index = token_transfer.transaction_index,
            log_index = token_transfer.log_index,
            hash = token_transfer.hash,
            token = get_token(token_transfer.token_address, sync=True),
            from_address = get_address(token_transfer.from_address, sync=True),
            to_address = get_address(token_transfer.to_address, sync=True),
            value = token_transfer.value,
            price = token_transfer.price,
            value_usd = token_transfer.value_usd,
            raw = json.encode(token_transfer),
        )
        commit()
    except Exception as e:
        if "numeric field overflow" not in str(e):
            raise e
        # NOTE: We can just leave this out of the db for now, figure out how to better handle before we start loading ranges from db
