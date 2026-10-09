from rich.console import Console
from rich.panel import Panel
from rich.rule import Rule

from config import (
    FILE_CONCILIADAS,
    FILE_DIVERGENTES,
    FILE_NOTAS_EMITIDAS_PROCESSED,
    FILE_NOTAS_EMITIDAS_RAW,
    FILE_NOTAS_SISTEMA_PROCESSED,
    FILE_NOTAS_SISTEMA_RAW,
    FILE_PENDENTES,
)
from cruzamento import cruza_notas
from formatacao_arquivo import (
    corrige_tipo_dados_relatorio_emitidas,
    corrige_tipo_dados_relatorio_loja,
    formata_relatorio_notas_emitidas,
    formata_relatorio_sistema_loja,
    salva_excel,
)
from utils import tabela_pendentes, tabela_resumo

console = Console()


def main() -> None:
    console.print(Panel.fit(
        '[bold]CONCILIAÇÃO DE NOTAS FISCAIS[/bold]\n'
        '[dim]Notas emitidas x Entrada no sistema da loja[/dim]',
        border_style='cyan',
        padding=(1, 4),
    ))

    # --- Relatório do sistema da loja
    console.print(
        Rule('[bold]1. Relatório do sistema da loja[/bold]', style='cyan'))
    with console.status('Padronizando dados...'):
        df_loja = formata_relatorio_sistema_loja(FILE_NOTAS_SISTEMA_RAW)
        df_loja = corrige_tipo_dados_relatorio_loja(df_loja)
        salva_excel(df_loja, FILE_NOTAS_SISTEMA_PROCESSED)
    console.print(f'[green]✔[/green] {len(df_loja)} notas processadas')

    # --- Relatório de notas emitidas
    console.print(
        Rule('[bold]2. Relatório de notas emitidas[/bold]', style='cyan'))
    with console.status('Padronizando dados...'):
        df_emitidas = formata_relatorio_notas_emitidas(FILE_NOTAS_EMITIDAS_RAW)
        df_emitidas = corrige_tipo_dados_relatorio_emitidas(df_emitidas)
        salva_excel(df_emitidas, FILE_NOTAS_EMITIDAS_PROCESSED)
    console.print(f'[green]✔[/green] {len(df_emitidas)} notas processadas')

    # --- Cruzamento
    console.print(Rule('[bold]3. Cruzamento dos dados[/bold]', style='cyan'))
    with console.status('Cruzando as tabelas...'):
        resultado = cruza_notas(df_emitidas, df_loja)

    conciliadas = resultado[resultado['_merge'] == 'both']
    pendentes = resultado[resultado['_merge'] == 'left_only']
    divergentes = conciliadas[conciliadas['valor_divergente']]

    console.print(tabela_resumo(
        len(resultado), len(conciliadas), len(pendentes), len(divergentes)))

    if not pendentes.empty:
        console.print(tabela_pendentes(pendentes))
    else:
        console.print('[green]Nenhuma nota pendente de entrada.[/green]')

    if not divergentes.empty:
        console.print(
            f'[red]Atenção:[/red] {len(divergentes)} nota(s) com diferença '
            'de valor entre emissão e entrada.')

    # --- Salvamento
    console.print(Rule('[bold]4. Salvando resultados[/bold]', style='cyan'))
    salva_excel(conciliadas, FILE_CONCILIADAS)
    salva_excel(pendentes, FILE_PENDENTES)
    salva_excel(divergentes, FILE_DIVERGENTES)

    console.print(Panel.fit(
        '[bold green]PROCESSO FINALIZADO COM SUCESSO[/bold green]',
        border_style='green',
    ))


if __name__ == '__main__':
    main()
