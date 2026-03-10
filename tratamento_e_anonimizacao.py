### ANONIMIZAÇÃO DOS DADOS SENSÍVEIS DO DATASET

## Digitar no Console: python -m pip install pandas numpy pandas openpyxl Faker hashlib

# Importando bibliotecas Python
import pandas as pd
import numpy as np
import hashlib

## Carregando a base de dados: tabelas "pedidos" e "ceua"

demanda_animais = pd.read_excel("C:/Users/Vicente JF/Documents/Projeto 1 _ Portfólio/dataset/dataset_biocen.xlsx",
                                sheet_name = ['pedidos','ceua','pesquisadores','precos'])
ceua = demanda_animais.get('ceua')
pedidos = demanda_animais.get('pedidos')
pesquisadores = demanda_animais.get('pesquisadores')
precos = demanda_animais.get('precos')

# PARTE I : TRATAMENTO E LIMPEZA DOS DADOS

# Tratamento de dados nas colunas contendo datas no dataframe 'pedidos_entregues'
# Transformando os dados da coluna 'Data da retirada' no tipo de dado object para datetime.
pedidos['Data da retirada'] = pd.to_datetime(pedidos['Data da retirada'], infer_datetime_format=True)
# Transformando os dados da coluna 'Data do email \n(pedido)' no tipo de dado object para datetime.
pedidos['Data do email \n(pedido)'] = pd.to_datetime(pedidos['Data do email \n(pedido)'], infer_datetime_format=True)

# Eliminando vazios nas categorias e nomes das colunas 'Pesquisador' da tabela 'ceua'
ceua['Pesquisador'] = ceua['Pesquisador'].str.strip()

# Eliminando vazios nas categorias e nomes das colunas "Pesquisador", "Unidade" e "Departamento" da tabela 'pesquisadores'
pesquisadores['Pesquisador'] = pesquisadores['Pesquisador'].str.strip()
pesquisadores['Departamento'] = pesquisadores['Departamento'].str.strip()
pesquisadores['Unidade'] = pesquisadores['Unidade'].str.strip()

# Trocar de lugar as observações da linha de índice 106 entre as colunas Departamento e Unidade. Elas estavam "trocadas de lugar"
pesquisadores.loc[106, ['Unidade', 'Departamento']] = pesquisadores.loc[106, ['Departamento', 'Unidade']].values

## Normalizando o nome da linhagem de camundongo para a mesma nomenclatura "C57bl/6j".
pedidos.loc[pedidos['Linhagem'].isin(['C57BL/6J','C57bl/6j','C57BL/6JUnib']), 'Linhagem'] = 'C57bl/6j'

## Normalizando nomes de departamentos na coluna "Departamento" da tabela "pesquisadores"
pesquisadores.loc[pesquisadores['Departamento'].isin([' Fisiologia e Biofísica','Fisiologia','Fisiologia e Biofísica']), 'Departamento'] = 'Fisiologia e Biofísica'
pesquisadores.loc[pesquisadores['Departamento'].isin(['Mestrado em Ciências da saúde','Ciência da Saúde','Ciências da Saúde']), 'Departamento'] = 'Ciência da Saúde'
pesquisadores.loc[pesquisadores['Departamento'].isin(['Mestrado em Ciências da saúde']), 'Departamento'] = 'Mestrado em Ciências da Saúde'
pesquisadores.loc[pesquisadores['Departamento'].isin(['Patologia Geral','Patologia']), 'Departamento'] = 'Patologia Geral'
pesquisadores.loc[pesquisadores['Departamento'].isin(['Departamento de Produtos Farmacêuticos','Produtos Farmacêuticos']), 'Departamento'] = 'Produtos Farmacêuticos'
pesquisadores.loc[pesquisadores['Departamento'].isin(['Setor de Patologia Clínica','Patologia Clínica']), 'Departamento'] = 'Patologia Clínica'
pesquisadores.loc[pesquisadores['Departamento'].isin(['Departamento de Medicina Veterinária Preventiva','Medicina Veterinária Preventiva']), 'Departamento'] = 'Medicina Veterinária Preventiva'
pesquisadores.loc[pesquisadores['Departamento'].isin(['Enfermagem Básica','Enfermagem']), 'Departamento'] = 'Enfermagem Básica'
pesquisadores.loc[pesquisadores['Departamento'].isin(['Faculdade de Física','Física']), 'Departamento'] = 'Física'
pesquisadores.loc[pesquisadores['Departamento'].isin(['Bioquímica e Imunologia','Bioquímica']), 'Departamento'] = 'Bioquímica e Imunologia'

