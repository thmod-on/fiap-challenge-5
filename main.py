#########################################################################################
# IMPORTS
#########################################################################################

import metodos as m
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OrdinalEncoder


#########################################################################################
# CARGA DOS DADOS
#########################################################################################

path_applicants = 'dados\\applicants.zip'
path_vagas = 'dados\\vagas.zip'
path_prospects = 'dados\\prospects.zip'

df_applicants = m.ler_json(path_applicants)
df_vagas      = m.ler_json(path_vagas)
df_prospects  = m.ler_json_candidaturas(path_prospects)

#########################################################################################
# TRATAMENTO DOS DADOS
#########################################################################################
#   PROSPECTS
#########################################################################################

# Removendo colunas que consideramos nao influenciar na analise
df_prospects.drop(columns=['nome', 'data_candidatura',
                           'recrutador', 'ultima_atualizacao',
                           'comentario', 'recrutador', 'titulo_vaga'
                           ], inplace=True)

#########################################################################################
#   VAGAS
#########################################################################################

# Removendo colunas que consideramos nao influenciar na analise
col_vagas_manter = ['informacoes_basicas.titulo_vaga', 'informacoes_basicas.tipo_contratacao',
                    'perfil_vaga.vaga_especifica_para_pcd', 'perfil_vaga.nivel profissional',
                    'perfil_vaga.nivel_academico', 'perfil_vaga.nivel_ingles', 'perfil_vaga.nivel_espanhol',
                    'perfil_vaga.outro_idioma', 'perfil_vaga.areas_atuacao']
df_vagas = m.remover_colunas(df_vagas,
                           col_vagas_manter,
                           'informacoes_basicas\.|perfil_vaga\.|beneficios\.')

# Padronizando os dados 'vazios'
df_vagas['perfil_vaga.vaga_especifica_para_pcd'] = df_vagas['perfil_vaga.vaga_especifica_para_pcd'].replace('', 'Não')
df_vagas['perfil_vaga.nivel_espanhol'] = df_vagas['perfil_vaga.nivel_espanhol'].replace('', 'Nenhum')
df_vagas['perfil_vaga.outro_idioma'] = df_vagas['perfil_vaga.outro_idioma'].replace('', 'Nenhum').str.replace(' - ',' ') 
  
#########################################################################################
#   APPLICANTS
#########################################################################################

# Removendo colunas que consideramos nao influenciar na analise
col_applicants_manter = ['informacoes_pessoais.pcd', 'informacoes_profissionais.titulo_profissional']
df_applicants = m.remover_colunas(df_applicants,
                                col_applicants_manter,
                                'infos_basicas\.|informacoes_pessoais\.|informacoes_profissionais\.|cargo_atual\.|formacao_e_idiomas.instituicao_ensino_superior|formacao_e_idiomas.cursos')

df_applicants.drop(columns=['cv_pt', 'cv_en',
                            'formacao_e_idiomas.ano_conclusao', 'formacao_e_idiomas.outro_curso'
                             ], inplace=True)

# Padronizando os dados 'vazios'
df_applicants['informacoes_pessoais.pcd'] = df_applicants['informacoes_pessoais.pcd'].replace('', 'Não')
df_applicants['formacao_e_idiomas.outro_idioma'] = df_applicants['formacao_e_idiomas.outro_idioma']. \
  replace('-', 'Nenhum'). \
  replace('Português -', 'Nenhum'). \
  replace('Alemão - Nenhum', 'Nenhum'). \
  replace('Japonês - Nenhum	', 'Nenhum'). \
  str.replace(' -', '')
df_applicants['formacao_e_idiomas.nivel_ingles'] = df_applicants['formacao_e_idiomas.nivel_ingles'].replace('', 'Nenhum')
df_applicants['formacao_e_idiomas.nivel_espanhol'] = df_applicants['formacao_e_idiomas.nivel_espanhol'].replace('', 'Nenhum')
df_applicants['formacao_e_idiomas.nivel_academico'] = df_applicants['formacao_e_idiomas.nivel_academico'].replace('', 'Não informado')
df_applicants['informacoes_profissionais.titulo_profissional'] = df_applicants['informacoes_profissionais.titulo_profissional'].replace('', 'Nenhum')

#########################################################################################
#   UNIFICANDO O MODELO
#########################################################################################

# Unindo os cadidatos as vagas atraves de suas candidaturas
df_merge = pd. \
  merge(df_prospects, df_vagas, left_on='codigo_vaga', right_on='ID', how='inner'). \
  merge(df_applicants, left_on='codigo_candidato', right_on='ID', how='inner')

# Tratando os dados a serem utilizados como 'target'
lst_situacoes_aprovado = ['Encaminhado ao Requisitante',
  'Contratado pela Decision', 'Entrevista com Cliente', 'Em avaliação pelo RH',
  'Aprovado', 'Contratado como Hunting', 'Proposta Aceita','Encaminhar Proposta']
