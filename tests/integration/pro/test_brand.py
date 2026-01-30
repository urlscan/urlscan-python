import pytest

from urlscan import Pro


@pytest.mark.integration
def test_get_available_brands(pro: Pro):
    brands = pro.brand.get_available_brands()
    assert isinstance(brands, dict)
    assert "kits" in brands
    assert len(brands["kits"]) > 0


@pytest.mark.integration
def test_get_brands(pro: Pro):
    brands = pro.brand.get_brands()
    assert isinstance(brands, dict)
    assert "responses" in brands
    assert len(brands["responses"]) > 0
