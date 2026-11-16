import pytest

from app import OrderService


@pytest.fixture
def servico():
    return OrderService()


def test_subtotal_soma_preco_vezes_quantidade(servico):
    assert servico.subtotal([(10.0, 2), (5.5, 1)]) == pytest.approx(25.5)


def test_frete_soma_a_taxa_administrativa(servico):
    assert servico.calculate_shipping(100.0) == pytest.approx(105.5)


def test_frete_de_outro_valor_base(servico):
    assert servico.calculate_shipping(50.0) == pytest.approx(55.5)


def test_total_do_pedido_inclui_o_frete(servico):
    assert servico.total([(20.0, 2), (10.0, 1)]) == pytest.approx(55.5)
