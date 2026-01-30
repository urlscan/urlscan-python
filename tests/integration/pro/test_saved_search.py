import pytest

from urlscan import Pro


@pytest.mark.integration
def test_saved_search_crud(pro: Pro):
    # Create a saved search
    created = pro.saved_search.create(
        datasource="scans",
        query="page.domain:example.com",
        name="integration-test",
    )
    search_id = created["search"]["_id"]

    try:
        # Get the saved search results
        results = pro.saved_search.get_results(search_id)
        assert results is not None

        # Update the saved search
        updated = pro.saved_search.update(
            search_id,
            datasource="scans",
            query="page.domain:example.net",
            name="integration-test-updated",
        )
        assert updated is not None

    finally:
        # Delete the saved search
        pro.saved_search.remove(search_id)


@pytest.mark.integration
def test_saved_search_list(pro: Pro):
    result = pro.saved_search.get_list()
    assert isinstance(result, dict)
    assert "searches" in result
    assert len(result["searches"]) > 0
