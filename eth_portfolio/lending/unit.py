
from typing import Dict, Optional

from brownie import chain
from eth_portfolio.lending.base import LendingProtocolWithLockedCollateral
from eth_portfolio.typing import PortfolioBalanceDetails
from multicall.utils import await_awaitable
from y import Contract, Network, get_price_async
from y.datatypes import Address, Block

# NOTE: This only works for YFI collateral, must extend before using for other collaterals
yfi = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
usdp = '0x1456688345527bE1f37E9e627DA0837D6f08C925'

class UnitXyz(LendingProtocolWithLockedCollateral):
    def __init__(self, asynchronous: bool = False) -> None:
        self.asynchronous = bool(asynchronous)
        self.unitVault = Contract("0xb1cff81b9305166ff1efc49a129ad2afcd7bcf19")
        self.start_block = 11315910
    
    def collateral(self, address: Address, block: Optional[Block] = None) -> Dict:
        coro = self.collateral_async(address, block)
        if self.asynchronous:
            return coro
        return await_awaitable(coro)
    
    async def collateral_async(self, address: Address, block: Optional[Block] = None) -> Dict:
        if block and block < self.start_block:
            return None
        
        bal = await self.unitVault.collaterals.coroutine(yfi, address, block_identifier=block)
        if bal:
            return {
                yfi: {
                    'balance': bal / 1e18,
                    'usd value': bal / 1e18 * await get_price_async(yfi, block),
                }
            }

    def debt(self, address: Address, block: Optional[Block] = None) -> Dict:
        coro = self.debt_async(address, block)
        if self.asynchronous:
            return coro
        return await_awaitable(coro)
    
    async def debt_async(self, address: Address, block: Optional[Block] = None) -> Optional[PortfolioBalanceDetails]:
        if block and block < self.start_block:
            return None
        # NOTE: This only works for YFI based debt, must extend before using for other collaterals
        debt = await self.unitVault.getTotalDebt.coroutine(yfi, address, block_identifier=block) / 1e18
        if debt:
            return {usdp: {'balance': debt, 'usd value': debt}}

unit = UnitXyz(asynchronous=True) if chain.id == Network.Mainnet else None
