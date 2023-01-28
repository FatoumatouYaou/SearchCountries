import streamlit as s
import pandas as pd
import plotly.express as px
import mysql.connector
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd
import streamlit
import urllib.request
import json
import os
import ssl

from plotly.subplots import make_subplots

try:
    mydb = connection = mysql.connector.connect(host='localhost',
                                                database='base',
                                                user='root',
                                                password='')
    query = "SELECT * FROM sortant"
    result_dataFrame = pd.read_sql(query, mydb)
    mydb.close()
except Exception as e:
    mydb.close()
    print(str(e))
df_s = result_dataFrame

try:
    mydb = connection = mysql.connector.connect(host='localhost',
                                                database='base',
                                                user='root',
                                                password='')
    query = "SELECT * FROM metier"
    result_dataFrame = pd.read_sql(query, mydb)
    mydb.close()
except Exception as e:
    mydb.close()
    print(str(e))
df_m = result_dataFrame

try:
    mydb = connection = mysql.connector.connect(host='localhost',
                                                database='base',
                                                user='root',
                                                password='')
    query = "SELECT * FROM secteur"
    result_dataFrame = pd.read_sql(query, mydb)
    mydb.close()
except Exception as e:
    mydb.close()
    print(str(e))
df_sec = result_dataFrame

try:
    mydb = connection = mysql.connector.connect(host='localhost',
                                                database='base',
                                                user='root',
                                                password='')
    query = "SELECT * FROM residence"
    result_dataFrame = pd.read_sql(query, mydb)
    mydb.close()
except Exception as e:
    mydb.close()
    print(str(e))
df_r = result_dataFrame

try:
    mydb = connection = mysql.connector.connect(host='localhost',
                                                database='base',
                                                user='root',
                                                password='')
    query = "SELECT * FROM commune"
    result_dataFrame = pd.read_sql(query, mydb)
    mydb.close()
except Exception as e:
    mydb.close()
    print(str(e))
df_com = result_dataFrame

try:
    mydb = connection = mysql.connector.connect(host='localhost',
                                                database='base',
                                                user='root',
                                                password='')
    query = "SELECT * FROM reponses"
    result_dataFrame = pd.read_sql(query, mydb)
    mydb.close()
except Exception as e:
    mydb.close()
    print(str(e))
df_resp = result_dataFrame
df_rep = result_dataFrame

try:
    mydb = connection = mysql.connector.connect(host='localhost',
                                                database='base',
                                                user='root',
                                                password='')
    query = "SELECT * FROM questions"
    result_dataFrame = pd.read_sql(query, mydb)
    mydb.close()
except Exception as e:
    mydb.close()
    print(str(e))
df_quest = result_dataFrame

# fusion sortant metier(id_sortant id_metier)
dfsm = pd.merge(df_s, df_m, on='id_metier', how='left')

# fusion dfsm er secteur(id_secteur)
dfsm_sec = pd.merge(dfsm, df_sec, on='id_secteur', how='left')

# fusion précédent et residence(id_residence)
dfsm_sec_res = pd.merge(dfsm_sec, df_r, on='id_residence', how='left')

# fusion précédent et commune(id_commune)
dfsm_sec_res_com = pd.merge(dfsm_sec_res, df_com, on='id_commune', how='left')

# fusion précédent et reponse(id_sortant)
df_fin = dfsm_sec_res_com
df = df_fin


