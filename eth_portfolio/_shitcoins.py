
from y import Network, convert

shitcoins = {
    Network.Mainnet: [
        # Tagged as fake on Etherscan
        "0xe397ef3E332256F38983ffaE987158da3e18c5Ec",
        "0x7452E3fC2fE611C6B7761c6c393BECe059881aC7",
        "0x4ab16CDc82a4eA4727Ab40caee1bb46622C13641",
        "0x471c3A7f132bc94938516CB2Bf6f02C7521D2797",
        "0x106EebF11F34ECCcaD59c1CA9398d828765f64f8",
        "0x634a31d5DB29F2a646bADAd27bb7b1E5A78FD316",
        "0xF673623e8507551BDe72290E909c7E184A4799a3",
        "0x269641A320F8465eF4e710F51Dc6e6862D7E8A77",
        "0x956F824B5a37673c6fC4a6904186cB3BA499349B",
        "0xBFA9180729f1c549334080005Ca37093593fB7Aa",
        "0x643695D282f6BA237afe27FFE0Acd89a86b50d3e",
        # Tagged as spam on Etherscan
        "0xdf66B9727553fB9Bfa417699CB8F60425d62d1E3",
        "0x68Ca006dB91312Cd60a2238Ce775bE5F9f738bBa",
        "0xBCCBeDAb3Bf6FA1cfC3e2d07Aa5ce4A282864D6E",
        "0x26004d228fC8A32c5bd1a106108c8647A455B04a",
        "0xf8358bd95dcA48187e3F4BE05847F3593776C086",
        "0x459176FDC68C945B6bb23eB946eee62457041567",
        "0xf55F8aA8F3d777f1aB3A4ae9E269C8D7B73078De",
        "0x434d5875534D19fC7105281Cf61dbfd1C93c8cb1",
        "0x908599FDf490b73D171B57731bd4Ca95b7F0DE6a",
        "0x4709099BE25D156578405132d66aeBfC2e12937A",
        "0x82315517d61ecf47f9A78705127934F3d431cB21",
        "0x2B000332CD291eF558aF76298A4d6F6001E4e015",
        "0x163F4D81d86ac282A0F0F94D9FE3E0321ACcfd37",
        "0x660235331d2FA5FeB7a49F31556B0Be31f02560D",
        "0x696F33F4dd9BE5538483f63308453D2D67D07331",
        "0xcbbadd74b3bb09836d97d91050e13E06089ba485",
        "0xA6D74802a2222d5cCe5eA0531159ed878943b54c",
        "0xcAB80A2bf07BECaF8d48168081352ea873B8Db91",
        "0x72B12aec69dA93357f2B69aCf33d5B75cF17575B",
        "0xA4C8A13FeE3b19718E45d678C071bDE3e33A7302",
        "0x579e4ca5888eD1420492988BF75E26D9e7B4C535",
        "0xB80216D5b4eec2BEc74eF10e5d3814Fec6Fd8af0",
        "0x6A007E207E50B4C6B2ADCFc6a873F6e698645fE3",
        "0x84d12988D71244a8937a9816037BeB3e61E17FdD",
        "0x0734E85525Ca6838fe48EC6EB29b9d457F254F73",
        "0xa10c97bF5629340A35c41a8AA308af0804750605",
        "0x69D732F50e248D4B825d524fEDEB0D7Ce3d76352",
        "0xAF0b2fBeDd5d1Fda457580FB3DAbAD1F5C8bBC36",
        "0xbadb4170Cd3309680477Fc81D527101cbB4000EE",
        "0x7841479c5976b8184DBcde9a7a5113901b233EfB",
        "0x1e4A0ADFC2e9bf2Dfd041Bc89405538d0D5A077a",
        "0xb07de4b2989E180F8907B8C7e617637C26cE2776",
        "0xa9517B2E61a57350D6555665292dBC632C76adFe",
        "0x38715Ab4b9d4e00890773D7338d94778b0dFc0a8",
        "0x6171136E82a2f1bAA2494c69528f599467EfeA20",
        "0x9Ee582c42F88CAA5e7BCDE2e86e69Af3Cf5FCe40",
        "0xFD1860C9d602236214652a21753731F9acD2C362",
        "0x0Fd23DaB8723b1Fd5e7c3d74Baa624B443423b6B",
        "0xe0736F3F455F1DBD29Bf6F8346EAd22f5CF78d08",
        # Tagged as phishing on Etherscan
        "0x0bF377fb3b5F1dD601e693B8fAF6b0bD249f37D3",
        "0xBf5fB1563ef58ba41325454ca61Cc3D62bd40744",
        "0x54fd62228C6e1234fd5Fded28555CA963Dcf6d26",
        "0xA36Ceec605d81aE74268Fda28A5c0Bd10b1D1f7C",
        "0xF9d25EB4C75ed744596392cf89074aFaA43614a8",
        "0x1412ECa9dc7daEf60451e3155bB8Dbf9DA349933",
        "0x120aA018634F555484c088c8da80F75Aa07E004F",
        "0xeDe11D3d5dd7D5454844f6f121cc106bF1144a45",
        "0x875bf9be244970B8572DD042053508bF758371Ee",
        "0x070C0147884D7CF984aFBC2Eb6F3428A39b5E229",
        "0xb0B1d4732eFE32AEA466ED6BC3c79181eD4810c4",
        "0xCf39B7793512F03f2893C16459fd72E65D2Ed00c",
        "0x89532890c2959e836C1Bca52309356841238b8B7",
        "0xD1B0c350f73E6f7Cd5c9978b82B46a59aE9aD524",
        "0x17a10104CBC1eD155D083eaD9FCF5C3440bb50e8",
        "0x8eB3FecAAA963C86d9b49004d9f28092f1Db3D6c",
        "0x52bbca3B24c1c1ac050fF4546F37AA88282aaE22",
        "0xECF0dE4C8498Cfd686E4702D955426b22d812d6B",
        "0xF01f7A348681776c1FC9A066c6973882B693cdC6",
        "0x0e1CD6d2715432e4DBedFE969b0Eb2867FF61d5b",
        # Generally looks like shit
        "0x525fC44CBE181C1108c209091B5EEc5a5028190d",
        "0x7d1a6a4f806A4a64AD32e7F2350E176eA6B9a1F6",
        "0x75E34A4A04d5f5F7Fc01801d2d287d64D882529B",
        "0x8F49cB69ee13974D6396FC26B0c0D78044FCb3A7",
        "0xB688d06d858E092EBB145394a1BA08C7a10E1F56",
        "0x11068577AE36897fFaB0024F010247B9129459E6",
        "0xBA89375bAE9b3DE92442e9C037d4303A6e4FB086",
        "0xcDbd4089C2F98DA715e52127680f87aFdB183A2e",
        "0x3a3a4d2d9755283D9e25105B042C5f45BC0Edf05",
        "0x70c18F2fDcb00d27494f767503874788e35c9940",
        "0xF511123fdf2F13811abf4edDb493860101471729",
        "0x830Cbe766EE470B67F77ea62a56246863F75f376",
        "0xa6DE609807c7258A0D34F5307c1808F062A59794",
        "0x698068C6a369b1BF04D516f5fE48424797973DCf",
        "0xbEb3c5F7f4F8dB708BcfaC4D0fDcDb0bEd285741",
        "0xCdC94877E4164D2e915fC5E8310155D661A995F1",
        "0x5D80A8D8CB80696073e82407968600A37e1dd780",
        "0x19383F024BA4c06e44D11a8B8BB7ebF87faB184C",
        "0xF5b2C59F6DB42FFCdFC1625999C81fDF17953384",
        "0xdb83eC9EEAC2b3CF8Eb282f91c73C38159578697",
        "0x2F30E0F6B484eF6Be57b6435e34687018ff8Cb4D",
        "0x242a705E8AF8A24B7EB30f3DbAF899eB25E3D76A",
        "0x2f848B4A2B5dfC3b9e4Eb229551c0887E6348653",
        "0x0795619E02716a81ac9EF6E55363D538DA104e57",
        "0x6D9541ba0f1039d0f8636b4f39D20A8a7464f357",
        "0x1C3d9Db84e0EEE4744893A7FAeE6187F31E39539",
        "0x3654746Ce159BA2FCDF926133D51ecBb85f19288",
        "0x67542502245eb5DF64eF7Ea776199CeB79401058",
        "0x0951490Cec0261F60Ff0C42DE7F62488Cc8313D8",
        "0xcdBb37f84bf94492b44e26d1F990285401e5423e",
        "0x53d345839E7dF5a6c8Cf590C5c703AE255E44816",
        "0xCCCCee7d9B0f18ab16b217A794D2671549F1A895",
        "0xc6a76f7ad66d0e6Ccd1AaAd6e7568c9bd55Dce62",
        # Tagged as well known address scam on Etherscan
        "0xEea2fEf22353282fb760d27EA7A1E2f06B3F442d",
        "0x218Ae209BEc57eeFa9149789aE09388459bC91d1",
        "0x4639FFC90b0fD6Dffb57Af712109bfa419afaEB5",
        "0x39dDC0a04F0E1F2830f3f1FEc414cD6E23168beE",
        "0x4a41775Da459B38e641141e4C696DF10EC1f4983",
        "0x72C07D9151DcE2ea862595487ef7e21cC312e564",
        "0x7cfa05320D83A20980Ac76B91a3A11981877Ef3A",
        "0x2840a9fC9ad15738c762e404300761eC828aFFCb",
        "0xC1c8c49b0405f6CFfBA5351179bEFB2d8a2c776c",
        "0x6545B409acdD7e1BE14C835B5c3B826C5d312D02",
        "0xdF781bBA6F9EefB1A74bb39f6DF5e282c5976636",
        "0xa51a8578052EdEB4Ced5333A5e058860d9E7a35b",
        "0x7a6b87D7a874Fce4c2d923b09C0E09e4936bcF57",
    ],
}

SHITCOINS = {chain: {convert.to_address(token) for token in tokens} for chain, tokens in shitcoins.items()}