lst_situacoes_reprovado = ['Prospect', 'Não Aprovado pelo Cliente','Não Aprovado pelo RH',
  'Não Aprovado pelo Requisitante','Desistiu da Contratação']
lst_situacoes_remover = ['Inscrito', 'Desistiu', 'Entrevista Técnica',
  'Sem interesse nesta vaga', 'Documentação PJ','Documentação CLT',
  'Documentação Cooperado','Recusado']

# Removendo as linhas com dados irrelevantes na coluna target
df_merge = df_merge[~df_merge['situacao_candidato'].isin(lst_situacoes_remover)].copy()
df_merge.loc[:, 'aprovado'] = df_merge['situacao_candidato'].isin(lst_situacoes_aprovado).astype(int)



#########################################################################################
#   MATRIZ DE CALOR
#########################################################################################


# Lista das colunas categóricas a serem transformadas
colunas_categoricas = [
    #'situacao_candidato',
    #'informacoes_basicas.titulo_vaga',
    'perfil_vaga.vaga_especifica_para_pcd',
    'perfil_vaga.nivel profissional',
    'perfil_vaga.nivel_academico',
    'perfil_vaga.nivel_ingles',
    'perfil_vaga.nivel_espanhol',
    'perfil_vaga.outro_idioma',
    'informacoes_pessoais.pcd',
    #'informacoes_profissionais.titulo_profissional',
    'formacao_e_idiomas.nivel_academico',
    'formacao_e_idiomas.nivel_ingles',
    'formacao_e_idiomas.nivel_espanhol',
    'formacao_e_idiomas.outro_idioma'
]

df_merge_ordinal = df_merge.copy()

# Aplicar o OrdinalEncoder nas colunas desejadas
encoder = OrdinalEncoder()
df_merge_ordinal[colunas_categoricas] = encoder.fit_transform(df_merge_ordinal[colunas_categoricas])

# Calcula a matriz de correlação (numeric_only ignora objetos)
corr = df_merge_ordinal.corr(numeric_only=True)

# Limiar mínimo de correlação. Iremos analisar apenas aqueles que estiverem acima deste limiar
limiar = 0.5

# Cria uma máscara booleana onde as correlações absolutas são maiores que o limiar (sem a diagonal)
mascara = (corr.abs() > limiar) & (corr.abs() < 1.0)

# Seleciona as colunas que têm pelo menos uma correlação forte
colunas_correlacionadas = mascara.any()[mascara.any()].index

# Submatriz com apenas colunas correlacionadas
sub_corr = corr.loc[colunas_correlacionadas, colunas_correlacionadas]

# Plot
# plt.figure(figsize=(12, 6))
# sns.heatmap(sub_corr, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f")
# plt.title(f'Heatmap de Correlações (>|{limiar}|)')
# plt.xticks(rotation=45)
# plt.show()


# colunas escolhidas segundo a matriz de calor do passo anterior
colunas_aprendizado = ['perfil_vaga.nivel_espanhol', 'perfil_vaga.nivel profissional', 
                       'formacao_e_idiomas.nivel_ingles', 'formacao_e_idiomas.nivel_espanhol',
                       'formacao_e_idiomas.nivel_academico']

#########################################################################################
#   TREINANDO O MODELO - RANDOMFOREST
#########################################################################################

df_resultados = pd.DataFrame(columns=['modelo', 'acuracia', 'f1_score'])

df_resultados = m.treinar_random_forest(df_merge_ordinal, colunas_aprendizado, 'aprovado', 'colunas que selecionamos pelo heatmap', df_resultados)
df_resultados = m.treinar_random_forest(df_merge_ordinal, colunas_categoricas, 'aprovado', 'colunas que selecionamos por análise', df_resultados)

#########################################################################################
#   TREINANDO O MODELO - XGBOOST
#########################################################################################

df_resultados = m.treinar_xgboost(df_merge_ordinal, colunas_aprendizado, 'aprovado', 'colunas que selecionamos pelo heatmap', df_resultados)
df_resultados = m.treinar_xgboost(df_merge_ordinal, colunas_categoricas, 'aprovado', 'colunas que selecionamos por análise', df_resultados)

#########################################################################################
#   TREINANDO O MODELO - LOGISTIC REGRESSION
#########################################################################################

df_resultados = m.treinar_log_regression(df_merge_ordinal, colunas_aprendizado, 'aprovado', 'colunas que selecionamos pelo heatmap', df_resultados)
df_resultados = m.treinar_log_regression(df_merge_ordinal, colunas_categoricas, 'aprovado', 'colunas que selecionamos por análise', df_resultados)

#########################################################################################
#   TREINANDO O MODELO - KNN
#########################################################################################

df_resultados = m.treinar_knn(df_merge_ordinal, colunas_aprendizado, 'aprovado', 'colunas que selecionamos pelo heatmap', df_resultados)
df_resultados = m.treinar_knn(df_merge_ordinal, colunas_categoricas, 'aprovado', 'colunas que selecionamos por análise', df_resultados)



print('\n\ncompilado:\n', df_resultados.sort_values(by='acuracia', ascending=False))