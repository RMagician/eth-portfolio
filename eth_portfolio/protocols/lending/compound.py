
import asyncio
from typing import List, Optional

import a_sync
from async_lru import alru_cache
from brownie import ZERO_ADDRESS, Contract
from y import ERC20, Contract, get_prices, weth
from y.datatypes import Block
from y.decorators import stuck_coro_debugger
from y.exceptions import ContractNotVerified
from y.prices.lending.compound import CToken, compound

from eth_portfolio.protocols.lending._base import LendingProtocol
from eth_portfolio.typing import Address, Balance, TokenBalances
from eth_portfolio.utils import Decimal


def _get_contract(market: CToken) -> Optional[Contract]:
    try:
        return market.contract
    except ContractNotVerified:
        # We will skip these for now. Might consider supporting them later if necessary.
        return None

class Compound(LendingProtocol):
    @a_sync.future
    @alru_cache(ttl=300)
    @stuck_coro_debugger
    async def underlyings(self) -> List[ERC20]:
        markets = await asyncio.gather(*[comp.markets for comp in compound.trollers.values()])
        markets = [market.contract for troller in markets for market in troller if hasattr(_get_contract(market), 'borrowBalanceStored')] # this last part takes out xinv
        gas_token_markets = [market for market in markets if not hasattr(market,'underlying')]
        other_markets = [market for market in markets if hasattr(market,'underlying')]

        markets = gas_token_markets + other_markets
        underlyings = [weth for market in gas_token_markets] + await asyncio.gather(*[market.underlying.coroutine() for market in other_markets])

        markets_zip = zip(markets,underlyings)
        self._markets, underlyings = [], []
        for contract, underlying in markets_zip:
            if underlying != ZERO_ADDRESS:
                self._markets.append(contract)
                underlyings.append(underlying)
        return [ERC20(underlying, asynchronous=True) for underlying in underlyings]

    @a_sync.future
    @stuck_coro_debugger
    async def markets(self):
        await self.underlyings()
        return self._markets
    
    async def _debt(self, address: Address, block: Optional[Block] = None) -> TokenBalances:
        if len(compound.trollers) == 0: # if ypricemagic doesn't support any Compound forks on current chain
            return TokenBalances()

        address = str(address)
        markets, underlyings = await asyncio.gather(*[self.markets(), self.underlyings()])
        debt_data, underlying_scale = await asyncio.gather(
            asyncio.gather(*[_borrow_balance_stored(market, address, block) for market in markets]),
            asyncio.gather(*[underlying.__scale__(sync=False) for underlying in underlyings]),
        )

        debts = {underlying: Decimal(debt) / scale for underlying, scale, debt in zip(underlyings, underlying_scale, debt_data) if debt}
        prices = await get_prices(debts.keys(), block=block, sync=False)
        balances: TokenBalances = TokenBalances()
        for (underlying, debt), price in zip(debts.items(), prices):
            balances[underlying] += Balance(debt, debt * Decimal(price))
        return balances

@stuck_coro_debugger
async def _borrow_balance_stored(market: Contract, address: Address, block: Optional[Block] = None) -> Optional[int]:
    try:
        return await market.borrowBalanceStored.coroutine(str(address), block_identifier=block)
    except ValueError as e:
        if str(e) != "No data was returned - the call likely reverted":
            raise
        return None
