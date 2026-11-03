"""
RPA — Automação de atividades de backoffice no sistema UNO.

Parte 1: importa a planilha de movimentações (MOVS) no UNO
Parte 2: importa os saldos (Ativos e Contas)
Parte 3: lança a carteira, gera o relatório de rentabilidade e o lote de APRs
Parte 4: prepara os dados para o QUANTUM/DAIR (Excel -> texto tabulado)
Parte 5: extrai o texto do relatório do UNO em PDF (pypdf)

A automação usa a posição dos elementos na tela (pyautogui), então as
coordenadas foram calibradas para a resolução do computador original.
Use pyautogui.position() (no fim do arquivo) para recalibrar.
"""

import time

import pandas as pd
import pyautogui
from pypdf import PdfReader

# ------------------------------------------------------------------
# Configuração — ajuste antes de rodar
# ------------------------------------------------------------------
URL_UNO = "https://unoapp.com.br/login"
URL_CADPREV = "https://cadprev.previdencia.gov.br/Cadprev/pages/index.xhtml"
CIDADE = "CIDADE"                                  # cliente (município) a processar
PASTA_ARQUIVOS = r"C:\caminho\para\pasta\do\cliente"
PLANILHA_QUANTUM = r"C:\caminho\para\planilha.xlsx"
RELATORIO_PDF = r"C:\caminho\para\relatorio_uno.pdf"
MES_LANCAMENTO = 2                                 # mês a lançar no QUANTUM

pyautogui.PAUSE = 0.4


def abrir_chrome(url):
    pyautogui.press("win")
    pyautogui.write("Chrome")
    pyautogui.press("backspace")
    pyautogui.press("enter")
    pyautogui.write(url)
    pyautogui.press("enter")
    time.sleep(1)


def login_uno():
    """O login usa as credenciais salvas no navegador."""
    pyautogui.click(x=1001, y=38)
    pyautogui.click(x=1141, y=519)


def selecionar_cidade(y_opcao=239):
    pyautogui.click(x=1044, y=150)
    pyautogui.click(x=1202, y=153)
    pyautogui.press("backspace", presses=20)  # apaga a cidade atual
    time.sleep(1)
    pyautogui.write(CIDADE)
    pyautogui.click(x=1047, y=203)
    pyautogui.click(x=1063, y=y_opcao)


def escolher_arquivo(x_nome, y_nome, x_abrir, y_abrir, x_pesquisa):
    """Navega no explorador de arquivos até a planilha da cidade."""
    pyautogui.click(x=x_nome, y=y_nome)              # campo "Nome"
    pyautogui.write(PASTA_ARQUIVOS)
    pyautogui.click(x=x_abrir, y=y_abrir, clicks=2)  # "Abrir"
    time.sleep(1)
    pyautogui.click(x=x_pesquisa, y=50)              # pesquisar na pasta
    pyautogui.write(CIDADE)
    pyautogui.press("enter")
    time.sleep(1)


# ------------------------------------------------------------------
# Parte 1 — Importar movimentações (MOVS)
# ------------------------------------------------------------------
def importar_movs():
    pyautogui.click(x=28, y=319)    # Investimentos
    pyautogui.click(x=102, y=425)   # Coleta de saldos
    pyautogui.click(x=224, y=220)   # Fundos
    selecionar_cidade()

    pyautogui.click(x=1306, y=663, clicks=2)  # (+)
    pyautogui.click(x=1306, y=663)
    pyautogui.click(x=1307, y=591)            # Importar movs
    escolher_arquivo(425, 547, 539, 575, 622)
    pyautogui.click(x=391, y=128, clicks=2)   # planilha MOVS
    time.sleep(2)
    pyautogui.click(x=1064, y=578)            # Iniciar importação
    time.sleep(10)