def main():
    # s.title("Auteur Aziz")
    # s.write("# Tableau de bord des sortants de formation professionelle au Niger")
    #  with s.sidebar:
    #     s.subheader('Apropos')
    #     s.markdown(
    #         'Bienvennue sur cette page vous allez retrouver des **statisques** et **graphiques**')
    # s.sidebar.image(
    #     'https://streamlit.io/images/brand/streamlit-mark-color.png', width=100)

    # s.markdown('''
    #     Il s'agit d'un tableau de bord montrant les *Statistiques* de différents types de :Formation professionelle suivis par les sortans
    #      ''')
    # s.header('')

    # fonction d'import de dataset
    # affiche data
    # df = result_dataFrame
    #df_sample = df
    # s.write(df_sample)
    s.header('Statistiques récapitulatives')
    stats = df_fin.groupby('id_sortant')['sexe'].agg(
        [('nombre', 'value_counts')]).reset_index()
    stats = stats.groupby('sexe')['nombre'].agg(
        [('index', 'value_counts')]).reset_index()
    stats['aziz'] = stats['index']

    stat1 = df.groupby('nom_metier')[
        'id_metier'].agg([('nombre', 'value_counts')])
    stat2 = df.groupby('quartier')[
        'id_residence'].agg([('nombre', 'value_counts')])
    # s.dataframe(stats)
    # s.dataframe(stat1)
    # s.dataframe(stat2)

    # line_fig = px.line(df[df['sexe'] == 'H'],
    #                    x='date_naiss', y='id_sortant',
    #                    title='Representation')
    # s.plotly_chart(line_fig)
    fig1 = go.Figure(data=[go.Histogram(
        y=df["sexe"], name="count", texttemplate="%{x}", textfont_size=20)])

    # s.plotly_chart(fig)
    d = df_resp.groupby('reponse')["id_sortant"].agg(
        [("Nombre", "count")]).reset_index()
    # fusion précédent et commune(id_commune)
    dfsm_quest_rep = pd.merge(df_rep, df_quest, on='id_question', how='left')
    df_id_quest = dfsm_quest_rep.loc[(dfsm_quest_rep['id_question'] == 26) | (
        dfsm_quest_rep['id_question'] == 11)]
    df_id_quest = df_id_quest.groupby('designation')['reponse'].agg(
        [('Nombre', 'value_counts')]).reset_index()
    fig2 = px.bar(df_id_quest, x='reponse', y='Nombre',
                  color='designation', barmode='group')

    # s.plotly_chart(fig)

    f = df.groupby('nom_metier')["situation_pro"].agg(
        [("Nombre", "value_counts")]).reset_index()
    fig3 = px.bar(f, x='situation_pro', y='Nombre',
                  color='nom_metier', barmode='group')
    tab1, tab2, tab3 = s.tabs(["repartition par sexe",
                               "statistiques sur les questionnaires", "repartition par metier et situation_pro"])
    with tab1:
        s.plotly_chart(fig1, theme="streamlit", use_conatiner_width=True)
    with tab2:
        s.plotly_chart(fig2, theme=None, use_conatiner_width=True)
        s.plotly_chart(fig1, theme="streamlit", use_conatiner_width=True)
    with tab3:
        s.plotly_chart(fig3, theme=None, use_conatiner_width=True)

    a = pd.DataFrame(df["situation_pro"].value_counts().reset_index())
    b = pd.DataFrame(df["nom_commune"].value_counts().reset_index())
    lst = list(df.groupby('nom_commune'))
    colors = ['#8BC34A', '#D4E157', '#FFB300', '#FF7043']
    # here we want our grid to be 2 x 3
    rows = 2
    cols = 3
    # continents are the first element in l
    subplot_titles = [l[0] for l in lst]

    stats = df_fin.groupby('id_sortant')['sexe'].agg(
        [('nombre', 'value_counts')]).reset_index()
    stats = stats.groupby('sexe')['nombre'].agg(
        [('index', 'value_counts')]).reset_index()
    # a compact and general version of what you did
    # specs = [[{'type':'domain'}]* cols] * rows

    specs = [[{"type": "pie"}, {"type": "Bar"}, {"type": "pie"}],
             [{"type": "bar"}, {"type": "bar"}, {"type": "pie"}]]
    fig = make_subplots(
        rows=rows,
        cols=cols,

        subplot_titles=("Situation professionelle des sortants", "",
                        "Secteur de travail des sortants", "Sortants en fonction de la résidence", "", "Répartion des reponses des sortans"),
        specs=specs,
        print_grid=True)

    fig.add_trace(go.Pie(labels=a.loc[:, 'index'], values=a.loc[:, 'situation_pro'],
                         hole=.4, marker=dict(colors=colors), textinfo='label+value+percent', hoverinfo='label', textposition='inside'), row=1, col=1)

    d = df_resp.groupby('reponse')["id_sortant"].agg(
        [("Nombre", "count")]).reset_index()
    fig.add_trace(go.Pie(labels=d.loc[:, 'reponse'], values=d.loc[:, 'Nombre'],
                         marker=dict(colors=colors), hovertemplate="%{label}: <br>Value: %{value} ",
                         showlegend=True,
                         textposition='inside',
                         rotation=90, hole=.4,),
                  row=2,
                  col=3
                  )

    c = df.groupby('sexe')["nom_secteur"].agg(
        [("Nombre", "value_counts")]).reset_index()

    fig.add_trace(go.Pie(labels=c.loc[:, 'nom_secteur'], values=c.loc[:, 'Nombre'],
                         marker=dict(colors=colors), textinfo='label+value+percent', textposition='inside', hoverinfo='label'),
                  row=1,
                  col=3
                  )

    f = df.groupby('nom_metier')["situation_pro"].agg(
        [("Nombre", "value_counts")]).reset_index()

    # fig.add_trace(px.bar(f, x='nom_metier', y='Nombre', color='situation_pro', barmode='group'), row=1,
    #               col=2)
    # fig.update_traces(
    #     marker_color=['slateblue', 'lightblue', 'lightblue'], selector={'name': 'gold'})

    # fig.add_trace(go.Bar(x=stats.loc[:, 'index'], y=stats.loc[:, 'sexe'],orientation='h',textposition="inside",
    #            opacity=0.3, showlegend=False), row=2, col=2)
    fig.add_trace(go.Bar(y=b.loc[:, 'nom_commune'], x=b.loc[:, 'index'],
                         opacity=0.3, showlegend=False), row=2, col=1)

    fig.update_layout(
        # paper_bgcolor= '#FFFDE7',
        plot_bgcolor='#FFFDE7',
        title=dict(text="", x=1, y=1, font_size=30), width=800, height=700,
        showlegend=False)
    s.plotly_chart(fig)


