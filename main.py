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
df_prospects  = m.ler_json_candidaturas("/content/prospects.zip")

#########################################################################################
# TRATAMENTO DOS DADOS
#########################################################################################
#   PROSPECTS
#########################################################################################

# Removendo colunas que consideramos nao influenciar na analise
df_prospects.drop(columns=['nome', 'data_candidatura',
                           'recrutador', 'ultima_atualizacao',
                           'comentario', 'recrutador'], inplace=True)

print(df_prospects.head())

#########################################################################################
#   VAGAS
#########################################################################################

# Removendo colunas que consideramos nao influenciar na analise
df_vagas.drop(columns=['informacoes_basicas.data_requicisao', 'informacoes_basicas.limite_esperado_para_contratacao',
                       'informacoes_basicas.cliente', 'informacoes_basicas.solicitante_cliente',
                       'informacoes_basicas.empresa_divisao', 'informacoes_basicas.requisitante',
                       'informacoes_basicas.analista_responsavel','informacoes_basicas.superior_imediato',
                       'informacoes_basicas.telefone', 'perfil_vaga.demais_observacoes',
                       'informacoes_basicas.data_inicial', 'informacoes_basicas.data_final',
                       'informacoes_basicas.nome_substituto','informacoes_basicas.nome',
                       'informacoes_basicas.origem_vaga', 'perfil_vaga.principais_atividades',
                       'beneficios.valor_compra_1', 'beneficios.valor_compra_2',
                       'perfil_vaga.habilidades_comportamentais_necessarias', 'beneficios.valor_venda',
                       'perfil_vaga.competencia_tecnicas_e_comportamentais', 'perfil_vaga.horario_trabalho'
                       ], inplace=True)

# Preenchendo nan com o "padrao" das ja utilizado em outras linhas e padronizando demais casos
df_vagas['perfil_vaga.equipamentos_necessarios'] = df_vagas['perfil_vaga.equipamentos_necessarios'].fillna('Nenhum -')
df_vagas['perfil_vaga.equipamentos_necessarios'] = df_vagas['perfil_vaga.equipamentos_necessarios'].str \
  .replace('Outro - Nenhum -', 'Nenhum -') \
  .replace('Outro -', 'Nenhum -') \
  .replace('', 'Nenhum -')
  
# Extrair os valores numéricos usando regex para ter a faixa etaria de forma mais clara
# Proposta de uso, no cadastro do candidato podemos realizar um filtro da idade dele pela idade ofertada pelas vagas?
df_vagas[['idade_minima', 'idade_maxima']] = df_vagas['perfil_vaga.faixa_etaria'].str.extract(r'De:\s*(\d+)\s*Até:\s*(\d+)')
df_vagas['idade_minima'] = df_vagas['idade_minima'].fillna(18).astype(int)
df_vagas['idade_maxima'] = df_vagas['idade_maxima'].fillna(60).astype(int)

#########################################################################################
#   APPLICANTS
#########################################################################################

# Removendo colunas que consideramos nao influenciar na analise
df_applicants.drop(columns=['infos_basicas.telefone_recado', 'infos_basicas.telefone',
                            'infos_basicas.inserido_por', 'infos_basicas.email',
                            'infos_basicas.sabendo_de_nos_por', 'infos_basicas.nome',
                            'informacoes_pessoais.nome', 'informacoes_pessoais.cpf',
                            'informacoes_pessoais.fonte_indicacao', 'informacoes_pessoais.email',
                            'informacoes_pessoais.email_secundario', 'informacoes_pessoais.data_nascimento',
                            'informacoes_pessoais.telefone_celular',
                            'informacoes_pessoais.telefone_recado', 'informacoes_pessoais.sexo',
                            'informacoes_pessoais.estado_civil', 'informacoes_pessoais.pcd',
                            'informacoes_pessoais.endereco', 'informacoes_pessoais.skype',
                            'informacoes_pessoais.url_linkedin', 'informacoes_pessoais.facebook',
                            'formacao_e_idiomas.instituicao_ensino_superior', 'informacoes_pessoais.download_cv',
                            'cargo_atual.nome_superior_imediato','cargo_atual.email_superior_imediato',
                            'cv_pt', 'cv_en', 'formacao_e_idiomas.outro_curso'], inplace=True)
