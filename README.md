# 📊 Evolução do IDEB e Indicadores nos Municípios da Paraíba

Aplicação interativa desenvolvida com **Streamlit** para analisar a evolução do **Índice de Desenvolvimento da Educação Básica (IDEB)** e indicadores educacionais dos municípios da **Paraíba**, permitindo comparações, visualizações e rankings de desempenho.

---

## 🚀 Funcionalidades

A aplicação contém **cinco abas principais**, acessíveis na interface Streamlit:

### 1️⃣ Evolução do IDEB
- Exibe a evolução do IDEB ao longo dos anos (2005 a 2023) para o município selecionado.  
- Apresenta gráfico interativo com linha temporal e valores de IDEB por ano.

### 2️⃣ Indicadores
- Mostra os indicadores educacionais de 2020 e 2023:
  - **Instituições**
  - **Projetos**
  - **Beneficiados**
- Apresenta comparações automáticas com mensagens indicando aumento, queda ou estabilidade.

### 3️⃣ Comparações
- Permite comparar o desempenho do IDEB entre **múltiplos municípios** em um gráfico de linhas interativo.

### 4️⃣ Panorama Geral
- Exibe a evolução do IDEB em **todos os municípios da Paraíba** simultaneamente.  
- Ideal para identificar tendências globais e contrastes regionais.

### 5️⃣ Ranking de Evolução
- Calcula a **variação percentual** do IDEB entre o primeiro e o último registro disponível (2005–2023).  
- Classifica os municípios em quatro categorias:
  - 🟢 **Excelente** (> 50%)
  - 🔵 **Bom** (30% – 50%)
  - 🟡 **Razoável** (15% – 30%)
  - 🔴 **Ruim** (< 15%)
- Exibe uma tabela interativa com **cores automáticas** para facilitar a análise visual.

---

## ⚙️ Tecnologias Utilizadas

- **[Streamlit](https://streamlit.io/)** — Interface web interativa.
- **[Pandas](https://pandas.pydata.org/)** — Manipulação e limpeza de dados.
- **[Altair](https://altair-viz.github.io/)** — Visualização de dados.
- **[NumPy](https://numpy.org/)** — Cálculos e operações matemáticas.

---

## 🧩 Pré-requisitos

Certifique-se de ter o **Python 3.8+** instalado.  
Em seguida, instale as dependências com:

```bash
pip install streamlit pandas altair numpy

---

## Para rodar o app
Insira 'streamlit run app.py' no terminal.



## 📂 Estrutura do Projeto

