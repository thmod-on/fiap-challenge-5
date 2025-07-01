#########################################################################################
# IMPORTS
#########################################################################################

import metodos as m
import pandas as pd

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
col_applicants_manter = ['informacoes_pessoais.pcd', 'informacoes_profissionais.titulo_profissional',
                         'informacoes_profissionais.area_atuacao', 'informacoes_profissionais.nivel_profissional',
                         'informacoes_profissionais.remuneracao']
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
#   TREINANDO O MODELO
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
df_merge = df_merge[~df_merge['situacao_candidato'].isin(lst_situacoes_remover)]
df_merge['aprovado'] = df_merge['situacao_candidato'].isin(lst_situacoes_aprovado).astype(int)

print(df_merge[['situacao_candidato','aprovado']].head(10))