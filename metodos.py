import zipfile
import json
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score
from xgboost import XGBClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

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
 
def separar_treino_teste(df, lst_colunas, col_target): 
    """Metodo para separar os dados a serem usados para treino e teste

    Args:
        df (dataFrame): dataFrame com dados a serem estudados
        lst_colunas (list): lista de colunas existentes no df que seram utilizadas no treino
        col_target (string): nome da coluna existente no df que sera nosso target

    Returns:
        _type_: dados de treino e teste para os modelos
    """
    X = df[lst_colunas]
    y = df[col_target]
    
    return train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
def treinar_random_forest(df, lst_colunas, col_target, descricao, df_resultados):
    """Metodo para realizar o treinamento randomForest

    Args:
        df (dataFrame): dataFrame com dados a serem estudados
        lst_colunas (list): lista de colunas existentes no df que seram utilizadas no treino
        col_target (string): nome da coluna existente no df que sera nosso target
        descricao (string): informacao a ser utilizada para distinguir mais de uma chamada ao memo modelo
        df_resultados (dataFrame): dataframe utilizado para guardar os resultados dos treinamentos

    Returns:
        dataFrame: Ao final sera retornado o dataFrame com os dados dos treinamentos de cada modelo
    """
    X_train, X_test, y_train, y_test = separar_treino_teste(df, lst_colunas, col_target)

    modelo_rf = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo_rf.fit(X_train, y_train)
    y_pred = modelo_rf.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='binary')
    modelo = 'RandomForest ' + descricao
    
    return atualizar_resultados(df_resultados, modelo, acc, f1)

def treinar_xgboost(df, lst_colunas, col_target, descricao, df_resultados):
    """Metodo para realizar o treinamento XGBOOST

    Args:
        df (dataFrame): dataFrame com dados a serem estudados
        lst_colunas (list): lista de colunas existentes no df que seram utilizadas no treino
        col_target (string): nome da coluna existente no df que sera nosso target
        descricao (string): informacao a ser utilizada para distinguir mais de uma chamada ao memo modelo
        df_resultados (dataFrame): dataframe utilizado para guardar os resultados dos treinamentos

    Returns:
        dataFrame: Ao final sera retornado o dataFrame com os dados dos treinamentos de cada modelo
    """
    X_train, X_test, y_train, y_test = separar_treino_teste(df, lst_colunas, col_target)
    
    modelo_xgb = XGBClassifier(random_state=42)
    modelo_xgb.fit(X_train, y_train)
    y_pred = modelo_xgb.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='binary')
    modelo = 'XGBOOST ' + descricao
    
    return atualizar_resultados(df_resultados, modelo, acc, f1)
    
def treinar_log_regression(df, lst_colunas, col_target, descricao, df_resultados):
    """Metodo para realizar o treinamento Logistic Regression

    Args:
        df (dataFrame): dataFrame com dados a serem estudados
        lst_colunas (list): lista de colunas existentes no df que seram utilizadas no treino
        col_target (string): nome da coluna existente no df que sera nosso target
        descricao (string): informacao a ser utilizada para distinguir mais de uma chamada ao memo modelo
        df_resultados (dataFrame): dataframe utilizado para guardar os resultados dos treinamentos

    Returns:
        dataFrame: Ao final sera retornado o dataFrame com os dados dos treinamentos de cada modelo
    """
    X_train, X_test, y_train, y_test = separar_treino_teste(df, lst_colunas, col_target)
    
    modelo_log = LogisticRegression(max_iter=1000)
    modelo_log.fit(X_train, y_train)
    y_pred = modelo_log.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='binary')
    modelo = 'LogisticRegression ' + descricao
    
    return atualizar_resultados(df_resultados, modelo, acc, f1)

def treinar_knn(df, lst_colunas, col_target, descricao, df_resultados):
    """Metodo para realizar o treinamento KNN

    Args:
        df (dataFrame): dataFrame com dados a serem estudados
        lst_colunas (list): lista de colunas existentes no df que seram utilizadas no treino
        col_target (string): nome da coluna existente no df que sera nosso target
        descricao (string): informacao a ser utilizada para distinguir mais de uma chamada ao memo modelo
        df_resultados (dataFrame): dataframe utilizado para guardar os resultados dos treinamentos

    Returns:
        dataFrame: Ao final sera retornado o dataFrame com os dados dos treinamentos de cada modelo
    """
    X_train, X_test, y_train, y_test = separar_treino_teste(df, lst_colunas, col_target)
    
    modelo_knn = KNeighborsClassifier(n_neighbors=5)
    modelo_knn.fit(X_train, y_train)
    y_pred = modelo_knn.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='binary')
    modelo = 'KNN ' + descricao
    
    return atualizar_resultados(df_resultados, modelo, acc, f1)

def atualizar_resultados(df, modelo, acuracia, f1):
    df.loc[len(df)] = [modelo, acuracia, f1]
    return df