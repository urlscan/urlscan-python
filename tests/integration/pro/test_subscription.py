import pytest

from urlscan import Pro


@pytest.mark.integration
def test_subscription_crud(pro: Pro):
    # First, create a saved search to use for the subscription
    search_result = pro.saved_search.create(
        datasource="scans",
        query="page.domain:example.com",
        name="integration-test-subscription",
    )
    search_id = search_result["search"]["_id"]

    try:
        # Create a subscription
        created = pro.subscription.create(
            search_ids=[search_id],
            frequency="daily",
            name="integration-test",
            email_addresses=["test@example.com"],
            is_active=True,
            ignore_time=False,
        )
        subscription_id = created["subscription"]["_id"]

        try:
            # Update the subscription
            updated = pro.subscription.update(
                subscription_id=subscription_id,
                search_ids=[search_id],
                frequency="hourly",
                name="integration-test-updated",
                email_addresses=["test@example.com"],
                is_active=True,
                ignore_time=False,
            )
            assert updated is not None

        finally:
            # Delete the subscription
            pro.subscription.delete_subscription(subscription_id=subscription_id)

    finally:
        # Clean up the saved search
        pro.saved_search.remove(search_id)


@pytest.mark.integration
def test_subscription_list(pro: Pro):
    result = pro.subscription.get_subscriptions()
    assert isinstance(result, dict)
    assert "subscriptions" in result
    assert len(result["subscriptions"]) > 0
