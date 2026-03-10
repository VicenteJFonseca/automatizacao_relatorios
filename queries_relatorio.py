# INSTALADORES

# Instalando PandaSQL e SQLAlquemy no prompt e comando do Windows

# python -m pip install -U pandasql
# python -m pip install --upgrade SQLAlchemy greenlet "typing-extensions>=4.2.0"

# Verificar versão do SQLAlquemy
# python -m pip show sqlalchemy

#Instalar leitor de arquivos em formato excel do pandas
# python -m pip install pandas openpyxl


# Importanod bibliotecas Python
import pandas as pd
from pandasql import sqldf

# BASE DE DADOS do BIOCEN (Biotério Central)

# Importando a base de dados contendo as tabelas ceua (dados dos protocolos CEUA) e de pedidos (dados dos pedidos de animais)

demanda_animais = pd.read_excel('C:/Users/Vicente JF/Documents/Projeto 1 _ Portfólio/dataset/dataset_biocen_anonimizado.xlsx',
                                sheet_name = ['tabela_ceua','tabela_pedidos','tabela_pesquisadores','tabela_precos'])
ceua = demanda_animais.get('tabela_ceua')
solicitacao = demanda_animais.get('tabela_pedidos')
pesquisadores = demanda_animais.get('tabela_pesquisadores')
precos = demanda_animais.get('tabela_precos')

# CONSULTAS: SQL Queries

# Função lambda para realização da linguagem SQL usando a linhagem Python através da API PandaSQL.

pysqldf = lambda q: sqldf(q, globals())

# PARTE I: RELATÓRIO DE SALDO POR PROJETO CEUA:
# A consulta query1 informa o saldo de animais ainda disponíveis para utilizar em um determinado projeto científico que/
# utiliza animais para experimentação. Em outras palavras, a consulta informa quantos animais de cada linhagem e sexo/
# o pesquisador ainda pode utilizar em um determinado projeto CEUA (Comissão de Ética de Uso Animal)

query1 = """
SELECT ceua.Pesquisador,
       ceua.id_ceua_pseud AS Protocolo_CEUA,
       ceua.Linhagem,
       ceua.Sexo,
       ceua.Quantidade AS Quantidade_CEUA,
       SUM(solicitacao.Quantidade) AS Solicitado_por_CEUA,
       (ceua.Quantidade - SUM(solicitacao.Quantidade)) AS Saldo
FROM ceua
    INNER JOIN solicitacao
    ON ceua.id_ceua_pseud = solicitacao.id_ceua_pseud

WHERE solicitacao.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
OR solicitacao.[Status do Pedido] IS NULL

GROUP BY ceua.id_ceua_pseud

ORDER BY "Saldo" ASC;
"""

saldo_ceua = pysqldf(query1)


# PARTE II: RELATÓRIO DE TOTAIS DE PROJETOS ATENDIDOS POR ANO E MÉDIA ANUAL NO PERÍODO DE 2023 A 2025
# Observa-se que na Query (query2) abaixo:
# Extrai ano da coluna "Data do email (pedido) para criar a coluna "ano_do_pedido"
# Depois filtra os pedidos retidos e irregulares usando o filtro WHERE em categorias da coluna "Status do Pedido"

query2 = """
SELECT
   STRFTIME('%Y', [Data do email \n(pedido)]) AS ano_do_pedido, 
   COUNT(DISTINCT id_ceua_pseud) AS total_projetos_atendidos
FROM solicitacao
WHERE solicitacao.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
GROUP BY ano_do_pedido;
"""
projetos_atendidos_por_ano = pysqldf(query2)

# Média de projetos por mês.
# Query 3 retorna a média de projetos por mês no triênio 2023-2025.

query3 = """

SELECT 
   ROUND(AVG(numero_projetos_mes), 2) AS media_projetos_mes
FROM (
        SELECT 
           STRFTIME('%Y-%m', [Data do email \n(pedido)]) AS ano_mes,
           COUNT(DISTINCT id_ceua_pseud) AS numero_projetos_mes
        FROM solicitacao
        WHERE solicitacao.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
        GROUP BY ano_mes        
     ) AS subquery_projetos_ceua_mes;

"""
media_projetos_mes_2023_a_2025 = pysqldf(query3)


## Média Anual de projetos atendidos no triênio 2023-2025
## Query 4 retorna a média anual de projetos CEUA atendidos pelo Biotério Central

query4 = """
SELECT 
   ROUND(AVG(total_projetos_atendidos), 2) AS media_anual_projetos
FROM (
      SELECT
         STRFTIME('%Y', [Data do email \n(pedido)]) AS ano_do_pedido, 
         COUNT(DISTINCT id_ceua_pseud) AS total_projetos_atendidos
      FROM solicitacao
      WHERE solicitacao.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
      GROUP BY ano_do_pedido

      ) AS subquery_media_anual_projetos;

"""
media_anual_projetos_2023a2025 = pysqldf(query4)


