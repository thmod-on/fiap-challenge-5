import zipfile
import json
import pandas as pd

def ler_json(caminho_zip):
    """Metodo criado para ler um arquivo .json que esteja dentro de um .zip
    Estrutura do json deve ser chave -> elemento - > valor 
    ou 
    chave -> categoria -> elemento -> valor

    Args:
        caminho_zip (string): caminho onde está o arquivo .zip

    Returns:
        dataframe: o json sera achatado para retornar um dataframe correspondente, 
        concatenando a categoria.elemento quando necessário
    """
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        nome_arquivo_json = zip_ref.namelist()[0]  # assumindo que só há um arquivo no zip
        with zip_ref.open(nome_arquivo_json) as file:
            dados = json.load(file)

    # Achatar os dados
    linhas = []
    for chave, conteudo in dados.items():
        linha = {"ID": chave}
        # Flatten (achatar) cada subnível com prefixo
        for secao, valores in conteudo.items():
            if isinstance(valores, dict):
                for subchave, subvalor in valores.items():
                    linha[f"{secao}.{subchave}"] = subvalor
            else:
                linha[secao] = valores
        linhas.append(linha)

    # Criar o DataFrame
    df = pd.DataFrame(linhas)
    return df


def ler_json_candidaturas(caminho_zip):
    """Similar ao metodo ler_json, porem, contemplando uma lista de elementos dentro 
    de uma categoria

    Args:
        caminho_zip (string): caminho onde está o arquivo .zip

    Returns:
        dataframe: o json sera achatado para retornar um dataframe correspondente, 
        concatenando a categoria.elemento quando necessário.
        Para o caso de uma lista de elementos, cada um vai gerar uma nova linha para a
        mesma chave inicial
    """
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        nome_arquivo_json = zip_ref.namelist()[0]  # assumindo que só há um arquivo no zip
        with zip_ref.open(nome_arquivo_json) as file:
            dados_candidatura = json.load(file)

    linhas_candidatura = []

    for codigo_vaga, conteudo in dados_candidatura.items():
        prospects = conteudo.get("prospects")

        # Verifica se há prospects e se é uma lista com itens
        if isinstance(prospects, list) and prospects:
            for prospect in prospects:
                linha_candidatura = {
                    'codigo_vaga': codigo_vaga,
                    'titulo_vaga': conteudo.get('titulo', ''),
                    'nome': prospect.get('nome', ''),
                    'codigo_candidato': prospect.get('codigo', ''),
                    'situacao_candidato': prospect.get('situacao_candidado', ''),
                    'data_candidatura': prospect.get('data_candidatura', ''),
                    'ultima_atualizacao': prospect.get('ultima_atualizacao', ''),
                    'comentario': prospect.get('comentario', ''),
                    'recrutador': prospect.get('recrutador', '')
                }
                linhas_candidatura.append(linha_candidatura)

    # Criar o DataFrame final
    df_candidaturas = pd.DataFrame(linhas_candidatura)
    return df_candidaturas

def exibir_head_df(nome_tabela, df):
    """Metodo para acompanhamento de dataframes

    Args:
        nome_tabela (string): nome a ser exibido no 'cabecalho'
        df (dataframe): dataframe a ser exibido
    """
    tabela = nome_tabela
    print('\n','-'*(len(tabela)+6))
    print('| ', tabela, ' |')
    print('-'*(len(tabela)+6))
    print(df.head(2))