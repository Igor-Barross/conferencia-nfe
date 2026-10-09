from pathlib import Path

# Caminhos das pastas do projeto

# -- Raiz do projeto

ROOT = Path(__file__).parents[1]

# --- PASTA DATA
DATA_DIR = ROOT / 'data'

# --- CAMINHO PASTA NOTAS EMITIDAS
DIR_NOTAS_EMITIDAS = DATA_DIR / 'notas-emitidas'
PATH_NOTAS_EMITIDAS_RAW = DIR_NOTAS_EMITIDAS / 'raw'
PATH_NOTAS_EMITIDAS_PROCESSED = DIR_NOTAS_EMITIDAS / 'processed'

# --- CAMINHO ARQUIVO NOTAS EMITIDAS
FILE_NOTAS_EMITIDAS_RAW = PATH_NOTAS_EMITIDAS_RAW / 'notas-fiscais.xlsx'
FILE_NOTAS_EMITIDAS_PROCESSED = PATH_NOTAS_EMITIDAS_PROCESSED / \
    'relatorio-notas-emitidas.xlsx'

# --- CAMINHO PASTA RELATÓRIO DE NOTAS DO SISTEMA DA LOJA
DIR_NOTAS_SISTEMA = DATA_DIR / 'notas-sistema'
PATH_NOTAS_SISTEMA_RAW = DIR_NOTAS_SISTEMA / 'raw'
PATH_NOTAS_SISTEMA_PROCESSED = DIR_NOTAS_SISTEMA / 'processed'

# --- CAMINHO ARQUIVO RELATÓRIO DE NOTAS DO SISTEMA DA LOJA
FILE_NOTAS_SISTEMA_RAW = PATH_NOTAS_SISTEMA_RAW / 'notas-entrada.xls'
FILE_NOTAS_SISTEMA_PROCESSED = PATH_NOTAS_SISTEMA_PROCESSED / \
    'relatorio-notas-sistema.xlsx'

# Pasta e arquivos do resultado final
DIR_RESULTADO = ROOT / 'resultado'
FILE_CONCILIADAS = DIR_RESULTADO / 'notas-conciliadas.xlsx'
FILE_PENDENTES = DIR_RESULTADO / 'notas-pendentes-entrada.xlsx'
FILE_DIVERGENTES = DIR_RESULTADO / 'notas-valor-divergente.xlsx'


# --- CAMINHO PASTA NOTEBOOKS
DIR_NOTEBOOKS = ROOT / 'notebooks'

# --- CAMINHO SRC
DIR_SRC = ROOT / 'src'

if __name__ == '__main__':
    print(ROOT)
    print(DATA_DIR)
    print(DIR_NOTAS_EMITIDAS)
    print(DIR_NOTAS_SISTEMA)
    print(PATH_NOTAS_SISTEMA_RAW)
    print(PATH_NOTAS_SISTEMA_PROCESSED)
    print(DIR_NOTEBOOKS)
    print(DIR_SRC)