## Normalizando nomes das unidades na coluna "Unidade" da tabela "pesquisadores"
pesquisadores.loc[pesquisadores['Unidade'].isin(['Instituto de Ciências Exatas','ICEX']), 'Unidade'] = 'Instituto de Ciências Exatas'
pesquisadores.loc[pesquisadores['Unidade'].isin(['Escola de veterinária','Escola de Veterinária']), 'Unidade'] = 'Escola de Veterinária'

# PARTE II: ANONIMIZAÇÃO
## Técnica de Anonimização: Mapeamento Consistente
### Aplicação nas chaves primária e estrangeira

# Gerar mapeamento consistente
mapping = {orig: f"ceua_{i:03d}" for i, orig in enumerate(ceua['COD_CEUA'].unique())}

# Aplicar na tabela pai (ceua)
ceua['id_ceua_pseud'] = ceua['COD_CEUA'].map(mapping)

# Aplicar na tabela filha ceua (mesmo mapping)
pedidos['id_ceua_pseud'] = pedidos['Protocolo na CEUA'].map(mapping)

#Parte II
## Anonimizando dados pessoais de pesquisadores e alunos

mapping_pesquisadores = {nome: f"pesquisador_{i:03d}" for i, nome in enumerate(ceua['Pesquisador'].drop_duplicates())}

# Aplicando mapping para criar colunas anonimizadas referente aos nomes dos pesquisadores
# Tabela pai (ceua)
ceua['Pesquisador'] = ceua['Pesquisador'].map(mapping_pesquisadores)

# Tabela filha (mesmo mapping!)
pedidos['Pesquisador'] = pedidos['Pesquisador'].map(mapping_pesquisadores)

# Tabela pesquisadores
pesquisadores['Pesquisador'] = pesquisadores['Pesquisador'].map(mapping_pesquisadores)

# Aplicando hashlib (SHA-256) para anonimizar nome dos alunos

def anonymize(value, salt="pedidos_alunos_22a25"):  # Não colocar o salt no portfólio para não codificarem a anonimização.
    if value is None:
        return None

    raw = f"{value}{salt}"
    return hashlib.sha256(raw.encode()).hexdigest()

# Anonimizando colunas com dados sensíveis

# Aplicando na tabela filha "pedidos"
pedidos["Responsável pela Retirada"] = pedidos["Responsável pela Retirada"].apply(anonymize)
# Aplicando na tabela "pesquisadores"
pesquisadores[["CPF do pesquisador","Ramal","E-mail"]] = pesquisadores[["CPF do pesquisador","Ramal","E-mail"]] .apply(anonymize)

### Retirando colunas com dados sensíveis que não foram anonimizadas

ceua_anon = ceua.drop(columns=['COD_CEUA','Protocolo na CEUA'])

pedidos_anon = pedidos.drop(columns=['Protocolo na CEUA'])


# Exportando as tabelas com os dados sensíveis anonimizados do formato dataframe Pandas para planilhas de excel (em abas diferentes).
with pd.ExcelWriter(r'C:/Users/Vicente JF/Documents/Projeto 1 _ Portfólio/dataset/dataset_biocen_anonimizado.xlsx') as dataset_biocen_anonimizado:
    ceua_anon.to_excel(dataset_biocen_anonimizado, sheet_name='tabela_ceua') # tabela pai anonimizada
    pedidos_anon.to_excel(dataset_biocen_anonimizado, sheet_name='tabela_pedidos') # tabela filha anonimizada
    pesquisadores.to_excel(dataset_biocen_anonimizado, sheet_name='tabela_pesquisadores')
    precos.to_excel(dataset_biocen_anonimizado, sheet_name='tabela_precos')