# ------------------------------------------------------------------
# Parte 2 — Importar saldos (Ativos e Contas)
# ------------------------------------------------------------------
def importar_saldos():
    pyautogui.click(x=104, y=487)   # Ativos e contas
    pyautogui.click(x=1305, y=668)  # (+)
    pyautogui.click(x=1305, y=597)  # Importar
    escolher_arquivo(411, 546, 540, 573, 638)
    pyautogui.click(x=388, y=123)
    pyautogui.click(x=360, y=127, clicks=2)  # planilha de saldos
    time.sleep(7)
    pyautogui.click(x=886, y=485)            # Iniciar importação
    time.sleep(6)


# ------------------------------------------------------------------
# Parte 3 — Lançar carteira, gerar relatório e APRs
# ------------------------------------------------------------------
def lancar_carteira_e_relatorios():
    pyautogui.click(x=104, y=426)   # Coleta de saldos
    pyautogui.click(x=1267, y=220)  # Lançar carteira
    time.sleep(3)
    pyautogui.click(x=893, y=579)   # Validar e lançar
    time.sleep(4)

    pyautogui.click(x=99, y=292)    # Rentabilidade
    pyautogui.click(x=1232, y=222)  # Gerar relatório
    pyautogui.click(x=1228, y=671)  # Confirmar
    time.sleep(15)

    pyautogui.click(x=101, y=362)   # Carteira
    pyautogui.click(x=409, y=226)   # APRs
    pyautogui.click(x=890, y=223)   # Gerar lote
    pyautogui.click(x=735, y=469)   # Exibir CPFs


# ------------------------------------------------------------------
# Parte 4 — Preparar dados para o QUANTUM / DAIR
# ------------------------------------------------------------------
def formatar_float(valor):
    """1234.5 -> '1.234,50'"""
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def preparar_quantum():
    tabela = pd.read_excel(PLANILHA_QUANTUM, sheet_name=1)  # segunda aba
    tabela["DATA"] = pd.to_datetime(tabela["DATA"]).dt.strftime("%d/%m/%Y")
    tabela = tabela[["MES", "CNPJ", "DATA", "TIPO"]]
    tabela = tabela.loc[tabela["MES"] == MES_LANCAMENTO].drop(columns=["MES"])
    tabela["TIPO"] = tabela["TIPO"].apply(formatar_float)
    # Texto tabulado e sem cabeçalho, pronto para colar no sistema
    return tabela.to_csv(index=False, header=None, sep="\t", encoding="UTF-8")


def abrir_novo_dair():
    abrir_chrome(URL_CADPREV)        # login no CADPREV, se necessário, é manual
    pyautogui.click(x=94, y=375)     # Investimentos
    pyautogui.click(x=77, y=439)     # DAIR
    pyautogui.click(x=120, y=469)    # Consultar demonstrativos
    pyautogui.click(x=651, y=294)    # Selecionar cidade
    time.sleep(10)
    pyautogui.click(x=863, y=701)    # Novo DAIR
    time.sleep(1)
    pyautogui.click(x=643, y=349)    # OK
    time.sleep(2)


# ------------------------------------------------------------------
# Parte 5 — Extrair texto do relatório do UNO (PDF)
# ------------------------------------------------------------------
def extrair_pdf(caminho):
    reader = PdfReader(caminho)
    return "".join(page.extract_text() for page in reader.pages)


def main():
    time.sleep(4)  # tempo para tirar a mão do mouse
    abrir_chrome(URL_UNO)
    login_uno()
    importar_movs()
    importar_saldos()
    lancar_carteira_e_relatorios()

    dados_quantum = preparar_quantum()
    print(dados_quantum)
    abrir_novo_dair()

    # Nova aba com o UNO aberto na coleta de saldos, para conferência
    pyautogui.hotkey("ctrl", "t")
    pyautogui.write(URL_UNO)
    pyautogui.press("enter")
    time.sleep(1)
    login_uno()
    selecionar_cidade(y_opcao=211)
    pyautogui.click(x=99, y=418)    # Coleta de saldos
    pyautogui.click(x=223, y=219)
    time.sleep(6)

    print(extrair_pdf(RELATORIO_PDF))


if __name__ == "__main__":
    main()
    # Para recalibrar coordenadas: posicione o mouse e rode
    # print(pyautogui.position())
