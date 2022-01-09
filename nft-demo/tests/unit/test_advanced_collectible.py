from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    FORKED_LOCAL_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import network, AdvancedCollectible
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_advanced_collectible():
    # Arrange
    if network.show_active() not in (
        LOCAL_BLOCKCHAIN_ENVIRONMENTS or FORKED_LOCAL_ENVIRONMENTS
    ):
        pytest.skip("Only for local testing")
    # Act
    advanced_collectible, creation_transaction = deploy_and_create()
    requestId = creation_transaction.events["requestedCollectible"]["requestId"]
    rnd_nr = 777
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, rnd_nr, advanced_collectible.address, {"from": get_account()}
    )
    # Assert
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToCamPos(0) == rnd_nr % 3