# PARTE III - RELATÓRIO DE PESQUISADORES 
# A consulta query5 mostra a quantidade pesquisadores atendidos por ano

query5 = """
SELECT
     STRFTIME('%Y', [Data da retirada]) AS ano,
     COUNT(DISTINCT Pesquisador) AS numero_pesquisadores
FROM solicitacao
WHERE [Data da retirada] IS NOT NULL
GROUP BY ano
HAVING ano <> '2026';
"""
pesquisadores_por_ano_atendidos = pysqldf(query5)


## Consulta query6 retorna o rank de 20 pesquisadores com mais pedidos em 2025

query6 = """
SELECT 
     sol.Pesquisador AS Pesquisadores,
     pesq.Unidade AS Unidade,
     pesq.Departamento AS Departamento,
     COUNT(sol.Pesquisador) AS QTD_Pedidos,
     STRFTIME('%Y', sol.[Data do email \n(pedido)]) AS ano
FROM solicitacao AS sol
     INNER JOIN pesquisadores AS pesq
     ON sol.Pesquisador = pesq.Pesquisador
WHERE ano == '2025'
GROUP BY Pesquisadores
ORDER BY QTD_Pedidos DESC
LIMIT 20;
"""
top20_pesquisadores = pysqldf(query6)

# Observação: TOP só existe no T-SQL (Microsoft SQL Server). Logo, usei o comando LIMIT para alcançar o /
# o mesmo resultado no SQLite.

# Observação 2: Note que depois de fazer a normalização da base de dados em um esquema estrela, é possível fazer /
# essa query usando uma INNER JOIN entre pedidos e pesquisadores para "trazer" as dimensões "Unidade" e "Departamento"


# PARTE IV - DEMANDA DE ANIMAIS
# Consulta abaixo mostra qual a idade de animais mais solicitadas pelos pesquisadores. 

query7 = """
SELECT
     [Idade em semanas],
     COUNT([Idade em semanas]) AS Frequencia,
     STRFTIME('%Y', [Data do email \n(pedido)]) AS ano
FROM solicitacao
WHERE [Idade em semanas] IS NOT NULL AND ano = '2025'
GROUP BY [Idade em semanas]
ORDER BY Frequencia DESC;
"""
idade_animais_por_pedido = pysqldf(query7)


# Query retorna a quantidade de animais para os anos de 2023, 2024 e 2025. Além disso, a query/
# também retorna a variação percentual no período entre os anos 2023 e 2024 e depois a variação percentual/
# para os biênio 2024-2025.

query8 = """
SELECT
      STRFTIME('%Y', [Data da retirada]) AS Ano,
      Linhagem,
      SUM(Quantidade) AS QTD_Total
FROM solicitacao
WHERE ano = "2025"
GROUP BY Ano, Linhagem;
"""
quantidade_entregue_ano_linhagens_2025 = pysqldf(query8)


### Participação em termos percentuais de cada linhagem de animal nas vendas anuais.

query9 = """

WITH QTD_Total_with AS (
    SELECT CAST(SUM(Quantidade) AS REAL) AS Total_linhagens
    FROM solicitacao
    WHERE 
       [Data da retirada] BETWEEN '2025-01-01' AND '2026-01-01' 
       AND [Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
)

SELECT
      STRFTIME('%Y', [Data da retirada]) AS Ano,
      Linhagem,
      SUM(Quantidade) AS Qtd_linhagens,
      ROUND((SUM(Quantidade)/TL.Total_linhagens)*100, 2) AS Porcentagem_linhagem
FROM solicitacao
CROSS JOIN
    QTD_TOTAL_with AS TL
WHERE
   ano = "2025"
   AND [Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
GROUP BY Linhagem;

"""
percentual_linhagens_2025 = pysqldf(query9)

## PARTE IV : VENDA DE ANIMAIS
### Consulta retorna tabela pedidos com os respectivos valores dos animais.

query10 = """
SELECT
      sol.[Data do email \n(pedido)] AS Data_Pedido,
      sol.[Data da retirada] AS Data_Entrega,
      sol.Pesquisador,
      sol.id_ceua_pseud AS Projeto_CEUA,
      sol.Linhagem,
      sol.[Idade em semanas] AS Idade_N_Semanas,
      sol.Quantidade AS QTD_animais,
      pc.[Preço Unitário] AS Valor_Unitario,
      (sol.Quantidade * pc.[Preço Unitário]) AS Valor_Total 
FROM solicitacao AS sol
LEFT JOIN 
    precos AS pc ON
    sol.[Modalidade de Solicitação] = pc.[Modalidade de Solicitação] AND
    sol.Linhagem = pc.Linhagem AND
    sol.[Idade em semanas] = pc.[Idade em semanas]
WHERE sol.[Data da retirada] BETWEEN '2025-01-01' AND '2026-01-01'
      AND sol.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA') ;
"""
valores_pedidos_2025 = pysqldf(query10)