if __name__ == '__main__':
    main()


def run():

    # En-tête
    streamlit.title("Application Machine Learning pour la prédiction ")
    streamlit.subheader("Auteur : Aziz")
    streamlit.markdown("Cette application simule l'utilisation d'un service prédictif qui dérive d'un modèle Machine Learning déployé sur Microsoft Azure."
                       "Le modèle a été construit avec la fonctionnalité Azure Machine Learning Automatisé et a un AUC pondéré de 0.58257 (presque 60% )."
                       "Il prédit si un demandeur d'une formation aura la chance d'etre en emploi ou en Chomage.")

    #df=pd.read_csv("mdata_suivi_pour_azure", sep=",")
    # Variables d'entrées renseignées par l'utilisateur
    var1 = streamlit.text_input("lieu_naiss", "")
    var3 = streamlit.text_input("sexe", "")
    var2 = streamlit.text_input("situation_matrimoniale", "")
    var4 = streamlit.text_input("metier", "")
    var5 = streamlit.text_input("residence")
    var6 = streamlit.text_input("Date_naissance", "")

    # Code du service prédictif

    def allowSelfSignedHttps(allowed):
        # bypass the server certificate verification on client side
        if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
            ssl._create_default_https_context = ssl._create_unverified_context

    # this line is needed if you use self-signed certificate in your scoring service.
    allowSelfSignedHttps(True)

    def return_prediction():
        # Request data goes here
        data = {
            "Inputs": {
                "data": [
                    {
                        "lieu_naiss": var1,
                        "sexe": var3,
                        "situation_matrimoniale": var2,
                        "metier": var4,
                        "residence": var5,
                        "Date_naissance": var6
                    }
                ]
            },
            "GlobalParameters": {
                "method": "predict"
            }
        }

        body = str.encode(json.dumps(data))

        url = 'http://b8c789bb-e52b-42ee-8eae-2f2ba721d62e.eastus2.azurecontainer.io/score'

        headers = {'Content-Type': 'application/json'}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)
            result = response.read()
            return result
            # print(result)

        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))
            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(json.loads(error.read().decode("utf8", 'ignore')))

    #################################
    liste = [var1, var2, var3, var4, var5, var6]
    if streamlit.button("Predict"):
        for i in liste:
            if not i:
                raise Exception(
                    "Renseignez les cellules qui sont toujours vide svp")
        else:
            resultat = return_prediction()
            c = "b"+'{"Results": [1]}'
            d = "Vous avez environ (60%) de chance d'avoir un travail aprés avec formation"
            e = "La probalité d'etre au chomage avec cette formation est d'environ (60%)"
        if resultat == c:
            streamlit.success(d)
        else:
            streamlit.success(e)


if __name__ == '__main__':
    run()
