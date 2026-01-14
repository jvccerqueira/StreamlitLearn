import streamlit as st
import pandas as pd

st.set_page_config(page_title="Finance", page_icon=":moneybag:", layout="centered")

st.text("Hello, Streamlit!")

# Widget de upload de arquivo
file_upload = st.file_uploader(label='Faça o upload dos dados', type=['csv'])

# Verifica se o arquivo foi carregado e exibe o DataFrame
if file_upload:
    # Leitura do arquivo CSV
    df = pd.read_csv(file_upload, sep=',')
    df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y').dt.date

    # Exibição do DataFrame
    exp1 = st.expander("Dados Brutos")
    columns_fmt = {'Valor': st.column_config.NumberColumn('Valor', format='R$ %.2f')}
    exp1.dataframe(df, hide_index=True, column_config=columns_fmt)

    # Visao Instituição
    exp2 = st.expander("Instituições")
    df_instituicao = df.pivot_table(index='Data', columns='Instituição', values='Valor')

    # Abas para Dados, Histórico e Distribuição
    tab_data, tab_history, tab_share = exp2.tabs(["Dados", "Histórico", "Distribuição"])
    
    # Exibe dataframe
    with tab_data:
        st.dataframe(df_instituicao, column_config=columns_fmt)
    # Exibe gráfico de linhas
    with tab_history:
        st.line_chart(df_instituicao)
    # Exibe gráfico de barras para data selecionada
    with tab_share:
        # date = st.date_input('Data para distribuição dos valores',
        #                      min_value=df_instituicao.index.min(),
        #                      max_value=df_instituicao.index.max(),)
        date = st.selectbox('Data para distribuição dos valores',
                            options=df_instituicao.index,)

        if  date not in df_instituicao.index:
            st.warning('Data selecionada não está disponível nos dados.')
        else:
            st.bar_chart(df_instituicao.loc[date])