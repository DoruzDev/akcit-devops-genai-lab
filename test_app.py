import importlib

import pytest

import app
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


@pytest.fixture
def recarregar_app(monkeypatch):
    """Recarrega app.py com o ambiente do teste e restaura o padrão no fim."""
    yield lambda: importlib.reload(app)
    monkeypatch.delenv("TAXA_ADMINISTRATIVA", raising=False)
    importlib.reload(app)


def test_taxa_administrativa_vem_do_ambiente(monkeypatch, recarregar_app):
    monkeypatch.setenv("TAXA_ADMINISTRATIVA", "7.25")

    modulo = recarregar_app()

    assert modulo.OrderService().calculate_shipping(100.0) == pytest.approx(107.25)


def test_taxa_invalida_no_ambiente_impede_a_carga(monkeypatch, recarregar_app):
    monkeypatch.setenv("TAXA_ADMINISTRATIVA", "5,50")

    with pytest.raises(ValueError):
        recarregar_app()
