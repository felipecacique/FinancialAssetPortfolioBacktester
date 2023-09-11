# Backtest modelo de investimento Magic Formula.
# Testar se a regra de investimento da fórmula mágica, do Joel Grenblatt, funcionou no Brasil nos últimos anos.
# Codigo baseado na bootcamp de 4 aulas das Varos, criando um modelo de investimento: https://www.youtube.com/@varos-programacao. 
# Estamos tambem utilizando o dataset dados_empresas.csv fornecido gratuitamente por eles.

def criandoUmModeloDeInvestimento(params):
    print(params)
    # Passo 1: Importando os módulos necessários
    import pandas as pd
    # import quantstats as qs 

    # Passo 2: Baixar os dados dispobinilizados.
    dados_empresas = pd.read_csv("dados_empresas.csv")
    dados_empresas

    # Passo 3: Filtrar liquidez.
    dados_empresas = dados_empresas[dados_empresas['volume_negociado'] > params['liquidezMin']]
    dados_empresas

    # Passo 4: Calcula os retornos mensais das empresas.
    dados_empresas['retorno'] = dados_empresas.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
    dados_empresas

    dados_empresas['retorno'] = dados_empresas.groupby('ticker')['retorno'].shift(-1) 
    dados_empresas

    # Passo 5: Cria o ranking dos indicadores.
    dados_empresas['data'].unique()

    dados_empresas['ranking_ev_ebit'] = dados_empresas.groupby('data')['ebit_ev'].rank(ascending = False)
    dados_empresas

    dados_empresas[dados_empresas['data'] == '2016-01-31'].sort_values('ranking_ev_ebit')

    dados_empresas['ranking_roic'] = dados_empresas.groupby('data')['roic'].rank(ascending = False)
    dados_empresas

    dados_empresas[dados_empresas['data'] == '2016-01-31'].sort_values('ranking_roic')

    # teste - vamos incluir a variacao do preco do ultimo mes e ver como fica o resultado
    dados_empresas['retorno_passado'] = dados_empresas.groupby('ticker')['preco_fechamento_ajustado'].pct_change()
    dados_empresas['retorno_passado'] = dados_empresas['retorno_passado'].fillna(0) 
    dados_empresas['ranking_retorno_passado'] = dados_empresas.groupby('data')['retorno_passado'].rank(ascending = False) # pega os que mais cairam no ultimo mes
    dados_empresas[dados_empresas['data'] == '2016-01-31'].sort_values('retorno_passado')

    from random import random
    dados_empresas['ranking_random'] = list([random() for i in list(dados_empresas['retorno_passado'])])

    dados_empresas['ranking_final'] = params['fatorEvEbit'] * dados_empresas['ranking_ev_ebit'] + params['fatorRoic'] * dados_empresas['ranking_roic'] + params['fatorRetornoMensal'] * dados_empresas['ranking_retorno_passado'] 
    dados_empresas['ranking_final'] = dados_empresas.groupby('data')['ranking_final'].rank()

    dados_empresas[dados_empresas['data'] == '2016-02-29'].sort_values('ranking_final').head(20)


    # Passo 6: Cria as carteiras. 
    dados_empresas = dados_empresas[dados_empresas['ranking_final'] <= params['rankingQtd']]

    dados_empresas[dados_empresas['data'] == '2016-01-31'].head(20)


    # Passo 7: Calcula a rentabilidade por carteira.
    rentabilidade_por_carteiras = dados_empresas.groupby('data')['retorno'].mean()
    rentabilidade_por_carteiras = rentabilidade_por_carteiras.to_frame()


    # Passo 8: Calcula a rentabilidade do modelo.
    rentabilidade_por_carteiras['modelo'] = (rentabilidade_por_carteiras['retorno'] + 1).cumprod() - 1
    # rentabilidade_por_carteiras['modelo'] = rentabilidade_por_carteiras['retorno'].cumsum()

    rentabilidade_por_carteiras = rentabilidade_por_carteiras.shift(1)
    rentabilidade_por_carteiras = rentabilidade_por_carteiras.dropna()


    # Passo 9: Calcula a rentabilidade do ibovespa no mesmo período.
    ibov = pd.read_csv('ibov.csv')

    retornos_ibov = ibov['fechamento'].pct_change().dropna()
    retorno_acum_ibov = (1 + retornos_ibov).cumprod() - 1
    rentabilidade_por_carteiras['ibovespa'] = retorno_acum_ibov.values
    rentabilidade_por_carteiras = rentabilidade_por_carteiras.drop('retorno', axis = 1)


    # Passo 10: Analisa os resultados. 
    # qs.extend_pandas()
    rentabilidade_por_carteiras['datas'] = rentabilidade_por_carteiras.index
    rentabilidade_por_carteiras.index = pd.to_datetime(rentabilidade_por_carteiras.index)

    # rentabilidade_por_carteiras['modelo'].plot_monthly_heatmap()
    # rentabilidade_por_carteiras['ibovespa'].plot_monthly_heatmap()

    rentabilidade_por_carteiras.plot()

    rentabilidade_ao_ano = (1 + rentabilidade_por_carteiras.loc['2023-06-30', 'modelo']) ** (1/7.5) - 1

    print(rentabilidade_ao_ano)

    resultado = {
        'rentabilidadeAoAnoModelo': rentabilidade_ao_ano,
        'rentabilidadeAoAnoIbovespa': rentabilidade_ao_ano,
        'timeSeriesData': {
            'labels': rentabilidade_por_carteiras.datas.to_list(),
            'datasets': [
                {
                    'label': 'modelo',
                    'data': rentabilidade_por_carteiras['modelo'].to_list()
                },
                            {
                    'label': 'ibovespa',
                    'data': rentabilidade_por_carteiras['ibovespa'].to_list()
                }
            ],
        }, 
    }

    return resultado

if __name__ == "__main__":
    # Prametros default para teste da funcao
    params = {
        "liquidezMin": 1000000,
        "fatorEvEbit": 1,
        "fatorRoic": 1,
        "fatorRetornoMensal": 1,
        "rankingQtd": 10
    }
    criandoUmModeloDeInvestimento(params)
