import pandas as pd
import pytest

from cruzamento import cruza_notas


def emitidas(linhas):
    """Monta o DataFrame de notas emitidas a partir de (numero, data, status, valor)."""
    return pd.DataFrame(
        [
            {
                'numero_nota': numero,
                'data_emissao': pd.Timestamp(data),
                'indicadores_selecionados': status,
                'valor_total': valor,
            }
            for numero, data, status, valor in linhas
        ]
    )


def loja(linhas):
    """Monta o DataFrame do sistema da loja a partir de (numero, data, valor)."""
    return pd.DataFrame(
        [
            {
                'numero_nota': numero,
                'data_emissao': pd.Timestamp(data),
                'data_entrada': pd.Timestamp(data) + pd.Timedelta(days=1),
                'valor_total': valor,
                'tipo': 'NFE',
            }
            for numero, data, valor in linhas
        ]
    )


def prepara(df_emitidas, df_loja):
    """Renomeia o valor das emitidas como o cruzamento espera ao final."""
    return cruza_notas(df_emitidas, df_loja)


def test_nota_com_entrada_e_classificada_como_both():
    e = emitidas([(100, '2026-09-01', 'AUTORIZADA', 500.0)])
    l = loja([(100, '2026-09-01', 500.0)])

    resultado = prepara(e, l)

    assert resultado['_merge'].tolist() == ['both']


def test_nota_sem_entrada_e_classificada_como_left_only():
    e = emitidas([(100, '2026-09-01', 'AUTORIZADA', 500.0)])
    l = loja([(999, '2026-09-01', 500.0)])

    resultado = prepara(e, l)

    assert resultado['_merge'].tolist() == ['left_only']


def test_nota_cancelada_e_ignorada():
    e = emitidas([
        (100, '2026-09-01', 'AUTORIZADA', 500.0),
        (101, '2026-09-01', 'CANCELADA', 300.0),
    ])
    l = loja([(100, '2026-09-01', 500.0)])

    resultado = prepara(e, l)

    assert resultado['numero_nota'].tolist() == [100]


def test_mesmo_numero_com_data_diferente_nao_casa():
    e = emitidas([(100, '2026-09-01', 'AUTORIZADA', 500.0)])
    l = loja([(100, '2026-08-01', 500.0)])

    resultado = prepara(e, l)

    assert resultado['_merge'].tolist() == ['left_only']


def test_numero_nota_como_texto_e_convertido():
    e = emitidas([('100', '2026-09-01', 'AUTORIZADA', 500.0)])
    l = loja([(100, '2026-09-01', 500.0)])

    resultado = prepara(e, l)

    assert resultado['_merge'].tolist() == ['both']


def test_diferenca_de_um_centavo_nao_e_divergencia():
    e = emitidas([(100, '2026-09-01', 'AUTORIZADA', 500.00)])
    l = loja([(100, '2026-09-01', 500.01)])

    resultado = prepara(e, l)

    assert not resultado['valor_divergente'].iloc[0]


def test_diferenca_maior_que_tolerancia_e_divergencia():
    e = emitidas([(100, '2026-09-01', 'AUTORIZADA', 500.00)])
    l = loja([(100, '2026-09-01', 500.50)])

    resultado = prepara(e, l)

    assert resultado['valor_divergente'].iloc[0]
    assert resultado['diferenca_valor'].iloc[0] == pytest.approx(-0.50)


def test_nota_pendente_nao_e_marcada_como_divergente():
    e = emitidas([(100, '2026-09-01', 'AUTORIZADA', 500.0)])
    l = loja([(999, '2026-09-01', 500.0)])

    resultado = prepara(e, l)

    assert not resultado['valor_divergente'].iloc[0]


def test_duplicidade_na_loja_levanta_erro():
    e = emitidas([(100, '2026-09-01', 'AUTORIZADA', 500.0)])
    l = loja([
        (100, '2026-09-01', 500.0),
        (100, '2026-09-01', 500.0),
    ])

    with pytest.raises(pd.errors.MergeError):
        prepara(e, l)


def test_linhas_sem_chave_sao_descartadas():
    e = emitidas([
        (100, '2026-09-01', 'AUTORIZADA', 500.0),
        (None, '2026-09-02', 'AUTORIZADA', 700.0),
    ])
    l = loja([(100, '2026-09-01', 500.0)])

    resultado = prepara(e, l)

    assert len(resultado) == 1


def test_valor_em_texto_nos_dois_lados_e_convertido():
    e = emitidas([(100, '2026-09-01', 'AUTORIZADA', '500.00')])
    e['valor_total'] = e['valor_total'].astype('string')
    l = loja([(100, '2026-09-01', '500.00')])
    l['valor_total'] = l['valor_total'].astype('string')

    resultado = prepara(e, l)

    assert resultado['_merge'].tolist() == ['both']
    assert not resultado['valor_divergente'].iloc[0]


def test_valor_que_nao_converte_levanta_erro_claro():
    e = emitidas([(100, '2026-09-01', 'AUTORIZADA', '1.234,56')])
    l = loja([(100, '2026-09-01', 1234.56)])

    with pytest.raises(ValueError, match='valor_total'):
        prepara(e, l)