# Consulta retorna preços internos - isto é, para pesquisadores da UFMG - médios nos anos 2024 e 2025.

query11 = """
SELECT 
    Linhagem,
    AVG(CASE WHEN strftime('%Y', Data_Entrega) = '2024' THEN Valor_Unitario END ) AS Preco_Medio_2024,
    AVG(CASE WHEN strftime('%Y', Data_Entrega) = '2025' THEN Valor_Unitario END ) AS Preco_Medio_2025
FROM (
      SELECT
           sol.[Data do email \n(pedido)] AS Data_Pedido,
           sol.[Data da retirada] AS Data_Entrega,
           sol.Pesquisador,
           sol.id_ceua_pseud AS Projeto_CEUA,
           sol.Linhagem,
           sol.[Idade em semanas] AS Idade_N_Semanas,
           sol.Quantidade AS QTD_animais,
           pc.[Preço Unitário] AS Valor_Unitario,
           (sol.Quantidade * pc.[Preço Unitário]) AS Valor_Total 
      FROM solicitacao AS sol
      LEFT JOIN 
           precos AS pc ON
           sol.[Modalidade de Solicitação] = pc.[Modalidade de Solicitação] AND
           sol.Linhagem = pc.Linhagem AND
           sol.[Idade em semanas] = pc.[Idade em semanas]
      WHERE sol.[Data da retirada] BETWEEN '2024-01-01' AND '2026-01-01'
           AND sol.[Modalidade de Solicitação] IN ('Programada', 'Não Programada')
           AND sol.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
           
      )  AS Valores_Animais

GROUP BY Linhagem;

"""

precos__internos_medios__24a25 = pysqldf(query11)

# Consulta retorna preços externos médios nos anos 2024 e 2025.

query12 = """
SELECT 
    Linhagem,
    AVG(CASE WHEN strftime('%Y', Data_Entrega) = '2024' THEN Valor_Unitario END ) AS Preco_Medio_2024,
    AVG(CASE WHEN strftime('%Y', Data_Entrega) = '2025' THEN Valor_Unitario END ) AS Preco_Medio_2025
FROM (
      SELECT
           sol.[Data do email \n(pedido)] AS Data_Pedido,
           sol.[Data da retirada] AS Data_Entrega,
           sol.Pesquisador,
           sol.id_ceua_pseud AS Projeto_CEUA,
           sol.Linhagem,
           sol.[Idade em semanas] AS Idade_N_Semanas,
           sol.Quantidade AS QTD_animais,
           pc.[Preço Unitário] AS Valor_Unitario,
           (sol.Quantidade * pc.[Preço Unitário]) AS Valor_Total 
      FROM solicitacao AS sol
      LEFT JOIN 
           precos AS pc ON
           sol.[Modalidade de Solicitação] = pc.[Modalidade de Solicitação] AND
           sol.Linhagem = pc.Linhagem AND
           sol.[Idade em semanas] = pc.[Idade em semanas]
      WHERE sol.[Data da retirada] BETWEEN '2024-01-01' AND '2026-01-01'
           AND sol.[Modalidade de Solicitação] = 'Venda Externa'
           AND sol.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
           
      )  AS Valores_Animais

 GROUP BY Linhagem;

"""

precos__externos_medios__24a25 = pysqldf(query12)

# Consulta retorna o ranqueamento das idades dos animais em semanas mais frequentes nos pedidos.

query13 = """
SELECT
    STRFTIME('%Y', [Data da retirada]) AS ano,
    [Idade em semanas],    
    COUNT([Idade em semanas]) AS Frequencia
FROM solicitacao 
WHERE ano == '2025'
GROUP BY [Idade em semanas]
ORDER BY Frequencia DESC;
"""
idade_animais_por_pedido_2025 = pysqldf(query13)


# Consulta retorna relatório com os quantitativos de animais considerando linhagem e idade que cada pesquisador que faz/
# /parte do Grupo de Pesquisa bem como também os respectivos débitos dos mesmos.

