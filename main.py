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
                           'comentario', 'recrutador'], inplace=True)

#########################################################################################
#   VAGAS
#########################################################################################

# Removendo colunas que consideramos nao influenciar na analise
df_vagas = m.remover_colunas(df_vagas, 
                             ['informacoes_basicas.titulo_vaga', 'informacoes_basicas.cliente'], 
                             'informacoes_basicas\.')

# df_vagas.drop(columns=[
#                        'informacoes_basicas.telefone', 'perfil_vaga.demais_observacoes',
#                        'perfil_vaga.principais_atividades',
#                        'perfil_vaga.regiao',
#                        'beneficios.valor_compra_1', 'beneficios.valor_compra_2',
#                        'perfil_vaga.habilidades_comportamentais_necessarias', 'beneficios.valor_venda',
#                        'perfil_vaga.competencia_tecnicas_e_comportamentais', 'perfil_vaga.horario_trabalho',
#                        'perfil_vaga.local_trabalho', 'perfil_vaga.bairro', 'perfil_vaga.faixa_etaria',
#                        'perfil_vaga.pais', 'perfil_vaga.estado', 'perfil_vaga.cidade'
#                        ], inplace=True)

# Preenchendo nan com o "padrao" das ja utilizado em outras linhas e padronizando demais casos
df_vagas['perfil_vaga.equipamentos_necessarios'] = df_vagas['perfil_vaga.equipamentos_necessarios'].fillna('Nenhum -')
df_vagas['perfil_vaga.equipamentos_necessarios'] = df_vagas['perfil_vaga.equipamentos_necessarios'].str \
  .replace('Outro - Nenhum -', 'Nenhum -') \
  .replace('Outro -', 'Nenhum -') \
  .replace('', 'Nenhum -')
  
  
print('\n\ncolunas: ', df_vagas.columns)
print('\n\nvagas: ', df_vagas.shape)

#########################################################################################
#   APPLICANTS
#########################################################################################

# Removendo colunas que consideramos nao influenciar na analise
df_applicants = m.remover_colunas(df_applicants, [], 'infos_basicas\.|informacoes_pessoais\.|cargo_atual\.')

df_applicants.drop(columns=['cv_pt', 'cv_en',
                            'informacoes_profissionais.remuneracao','informacoes_profissionais.area_atuacao',
                            'informacoes_profissionais.outras_certificacoes','informacoes_profissionais.experiencias',
                            'formacao_e_idiomas.ano_conclusao', 'formacao_e_idiomas.outro_curso'
                             ], inplace=True)

print('candidatos: ', df_applicants.shape)

#m.exibir_head_df('CANDIDATOS', df_applicants)
#m.exibir_head_df('VAGAS', df_vagas)
#m.exibir_head_df('CANDIDATURA', df_prospects)
