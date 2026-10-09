from pathlib import Path

import pandas as pd

from config import (
    FILE_NOTAS_EMITIDAS_PROCESSED,
    FILE_NOTAS_EMITIDAS_RAW,
    FILE_NOTAS_SISTEMA_PROCESSED,
    FILE_NOTAS_SISTEMA_RAW,
)


def formata_relatorio_sistema_loja(caminho: Path) -> pd.DataFrame:

    # Pula o cabeçalho e o rodapé, seleciona apenas as colunas necessárias
    df = pd.read_excel(caminho, engine="xlrd", skiprows=5,
                       skipfooter=1, usecols=[1, 5, 6, 7, 14])

    df.dropna(inplace=True)  # Remove linhas com valores nulos

    df.columns = [
        'numero_nota', 'tipo', 'data_emissao', 'data_entrada', 'valor_total'
    ]

    return df


def formata_relatorio_notas_emitidas(caminho: Path) -> pd.DataFrame:
    # dtype=str na planilha toda: não depende do nome original da coluna
    df = pd.read_excel(caminho, engine='openpyxl', dtype=str)
    df.columns = [
        'cnpj_cpf_remetente', 'razao_social_emitente', 'uf', 'numero_nota',
        'data_emissao', 'indicadores_selecionados', 'valor_total', 'chave_nf_e',
    ]
    return df


def corrige_tipo_dados_relatorio_loja(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Retira caracteres desnecessários e converte para inteiro
    df['numero_nota'] = pd.to_numeric(
        df['numero_nota'].astype('string').str.extract(r"(\d+)\s*$")[0],
        errors='coerce',
    ).astype('Int64')

    # Converte o tipo de dados da coluna 'Data-Emissao' para datetime
    df['data_emissao'] = pd.to_datetime(
        df['data_emissao'], errors='coerce', format='%d/%m/%Y').dt.normalize()

    # Converte o tipo de dados da coluna 'Data-Entrada para datetime
    df['data_entrada'] = pd.to_datetime(
        df['data_entrada'], errors='coerce', format='%d/%m/%Y').dt.normalize()

    # Converte o tipo de dados da coluna 'Valor-Total' para float, removendo caracteres não numéricos
    df['valor_total'] = pd.to_numeric(
        df['valor_total']
        .astype('string')
        .str.replace(r'[^\d,.\-]', '', regex=True)   # tira "R$", espaços, etc.
        .str.replace('.', '', regex=False)           # remove o ponto de milhar
        # vírgula decimal vira ponto
        .str.replace(',', '.', regex=False),
        errors='coerce',
    )

    # Orderna por data de emissão e reseta o índice
    df = df.sort_values(['data_emissao', 'numero_nota']).reset_index(drop=True)
    return df


def corrige_tipo_dados_relatorio_emitidas(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    df['data_emissao'] = pd.to_datetime(
        df['data_emissao'], errors='coerce', format='%d/%m/%Y').dt.normalize()

    df['numero_nota'] = pd.to_numeric(
        df['numero_nota'], errors='coerce').astype('Int64')

    df['valor_total'] = pd.to_numeric(df['valor_total'], errors='coerce')

    # Ordena por data de emissão e reseta o índice
    df = df.sort_values(['data_emissao', 'numero_nota']).reset_index(drop=True)
    return df


def salva_excel(df: pd.DataFrame, caminho: Path) -> None:
    # garante que a pasta existe
    caminho.parent.mkdir(parents=True, exist_ok=True)
    df.to_excel(caminho, index=False, engine='openpyxl')
    print(f'Arquivo salvo em: {caminho}')


if __name__ == '__main__':
    print('Processando relatório do sistema da loja...')
    df_loja = formata_relatorio_sistema_loja(FILE_NOTAS_SISTEMA_RAW)
    df_loja = corrige_tipo_dados_relatorio_loja(df_loja)
    salva_excel(df_loja, FILE_NOTAS_SISTEMA_PROCESSED)

    print('Processando relatório de notas emitidas...')
    df_emitidas = formata_relatorio_notas_emitidas(FILE_NOTAS_EMITIDAS_RAW)
    df_emitidas = corrige_tipo_dados_relatorio_emitidas(df_emitidas)
    salva_excel(df_emitidas, FILE_NOTAS_EMITIDAS_PROCESSED)
