# ⚙️ Automação de Atividades de Backoffice (RPA)

Script em **Python** que automatiza o envio de planilhas de investimentos para o sistema **UNO** e a geração de relatórios e APRs dentro do sistema.

**Metodologia:** foram usados o VS Code e a linguagem Python.

### ▶️ [Ver a automação funcionando (vídeo)](https://www.youtube.com/watch?v=7pwIwK7izuM&t=91s)

## 🎯 Contexto e objetivo

As principais funcionalidades do código são:

- ➡️ Abrir o navegador Chrome e acessar o site do UNO.
- ➡️ Fazer login no sistema UNO.
- ➡️ Navegar pelas funcionalidades do UNO, como "Coleta de Saldos" e "Fundos".
- ➡️ Importar as planilhas de movimentações financeiras para o sistema.
- ➡️ Lançar os saldos das contas e carteiras.
- ➡️ Gerar relatórios de rentabilidade e APRs.
- ➡️ Ler uma planilha Excel, formatar os dados e convertê-la em um arquivo CSV para importação no sistema **QUANTUM**.
- ➡️ Ler um arquivo PDF, extrair o texto e importar o texto extraído para o sistema, com a biblioteca **pypdf**.

📄 Código: [`uno_backoffice.py`](uno_backoffice.py). Os caminhos de pasta e o cliente ficam configuráveis no topo do arquivo.

## 💡 Insights e resultados

- 💡 **Economia de tempo** nas atividades administrativas rotineiras do backoffice.
- 💡 O código usa diversas bibliotecas Python, como **pyautogui, pandas, datetime, subprocess, keyboard e pypdf**, para interagir com a interface do UNO e processar os dados das planilhas.
- 💡 A extração automática de texto de PDFs é útil para análise de dados, processamento de textos e integração com outros sistemas.

> 📊 O acompanhamento dessas atividades é feito no [Dashboard de Performance do Backoffice](https://github.com/anajuliapf/dashboard-performance-backoffice).

## 🧰 Ferramentas

Python · VS Code · pyautogui · pandas · keyboard · subprocess · pypdf · Excel
