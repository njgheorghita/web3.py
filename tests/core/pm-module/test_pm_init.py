import pytest

from web3.pm import (
    PM,
)


VALID_MANIFEST = {
    'package_name': 'foo',
    'manifest_version': '2',
    'version': '1.0.0',
}


# Returns web3 instance with `pm` module attached
@pytest.fixture
def web3():
    PM.attach(web3, 'pm')
    return web3


def test_pm_get_package_from_manifest(web3):
    pkg = web3.pm.get_package_from_manifest(VALID_MANIFEST)
    assert pkg.name == 'foo'


def test_pm_get_package_from_registry_uri(web3):
    pkg = web3.pm.get_package_from_registry_uri('ercxxx://packages.eth/owned?version=1.0.0', web3)
    assert pkg.name == 'owned'
