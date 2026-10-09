import pytest

from utils import formata_brl


@pytest.mark.parametrize(
    'valor, esperado',
    [
        (30224.0, 'R$ 30.224,00'),
        (30224.5, 'R$ 30.224,50'),
        (241.73, 'R$ 241,73'),
        (0, 'R$ 0,00'),
        (1234567.89, 'R$ 1.234.567,89'),
    ],
)
def test_formata_brl(valor, esperado):
    assert formata_brl(valor) == esperado