query14 = """
SELECT
     sol.[Data do email \n(pedido)] AS Data_Pedido,
     sol.[Data da retirada] AS Data_Entrega,
     sol.Pesquisador,
     peq.Unidade,
     peq.Departamento,
     sol.id_ceua_pseud AS Projeto_CEUA,
     sol.Linhagem,
     sol.[Idade em semanas] AS Idade_N_Semanas,
     sol.Quantidade AS QTD_animais,
     pc.[Preço Unitário] AS Valor_Unitario,
     (sol.Quantidade * pc.[Preço Unitário]) AS Valor_Total 
FROM solicitacao AS sol
    INNER JOIN precos AS pc ON 
        sol.[Modalidade de Solicitação] = pc.[Modalidade de Solicitação] AND
        sol.Linhagem = pc.Linhagem AND
        sol.[Idade em semanas] = pc.[Idade em semanas]
     INNER JOIN pesquisadores AS peq ON
        sol.Pesquisador = peq.Pesquisador      
WHERE sol.[Data da retirada] BETWEEN '2025-10-01' AND '2025-10-31'
     AND sol.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
     AND peq.Grupo_de_pesquisa = 'sim'
ORDER BY [Data da retirada] ASC;

"""
retiradas_grupo_pesquisa_mes_out_2025 = pysqldf(query14)

## PARTE V: UNIDADES E DEPARTAMENTOS ATENDIDOS
## Query 15: Ranqueamento das Unidades Acadêmicas atendidas segundo a quantidade de animais para experimentação pedidos ao Biocen

query15 = """

SELECT
    peq.Unidade,
    SUM(sol.Quantidade) AS QTD_animais_pedidos    
FROM solicitacao AS sol
    INNER JOIN pesquisadores AS peq ON
    sol.Pesquisador = peq.Pesquisador
WHERE sol.[Data da retirada] BETWEEN '2025-01-01' AND '2025-12-31'
     AND sol.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
     AND sol.[Modalidade de Solicitação] <> 'Venda Externa'
GROUP BY peq.Unidade
ORDER BY SUM(sol.Quantidade) DESC;

"""
rank_unidades_2025 = pysqldf(query15)

## Query 16: Ranqueamento dos departamentos atendidos em 2025

query16 = """

SELECT
    peq.Unidade,
    peq.Departamento,
    SUM(sol.Quantidade) AS QTD_animais_pedidos    
FROM solicitacao AS sol
    INNER JOIN pesquisadores AS peq ON
    sol.Pesquisador = peq.Pesquisador
WHERE sol.[Data da retirada] BETWEEN '2025-01-01' AND '2025-12-31'
     AND sol.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
     AND sol.[Modalidade de Solicitação] <> 'Venda Externa'
GROUP BY peq.Departamento, peq.Unidade
ORDER BY SUM(sol.Quantidade) DESC;

"""
rank_departamentos_2025 = pysqldf(query16)

## Query 17: Ranqueamento das instituições externas no biêncio 2024-2025.

query17 = """

SELECT
    peq.Unidade,
    SUM(sol.Quantidade) AS QTD_animais_pedidos    
FROM solicitacao AS sol
    INNER JOIN pesquisadores AS peq ON
    sol.Pesquisador = peq.Pesquisador
WHERE sol.[Data da retirada] BETWEEN '2024-01-01' AND '2025-12-31'
     AND sol.[Status do Pedido] NOT IN ('Cancelado', 'Qtd CEUA atingida', 'Pendências no CEUA')
     AND sol.[Modalidade de Solicitação] = 'Venda Externa'
GROUP BY  peq.Unidade
ORDER BY SUM(sol.Quantidade) DESC;

"""
instituicoes_externas_2024_2025 = pysqldf(query17)


## GERAR RELATÓRIO EXCEL DAS CONSULTAS REALIZADAS

# Exportando consultas geradas com o objetivo de gerar um relatório no formato Excel.
with pd.ExcelWriter(r'C:/Users/Vicente JF/Documents/Projeto 1 _ Portfólio/dataset/relatorio_pedido_e_vendas_animais.xlsx') as relatorio_pedidos_e_vendas_animais:
    saldo_ceua.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='saldo_ceua') 
    projetos_atendidos_por_ano.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='projetos_atendidos') 
    media_projetos_mes_2023_a_2025.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='projetos_mes')
    media_anual_projetos_2023a2025.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='projetos_ano')
    pesquisadores_por_ano_atendidos.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='pesquisadores_ano')
    top20_pesquisadores.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='top20_pesquisadores')
    idade_animais_por_pedido.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='idade_animais')
    idade_animais_por_pedido_2025.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='idade_animais_25')
    quantidade_entregue_ano_linhagens_2025.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='QTD_animais_2025')
    percentual_linhagens_2025.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='perc_linhagens')
    valores_pedidos_2025.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='valores_medios')
    precos__internos_medios__24a25.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='precos_internos')
    precos__externos_medios__24a25.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='precos_externos')
    retiradas_grupo_pesquisa_mes_out_2025.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='grupo_pesquisa')
    rank_unidades_2025.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='rank_unidades')
    rank_departamentos_2025.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='rank_departamentos')
    instituicoes_externas_2024_2025.to_excel(relatorio_pedidos_e_vendas_animais, sheet_name='rank_departamentos') 
