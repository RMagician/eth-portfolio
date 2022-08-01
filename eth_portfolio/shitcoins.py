
from y import Network, convert

shitcoins = {
    Network.Mainnet: [
        # Tagged as spam on Etherscan
        "0x1e4A0ADFC2e9bf2Dfd041Bc89405538d0D5A077a",
        "0xb07de4b2989E180F8907B8C7e617637C26cE2776",
        "0xa9517B2E61a57350D6555665292dBC632C76adFe",
        "0x6171136E82a2f1bAA2494c69528f599467EfeA20",
        "0xFD1860C9d602236214652a21753731F9acD2C362",
        "0x0Fd23DaB8723b1Fd5e7c3d74Baa624B443423b6B",
        # Tagged as phishing on Etherscan
        "0xCf39B7793512F03f2893C16459fd72E65D2Ed00c",
        "0x89532890c2959e836C1Bca52309356841238b8B7",
        "0xD1B0c350f73E6f7Cd5c9978b82B46a59aE9aD524",
        "0x17a10104CBC1eD155D083eaD9FCF5C3440bb50e8",
        # Generally looks like shit
        "0xdb83eC9EEAC2b3CF8Eb282f91c73C38159578697",
        "0x242a705E8AF8A24B7EB30f3DbAF899eB25E3D76A",
        "0x0795619E02716a81ac9EF6E55363D538DA104e57",
        # Tagged as well known address scam on Etherscan
        "0xEea2fEf22353282fb760d27EA7A1E2f06B3F442d",
        "0x218Ae209BEc57eeFa9149789aE09388459bC91d1",
        "0x4639FFC90b0fD6Dffb57Af712109bfa419afaEB5",
        "0x4a41775Da459B38e641141e4C696DF10EC1f4983",
        "0x72C07D9151DcE2ea862595487ef7e21cC312e564",
    ],
}

SHITCOINS = {chain: [convert.to_address(token) for token in tokens] for chain, tokens in shitcoins.items()}
