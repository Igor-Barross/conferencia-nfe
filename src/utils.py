from rich import box
from rich.table import Table


def formata_brl(valor: float) -> str:
    """Formata 30224.5 como 'R$ 30.224,50'."""
    texto = f'{valor:,.2f}'.replace(
        ',', 'X').replace('.', ',').replace('X', '.')
    return f'R$ {texto}'


def tabela_resumo(total: int, conciliadas: int, pendentes: int, divergentes: int) -> Table:
    tabela = Table(box=box.ROUNDED, show_header=True, header_style='bold cyan')
    tabela.add_column('Indicador')
    tabela.add_column('Quantidade', justify='right')
    tabela.add_column('%', justify='right')

    def pct(n: int) -> str:
        return f'{n / total:.1%}' if total else '-'

    tabela.add_row('Notas autorizadas analisadas', str(total), '100%')
    tabela.add_row('[green]Conciliadas (deram entrada)[/green]',
                   str(conciliadas), pct(conciliadas))
    tabela.add_row('[yellow]Pendentes de entrada[/yellow]',
                   str(pendentes), pct(pendentes))
    tabela.add_row('[red]Com valor divergente[/red]',
                   str(divergentes), pct(divergentes))
    return tabela


def tabela_pendentes(pendentes) -> Table:
    tabela = Table(
        title='Notas pendentes de entrada',
        box=box.SIMPLE_HEAVY,
        header_style='bold yellow',
    )
    tabela.add_column('Nota', justify='right')
    tabela.add_column('Emissão')
    tabela.add_column('Valor', justify='right')
    tabela.add_column('Chave NF-e', overflow='fold')

    for _, linha in pendentes.iterrows():
        tabela.add_row(
            str(linha['numero_nota']),
            f"{linha['data_emissao']:%d/%m/%Y}",
            formata_brl(linha['valor_total_emitida']),
            str(linha['chave_nf_e']),
        )
    return tabela
