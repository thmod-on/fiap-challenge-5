import zipfile
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

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

def remover_colunas(df, lst_colunas_manter, str_colunas_apagar):
    """Metodo para remover dinamicamente um conjunto de colunas de um df seguindo um padrao e deixando outras deste mesmo padrao

    Args:
        df (dataframe): dataframe que terá as colunas removidas
        lst_colunas_manter ([string]): lista de strings contendo as colunas que devem ser mantidas
        str_colunas_apagar (string): expressao regular contendo as colunas a serem apagadas

    Returns:
        dataframe: dataframe inicial apos a remocao das colunas solicitadas
    """
    col_apagar = df.columns[df.columns.str.contains(str_colunas_apagar)]
    col_apagar_final = [coluna for coluna in col_apagar if coluna not in lst_colunas_manter]
    df = df.drop(columns=col_apagar_final)
    return df

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
    print(df.head(10))
    
def treinar_random_forest(df, lst_colunas, col_target, descricao):
    X = df[lst_colunas]
    y = df[col_target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)

    y_pred = modelo_rf.predict(X_test)

    print('\n\nRandomForest usando ',descricao)
    print('Acurácia:', accuracy_score(y_test, y_pred))
    print('\nRelatório de Classificação:\n', classification_report(y_test, y_pred))
    
    # import pandas as pd
    # import matplotlib.pyplot as plt

    # importancias = pd.Series(modelo_rf.feature_importances_, index=lst_colunas)
    # importancias.sort_values().plot(kind='barh')
    # plt.title('Importância das Variáveis')
    # plt.show()
