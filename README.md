# Central de Comparadores

A **Central de Comparadores** é uma plataforma baseada em Streamlit projetada para facilitar o cruzamento e validação de dados em operações logísticas e financeiras. A ferramenta automatiza operações de `merge` e verificação de divergências de valores, sem a necessidade de fórmulas complexas no Excel.

## 🚀 Como Executar

**Pré-requisitos:** Python 3 instalado.

1. Instale as dependências:
```bash
pip install -r requirements.txt
```
*(As dependências incluem `streamlit`, `pandas` e `openpyxl`)*

2. Execute a aplicação (a partir da pasta raiz do projeto):
```bash
python -m streamlit run app.py
```

3. O sistema será aberto automaticamente no seu navegador.

---

## 🛠 Funcionalidades

A plataforma oferece dois módulos principais focados em diferentes necessidades de análise detalhadas abaixo.

### 1. 🔀 Comparador Genérico (Qualquer Planilha)
Ideal para cruzamentos universais de dados. Permite comparar planilhas de diferentes sistemas com estruturas variadas.

**Como usar:**
1. **Upload:** Faça upload de uma ou múltiplas planilhas no lado A (Pedidos/Base) - elas serão consolidadas automaticamente no sistema. E faça upload de uma planilha no lado B (Referência/Preço). Suporte a Excel, CSV e TXT (com tentativa de auto-detectar tabulação).
2. **Chave de Cruzamento:** Selecione as colunas que servirão como ID único (ex: Código de Barras, CPF, ID do Pedido) dos dois lados para realizar o merge. O sistema suporta até 4 chaves combinadas.
3. **Pares de Comparação de Valor:** Selecione pares de colunas (Lado A e Lado B) para comparar valores monetários/quantitativos. O sistema calculará a diferença matemática entre eles.
4. **Colunas Adicionais:** Escolha colunas extras das duas tabelas para que sejam visualizadas no relatório final.
5. **Resultado:** Obtenha uma visualização detalhada com status automático `OK` (valores exatos), `DIVERGENTE` (valores diferentes) ou `NÃO ENCONTRADO`.

### 2. 🔍 Comparador de SKUs e Preços (Netshoes)
Uma ferramenta rápida e otimizada, desenvolvida especificamente para o fluxo financeiro diário de cruzamento entre Pedidos e Sellers.

**Como usar:**
1. **Upload Rápido:** Faça o upload da `Planilha de Pedidos` de um lado e da `Planilha de Preço / Seller` de outro.
2. **Auto-Detecção:** O sistema tentará detectar automaticamente onde estão as colunas de "SKU Lojista" e "Valor do SKU". Se a detecção automática não encontrar os nomes exatos, você poderá selecionar manualmente nos seletores.
3. **Métricas Instantâneas:** Após processar, a ferramenta entrega painéis rápidos com o número total de resultados: quantidade de registros corretos (`OK`), registros com diferenças financeiras (`DIVERGENTE`) e pendências de cadastro (`NÃO ENCONTRADOS`).
4. **Filtros e Cores:** As linhas da tabela resultado ficam coloridas automaticamente dependendo da sua divergência.
5. **Ação Integrada:** Baixe o relatório resultante com as correções de preços evidenciadas no formato Excel.

---

## 📐 Estrutura do Projeto

- `app.py`: Interface inicial da Central de Comparadores (o ponto de entrada da aplicação).
- `pages/Comparador_Generico.py`: Módulo da ferramenta de comparação genérica com painel configurável.
- `pages/Comparador_Netshoes.py`: Módulo especializado para a validação rápida de SKUs.
- `requirements.txt`: Definição de pacotes Python em uso.
