
from y import Network, convert

shitcoins = {
    Network.Mainnet: [
        # Tagged as fake on Etherscan
        "0x471c3A7f132bc94938516CB2Bf6f02C7521D2797",
        "0x106EebF11F34ECCcaD59c1CA9398d828765f64f8",
        # Tagged as spam on Etherscan
        "0xAF0b2fBeDd5d1Fda457580FB3DAbAD1F5C8bBC36",
        "0xbadb4170Cd3309680477Fc81D527101cbB4000EE",
        "0x7841479c5976b8184DBcde9a7a5113901b233EfB",
        "0x1e4A0ADFC2e9bf2Dfd041Bc89405538d0D5A077a",
        "0xb07de4b2989E180F8907B8C7e617637C26cE2776",
        "0xa9517B2E61a57350D6555665292dBC632C76adFe",
        "0x6171136E82a2f1bAA2494c69528f599467EfeA20",
        "0x9Ee582c42F88CAA5e7BCDE2e86e69Af3Cf5FCe40",
        "0xFD1860C9d602236214652a21753731F9acD2C362",
        "0x0Fd23DaB8723b1Fd5e7c3d74Baa624B443423b6B",
        "0xe0736F3F455F1DBD29Bf6F8346EAd22f5CF78d08",
        # Tagged as phishing on Etherscan
        "0xb0B1d4732eFE32AEA466ED6BC3c79181eD4810c4",
        "0xCf39B7793512F03f2893C16459fd72E65D2Ed00c",
        "0x89532890c2959e836C1Bca52309356841238b8B7",
        "0xD1B0c350f73E6f7Cd5c9978b82B46a59aE9aD524",
        "0x17a10104CBC1eD155D083eaD9FCF5C3440bb50e8",
        "0x8eB3FecAAA963C86d9b49004d9f28092f1Db3D6c",
        "0xECF0dE4C8498Cfd686E4702D955426b22d812d6B",
        # Generally looks like shit
        "0xdb83eC9EEAC2b3CF8Eb282f91c73C38159578697",
        "0x2F30E0F6B484eF6Be57b6435e34687018ff8Cb4D",
        "0x242a705E8AF8A24B7EB30f3DbAF899eB25E3D76A",
        "0x2f848B4A2B5dfC3b9e4Eb229551c0887E6348653",
        "0x0795619E02716a81ac9EF6E55363D538DA104e57",
        "0x6D9541ba0f1039d0f8636b4f39D20A8a7464f357",
        "0x3654746Ce159BA2FCDF926133D51ecBb85f19288",
        # Tagged as well known address scam on Etherscan
        "0xEea2fEf22353282fb760d27EA7A1E2f06B3F442d",
        "0x218Ae209BEc57eeFa9149789aE09388459bC91d1",
        "0x4639FFC90b0fD6Dffb57Af712109bfa419afaEB5",
        "0x39dDC0a04F0E1F2830f3f1FEc414cD6E23168beE",
        "0x4a41775Da459B38e641141e4C696DF10EC1f4983",
        "0x72C07D9151DcE2ea862595487ef7e21cC312e564",
    ],
}

SHITCOINS = {chain: [convert.to_address(token) for token in tokens] for chain, tokens in shitcoins.items()}
