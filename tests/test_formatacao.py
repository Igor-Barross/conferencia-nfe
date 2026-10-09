import pandas as pd
import pytest

from formatacao_arquivo import (
    corrige_tipo_dados_relatorio_emitidas,
    corrige_tipo_dados_relatorio_loja,
)


def df_loja(**colunas):
    base = {
        'numero_nota': ['19439'],
        'data_emissao': ['04/09/2026'],
        'data_entrada': ['08/09/2026'],
        'valor_total': ['33.720,00'],
    }
    base.update(colunas)
    return pd.DataFrame(base)


# --- Valor total (relatório da loja, formato brasileiro) -------------------

@pytest.mark.parametrize(
    'bruto, esperado',
    [
        ('33.720,00', 33720.0),
        ('1.102,73', 1102.73),
        ('241,73', 241.73),
        ('42,75', 42.75),
        ('820,00', 820.0),
        ('R$ 820,00', 820.0),
    ],
)
def test_valor_loja_formato_brasileiro(bruto, esperado):
    resultado = corrige_tipo_dados_relatorio_loja(df_loja(valor_total=[bruto]))

    assert resultado['valor_total'].iloc[0] == pytest.approx(esperado)


def test_valor_loja_vazio_vira_nulo():
    resultado = corrige_tipo_dados_relatorio_loja(df_loja(valor_total=[None]))

    assert pd.isna(resultado['valor_total'].iloc[0])


# --- Número da nota ---------------------------------------------------------

def test_numero_nota_vira_inteiro():
    resultado = corrige_tipo_dados_relatorio_loja(
        df_loja(numero_nota=['19439']))

    assert resultado['numero_nota'].iloc[0] == 19439
    assert str(resultado['numero_nota'].dtype) == 'Int64'


def test_numero_nota_com_texto_antes_do_numero():
    resultado = corrige_tipo_dados_relatorio_loja(
        df_loja(numero_nota=['NF 19439']))

    assert resultado['numero_nota'].iloc[0] == 19439


# --- Datas ------------------------------------------------------------------

def test_datas_da_loja_viram_datetime():
    resultado = corrige_tipo_dados_relatorio_loja(df_loja())

    assert resultado['data_emissao'].iloc[0] == pd.Timestamp('2026-09-04')
    assert resultado['data_entrada'].iloc[0] == pd.Timestamp('2026-09-08')


def test_data_invalida_vira_nat():
    resultado = corrige_tipo_dados_relatorio_loja(
        df_loja(data_emissao=['31/02/2026']))

    assert pd.isna(resultado['data_emissao'].iloc[0])


def test_data_primeiro_o_dia_depois_o_mes():
    # 01/10 deve ser 1º de outubro, e não 10 de janeiro
    resultado = corrige_tipo_dados_relatorio_loja(
        df_loja(data_emissao=['01/10/2026']))

    assert resultado['data_emissao'].iloc[0] == pd.Timestamp('2026-10-01')


# --- Relatório de notas emitidas -------------------------------------------

def test_emitidas_converte_data_e_valor():
    df = pd.DataFrame({
        'numero_nota': ['19944'],
        'data_emissao': ['29/09/2026'],
        'valor_total': ['19782'],
    })

    resultado = corrige_tipo_dados_relatorio_emitidas(df)

    assert resultado['data_emissao'].iloc[0] == pd.Timestamp('2026-09-29')
    assert resultado['valor_total'].iloc[0] == pytest.approx(19782.0)


def test_emitidas_valor_com_decimal():
    df = pd.DataFrame({
        'numero_nota': ['3405'],
        'data_emissao': ['05/09/2026'],
        'valor_total': ['1102.73'],
    })

    resultado = corrige_tipo_dados_relatorio_emitidas(df)

    assert resultado['valor_total'].iloc[0] == pytest.approx(1102.73)


def test_funcoes_nao_alteram_o_dataframe_original():
    df = df_loja()
    copia = df.copy()

    corrige_tipo_dados_relatorio_loja(df)

    pd.testing.assert_frame_equal(df, copia)
