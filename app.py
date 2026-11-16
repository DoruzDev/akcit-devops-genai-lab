"""Serviço de pedidos usado no miniprojeto de DevOps com IA generativa."""

# Taxa administrativa somada a todo frete, em reais.
TAXA_ADMINISTRATIVA = 5.50


class OrderService:
    def subtotal(self, itens):
        """Soma preço x quantidade de cada item."""
        return round(sum(preco * quantidade for preco, quantidade in itens), 2)

    def calculate_shipping(self, base_price, tax_rate=TAXA_ADMINISTRATIVA):
        """Frete total: valor base mais a taxa administrativa."""
        return round(base_price + tax_rate, 2)

    def total(self, itens):
        """Total do pedido: subtotal dos itens mais o frete."""
        return self.calculate_shipping(self.subtotal(itens))
