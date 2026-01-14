import streamlit as st
import pandas as pd

def compute_metrics(df):
    df_data = df.groupby(by='Data')[['Valor']].sum()
    df_data['lag_1'] = df_data['Valor'].shift(1)
    df_data['Diferenca_mensal'] = df_data['Valor'] - df_data['lag_1']
    df_data['Media 6M Diferenca Mensal'] = df_data['Diferenca_mensal'].rolling(6).mean()
    df_data['Media 12M Diferenca Mensal'] = df_data['Diferenca_mensal'].rolling(12).mean()
    df_data['Media 24M Diferenca Mensal'] = df_data['Diferenca_mensal'].rolling(24).mean()
    df_data['Diferença mensal %'] = df_data["Valor"] / df_data["lag_1"] - 1
    df_data['Evolução 6M Total'] = df_data['Valor'].rolling(6).apply(lambda x: x[-1] - x[0])
    df_data['Evolução 12M Total'] = df_data['Valor'].rolling(12).apply(lambda x: x[-1] - x[0])
    df_data['Evolução 24M Total'] = df_data['Valor'].rolling(24).apply(lambda x: x[-1] - x[0])
    df_data['Evolução 6M Relativa'] = df_data['Valor'].rolling(6).apply(lambda x: x[-1] / x[0] - 1)
    df_data['Evolução 12M Relativa'] = df_data['Valor'].rolling(12).apply(lambda x: x[-1] / x[0] - 1)
    df_data['Evolução 24M Relativa'] = df_data['Valor'].rolling(24).apply(lambda x: x[-1] / x[0] - 1)

    df_data = df_data.drop(columns=['lag_1'])
    return df_data

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
    # Métricas Gerais

    exp3 = st.expander("Métricas Gerais")

    df_stats = compute_metrics(df)
    columns_fmt_stats = {
        'Valor': st.column_config.NumberColumn('Valor', format='R$ %.2f'),
        'Diferenca_mensal': st.column_config.NumberColumn('Diferença Mensal', format='R$ %.2f'),
        'Media 6M Diferenca Mensal': st.column_config.NumberColumn('Média 6M Diferença Mensal', format='R$ %.2f'),
        'Media 12M Diferenca Mensal': st.column_config.NumberColumn('Média 12M Diferença Mensal', format='R$ %.2f'),
        'Media 24M Diferenca Mensal': st.column_config.NumberColumn('Média 24M Diferença Mensal', format='R$ %.2f'),
        'Evolução 6M Total': st.column_config.NumberColumn('Evolução 6M Total', format='R$ %.2f'),
        'Evolução 12M Total': st.column_config.NumberColumn('Evolução 12M Total', format='R$ %.2f'),
        'Evolução 24M Total': st.column_config.NumberColumn('Evolução 24M Total', format='R$ %.2f'),
        'Diferença mensal %': st.column_config.NumberColumn('Diferença Mensal %', format='percent'),
        'Evolução 6M Relativa': st.column_config.NumberColumn('Evolução 6M Relativa', format='percent'),
        'Evolução 12M Relativa': st.column_config.NumberColumn('Evolução 12M Relativa', format='percent'),
        'Evolução 24M Relativa': st.column_config.NumberColumn('Evolução 24M Relativa', format='percent'),
    }

    tab_stats, tab_abs, tab_rel = exp3.tabs(["Dados", "Histórico de Evolução", "Crescimento Relativo"])

    with tab_stats:
        st.dataframe(df_stats, column_config=columns_fmt_stats)
    with tab_abs:
        abs_cols = [
            'Diferenca_mensal',
            'Media 6M Diferenca Mensal',
            'Media 12M Diferenca Mensal',
            'Media 24M Diferenca Mensal'
        ]

        st.line_chart(df_stats[abs_cols])
    with tab_rel:
        rel_cols = [
            'Diferença mensal %',
            'Evolução 6M Relativa',
            'Evolução 12M Relativa',
            'Evolução 24M Relativa'
        ]

        st.line_chart(df_stats[rel_cols])