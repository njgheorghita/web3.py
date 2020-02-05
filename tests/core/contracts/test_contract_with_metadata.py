from web3.contract import Contract
import json
from ethpm import ASSETS_DIR, Package
from web3.auto.infura import w3

# todo compiler
def xtest_contract_instance_displays_metadata():
    package_with_metadata = json.loads((ASSETS_DIR / 'escrow' / '1.0.0-pretty.json').read_text())
    pkg = Package(package_with_metadata, w3)
    escrow_data = pkg.manifest['contract_types']['Escrow']
    safe_send_lib_data = pkg.manifest['contract_types']['SafeSendLib']
    escrow_contract = w3.eth.contract(
        abi=escrow_data['abi'],
        natspec=escrow_data['natspec'],
    )
    safe_send_lib_contract = w3.eth.contract(
        abi=safe_send_lib_data['abi'],
        natspec=safe_send_lib_data['natspec'],
    )
    assert escrow_contract.abi == escrow_data['abi']
    assert escrow_contract.natspec == escrow_data['natspec']
    assert escrow_contract.describe() == (
        "Title: Contract for holding funds in escrow between two semi trusted parties.",
        "Author: Piper Merriam <pipermerriam@gmail.com>",
    )
    assert safe_send_lib_contract.abi == safe_send_lib_data['abi']
    assert safe_send_lib_contract.natspec == safe_send_lib_data['natspec']
    assert safe_send_lib_contract.describe() == (
        "Title: Library for safe sending of ether.",
        "Author: Piper Merriam <pipermerriam@gmail.com>",
    )

ABI = [
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "uint256",
				"name": "rings",
				"type": "uint256"
			}
		],
		"name": "age",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "pure",
		"type": "function"
	}
]

DEVDOC = {
	"author": "Larry A. Gardner",
	"details": "All function calls are currently implemented without side effects",
	"methods": {
		"age(uint256)": {
			"author": "Mary A. Botanist",
			"details": "The Alexandr N. Tetearing algorithm could increase precision",
			"params": {
				"rings": "The number of rings from dendrochronological sample"
			},
			"return": "age in years, rounded up for partial years"
		}
	},
	"title": "A simulator for trees"
}

USERDOC = {
    "methods": {
	"age(uint256)": {
	    "notice": "Calculate tree age in ${age} years, rounded up, for live trees"
	},
        "addr(bytes32)": {
            "notice": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        }
    },
    "notice": "You can use this contract for only the most basic simulation"
}

def test_contract_instance_displays_metadata(web3):
    natspec = {**DEVDOC, **USERDOC}
    # test with instance also
    natspec_contract = web3.eth.contract(
        abi=ABI,
        natspec=natspec,
    )
    assert natspec_contract.natspec == natspec
    description = natspec_contract.describe()
    expected = (
        'Title: A simulator for trees',
        'Details: You can use this contract for only the most basic simulation',
        "age(uint256): Calculate tree age in ${age} years, rounded up, for live trees",
        "addr(bytes32): xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    )
    assert description == expected
