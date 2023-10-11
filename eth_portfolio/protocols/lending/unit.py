
from typing import Optional

from brownie import chain
from y import Contract, Network, get_price
from y.datatypes import Address, Block
from y.decorators import stuck_coro_debugger

from eth_portfolio.protocols.lending._base import \
    LendingProtocolWithLockedCollateral
from eth_portfolio.typing import Balance, TokenBalances

# NOTE: This only works for YFI collateral, must extend before using for other collaterals
yfi = "0x0bc529c00C6401aEF6D220BE8C6Ea1667F6Ad93e"
usdp = '0x1456688345527bE1f37E9e627DA0837D6f08C925'

class UnitXyz(LendingProtocolWithLockedCollateral):
    networks = [Network.Mainnet]
    
    def __init__(self) -> None:
        self.unitVault = Contract("0xb1cff81b9305166ff1efc49a129ad2afcd7bcf19")
        self.start_block = 11315910
    
    @stuck_coro_debugger
    async def _balances(self, address: Address, block: Optional[Block] = None) -> TokenBalances:
        balances: TokenBalances = TokenBalances()
        if block and block < self.start_block:
            return balances
        bal = await self.unitVault.collaterals.coroutine(yfi, address, block_identifier=block)
        if bal:
            bal /= 1e18
            balances[yfi] = Balance(bal, bal * await get_price(yfi, block, sync=False))
        return balances

    @stuck_coro_debugger
    async def _debt(self, address: Address, block: Optional[Block] = None) -> TokenBalances:
        balances: TokenBalances = TokenBalances()
        if block and block < self.start_block:
            return balances
        # NOTE: This only works for YFI based debt, must extend before using for other collaterals
        debt = await self.unitVault.getTotalDebt.coroutine(yfi, address, block_identifier=block) / 1e18
        if debt:
            balances[usdp] = Balance(debt, debt)
        return balances
