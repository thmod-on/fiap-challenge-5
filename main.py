import metodos as m
import pandas as pd

path_applicants = 'dados\\applicants.zip'
path_vagas = 'dados\\vagas.zip'
path_prospects = 'dados\\prospects.zip'

df_applicants = m.ler_json(path_applicants)
df_vagas = m.ler_json(path_vagas)
df_prospects = m.ler_json(path_prospects)

print(df_applicants.head())
print(df_vagas.head())

# Precisa de ajuste na leitura deste json
print(df_prospects.head())