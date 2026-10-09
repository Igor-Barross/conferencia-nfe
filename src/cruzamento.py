import pandas as pd

CHAVE = ['numero_nota', 'data_emissao']
TOLERANCIA_VALOR = 0.01  # R$ 0,01


def _converte_valor(df: pd.DataFrame, nome: str) -> pd.DataFrame:
    """Converte 'valor_total' para número e falha se algum valor se perder."""
    df = df.copy()
    nulos_antes = df['valor_total'].isna().sum()
    df['valor_total'] = pd.to_numeric(df['valor_total'], errors='coerce')
    perdidos = df['valor_total'].isna().sum() - nulos_antes
    if perdidos:
        raise ValueError(
            f'{nome}: {perdidos} valor(es) de "valor_total" não puderam ser '
            'convertidos em número. Confira o formato (por exemplo 1.234,56).')
    return df


def cruza_notas(df_emitidas: pd.DataFrame, df_loja: pd.DataFrame) -> pd.DataFrame:
    """Cruza as notas emitidas (autorizadas) com as notas lançadas no sistema.

    Retorna as emitidas com as colunas da loja, a coluna '_merge'
    ('both' = deu entrada, 'left_only' = pendente) e a checagem de valor.
    """
    emitidas = df_emitidas.copy()
    loja = df_loja.copy()

    # Mesmo tipo da chave nos dois lados
    for df in (emitidas, loja):
        df['numero_nota'] = pd.to_numeric(
            df['numero_nota'], errors='coerce').astype('Int64')

    # Garante valor numérico nos dois lados (texto não pode ser subtraído)
    emitidas = _converte_valor(emitidas, 'emitidas')
    loja = _converte_valor(loja, 'loja')

    # Só notas autorizadas precisam de entrada
    emitidas = emitidas[emitidas['indicadores_selecionados'] == 'AUTORIZADA']

    # Descarta linhas sem chave
    emitidas = emitidas.dropna(subset=CHAVE)
    loja = loja.dropna(subset=CHAVE)

    colunas_loja = CHAVE + ['data_entrada', 'valor_total', 'tipo']

    resultado = pd.merge(
        emitidas,
        loja[colunas_loja],
        how='left',
        on=CHAVE,
        suffixes=('_emitida', '_loja'),
        indicator=True,
        validate='1:1',  # acusa duplicidade na chave
    )

    # Conferência de valores (só faz sentido nas conciliadas)
    resultado['diferenca_valor'] = (
        resultado['valor_total_emitida'] - resultado['valor_total_loja']
    )
    resultado['valor_divergente'] = (
        resultado['diferenca_valor'].abs() > TOLERANCIA_VALOR
    )

    return resultado
