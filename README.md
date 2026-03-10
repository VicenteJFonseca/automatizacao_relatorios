
### O PROJETO DE DADOS
O presente projeto se trata da automatização de relatórios de dados de demanda e venda de animais do BIOCEN mais demandados pela direção/coordenação. São 17 (dezessete) relatórios ao todo gerados e que estão enumerados a seguir: 

1.	Saldo CEUA

2.	Projetos Atendidos por Ano

3.	Média de Projetos por Mês (Período: 2023-2025)

4.	Média Anual de Projetos (Período: 2023-2025)

5.	Pesquisadores Atendidos por Ano

6.	Top 20 Pesquisadores

7.	Idade dos Animais por Pedido

8.	Quantidade Entregue de Linhagens (Período: 2025)

9.	Percentual de Linhagens (Período: 2025)

10.	Valores dos Pedidos (Período: 2025)

11.	Preços Internos Médios (Período: 2024-2025)

12.	Preços Externos Médios (Período: 2024-2025)

13.	Idade dos Animais por Pedido (Período: 2025)

14.	Retiradas por Grupo de Pesquisa (outubro/2025)

15.	Ranking de Unidades (Período: 2025)

16.	Ranking de Departamentos (Período: 2025)

17.	Instituições Externas (Período: 2024-2025)

### TECNOLOGIAS USADAS

•	Python <br>
•	SQL <br>
•	Excel

### OBJETIVO
Este relatório foi desenvolvido para munir, de forma ágil, o coordenador do BIOCEN das informações necessárias para tomada de decisões e aplicação de projetos tanto para a própria Universidade quanto às instituições de fomento, tais como FAPEMIG E FINEP, com o intuito de obter recursos para investimentos e melhorias na infraestrutura.

### DEFINIÇÕES
- BIOCEN: O Biotério Central da UFMG é um laboratório de biomodelos que são animais voltados para experimentação científica. Esses animais são disponibilizados a preços subsidiados a pesquisadores tanto da UFMG quanto para instituições externas, como por exemplo, a USP e a UFRJ. O BIOCEN produz animais SPF (Specific Pathogen Free), ou seja, livre de patógenos. Além disso, são animais com alta padronização genética. Essa alta qualidade é importante para não causar vieses nas pesquisas científicas; dentre elas, o desenvolvimento da vacina contra a dependência de cocaína e crack empreendida por pesquisadores da UFMG e que utilizaram animais do BIOCEN. A vacina contra o crack/cocaína já está na fase de testes em voluntários. <br>
- Linhagens: animais geneticamente padronizados. Podem ser homogênicos (clones) ou heterogênicos (diferentes geneticamente entre si). As linhagens produzidas no BIOCEN são: Balb, C57 e CD1 (camundongos) e Wistar (rato). <br>
- CEUA: Comissão de Ética de Uso Animal para Experimentação. Pesquisadores só podem usar animais em pesquisas se tiverem autorização comprovada por esse documento. O CEUA especifica quanto animais podem ser utilizados e qual espécie, linhagem e sexo dos animais devem ser utilizados na pesquisa. Os pesquisadores podem retirar parcialmente os animais do BIOCEN. Daí a importância do controle do quantitativo que é um dos relatórios gerados por esse projeto.
### BASE DE DADOS
**OBSERVAÇÃO:** No presente projeto, os dados sencíveis foram anonimizados e os demais dados foram autorizados pela coordenação do BIOCEN para que eu pudesse colocá-los em um repositório no GitHub; conforme Lei Geral de Proteção de Dados (LGPD - Lei nº 13.709/2018). <br>
Planillhas Excel que constam no dataset_biocen:<br>
•	pedidos - dados dos pedidos dos pesquisadores com informações relevantes dos animais (idade, linhagem, sexo, espécie, quantidade, etc.) <br>
•	ceua - certificado de autorização para pesquisa com animais que cada pesquisador solicitante deve ter especificando: espécie, linhagem, sexo e quantidade. <br>
•	pesquisadores - dados dos pesquisadores com informações sobre a unidade (faculdade), departamento, CPF, etc. <br>
•	precos - tabela de preços que varia por idade (em semanas) e espécie (rato ou camundongo). <br>
### COMO FUNCIONA
- Etapa I: Tratamento dos Dados - Utilizando Python, foi realizado a limpeza dos dados, tais como: padronização na nomenclatura de categorias, eliminação de espaços vazios e dados do tipo string, remoção de características (variáveis) irrelevantes para o presente projeto, etc. <br>
- Etapa II:Anonimização dos Dados Sensíveis - Colunas com os dados dos pesquisadores e informações dos certificados CEUA foram anonimizados.  O certificado CEUA é importante anonimizar para não provocar a quebra de patentes das pesquisas. <br>
- Etapa III: Combinação de Python e SQL através das bibliotecas PandaSQL e da ferramenta SQLAlchemy a fim de fazer o carregamento da base de dados e realizar consultas na linguagem SQL. As consultas foram salvas como Pandas Dataframe. <br>
- Etapa IV: As consultas salvas em Pandas Dataframe são exportadas em um único arquivo Excel em planilhas separadas. <br>
### RESULTADO
Foi possível com essa automatização reduzir em 83% o tempo de entrega dos relatórios à coordenação do BIOCEN.
 
