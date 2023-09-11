# Como pegar dados em sites e automatizar a criação da carteira do nosso modelo.
# Construir um código que vá no fundamentus.com e busque dados de todos os indicadores da bolsa brasileira e gere a carteira selecionando as maiores ev_ebit e roic.
# Codigo baseado na bootcamp de 4 aulas das Varos, criando um modelo de investimento: https://www.youtube.com/@varos-programacao. 
# A tabela de resultados é salva em tabela.pickle. 

def pegarDadosEmSitesAutomatizarCriacaoCarteira():
    # Passo 2: Importar as bibliotecas
    import pickle
    from datetime import date

    # Lets check if we have already saved the table today, if it is de case, we get it from memory, otherwise we must do webscrapping
    # The table will be update every day
    with open('tabela.pickle', 'rb') as handle:
        tabela_dict_date = pickle.load(handle)
        today = date.today()
        d1 = today.strftime("%Y-%m-%d")
        print('d1: ', d1)
        if ('date' in tabela_dict_date and tabela_dict_date['date'] == d1):
            print("Getting table from memory")
            tabela_dict = tabela_dict_date["tabela_dict"]
            [print(record) for record in tabela_dict]
            return tabela_dict

    import sqlite3 # For SQLite database interaction
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.options import Options
    import pandas as pd

    # Passo 3: Entender como funcionam requisições na internet.
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    url = 'https://www.fundamentus.com.br/resultado.php'

    driver.get(url)

    # Passo 6 - Ler a tabela de dados.
    local_tabela = '/html/body/div[1]/div[2]/table'

    elemento = driver.find_element("xpath", local_tabela)

    html_tabela = elemento.get_attribute('outerHTML')

    tabela = pd.read_html(str(html_tabela), thousands = '.', decimal = ',')[0]


    tabela = tabela.set_index("Papel")

    # Tratando erros
    print("Columns names before: ", tabela.columns.values)
    if ("Cotaï¿½ï¿½o" in list(tabela.columns.values)):
        tabela = tabela.rename({'Cotaï¿½ï¿½o': 'Cotação'}, axis=1)
    print("Columns names after: ", tabela.columns.values)
    
    tabela = tabela[['Cotação', 'EV/EBIT', 'ROIC', 'Liq.2meses']]

    # Passo 7 - Construir a tabela final

    tabela.info()

    # Temos que transformar o texto em números
    tabela['ROIC'] = tabela['ROIC'].str.replace("%", "")
    tabela['ROIC'] = tabela['ROIC'].str.replace(".", "")
    tabela['ROIC'] = tabela['ROIC'].str.replace(",", ".")
    tabela['ROIC'] = tabela['ROIC'].astype(float)



    # Passo 7.3: Fazendo os filtros e criando os rankings

    tabela = tabela[tabela['Liq.2meses'] > 1000000]

    tabela = tabela[tabela['EV/EBIT'] > 0]
    tabela = tabela[tabela['ROIC'] > 0]

    tabela['ranking_ev_ebit'] = tabela['EV/EBIT'].rank(ascending = True)
    tabela['ranking_roic'] = tabela['ROIC'].rank(ascending = False)
    tabela['ranking_total'] = tabela['ranking_ev_ebit'] + tabela['ranking_roic']

    tabela = tabela.sort_values('ranking_total')

    tabela = tabela.reset_index()

    print(tabela.head(10))

    tabela_dict = tabela.iloc[:30].to_dict(orient = 'records')


    # Save in memory so we dont need to webscrapping every time we call this function, only once a day
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    print('d1: ', d1)
    tabela_dict_date = {'tabela_dict': tabela_dict, 'date': d1}
    with open('tabela.pickle', 'wb') as handle:
        pickle.dump(tabela_dict_date, handle, protocol=pickle.HIGHEST_PROTOCOL)


    [print(record) for record in tabela_dict]

    return tabela_dict


if __name__ == "__main__":

    pegarDadosEmSitesAutomatizarCriacaoCarteira()
    