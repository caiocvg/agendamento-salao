
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Arquivo onde os dados serão salvos
ARQUIVO_EXCEL = "clientes.xlsx"

# Inicializar o DataFrame ou carregar existente
def carregar_dados():
    if os.path.exists(ARQUIVO_EXCEL):
        return pd.read_excel(ARQUIVO_EXCEL)
    else:
        return pd.DataFrame(columns=["Nome", "Data", "Horário", "Celular", "Funcionário"])

# Salvar dados no Excel
def salvar_dados(dados):
    dados.to_excel(ARQUIVO_EXCEL, index=False)

# Carregar dados existentes
df = carregar_dados()

st.set_page_config(page_title="Agendamento de Clientes - Salão", layout="centered")
st.title("📅 Sistema de Agendamento - Salão de Beleza")

# Formulário de cadastro
with st.form("formulario_cadastro"):
    nome = st.text_input("Nome do Cliente")
    data = st.date_input("Data do Agendamento", value=datetime.today())
    horario = st.time_input("Horário do Agendamento")
    celular = st.text_input("Celular")
    funcionario = st.text_input("Funcionário Responsável")

    submitted = st.form_submit_button("Cadastrar Agendamento")

    if submitted:
        if nome and funcionario:
            data_str = data.strftime("%d/%m/%Y")
            hora_str = horario.strftime("%H:%M")

            # Verificar se já existe agendamento nesse horário e data
            conflito = df[(df["Data"] == data_str) & (df["Horário"] == hora_str)]
            if not conflito.empty:
                st.warning("⚠️ Já existe um agendamento nesse horário!")

            # Salvar o novo agendamento
            novo = pd.DataFrame([[nome, data_str, hora_str, celular, funcionario]],
                                columns=["Nome", "Data", "Horário", "Celular", "Funcionário"])
            df = pd.concat([df, novo], ignore_index=True)
            salvar_dados(df)
            st.success("✅ Agendamento salvo com sucesso!")
        else:
            st.error("Por favor, preencha todos os campos obrigatórios.")

st.markdown("---")
st.subheader("📋 Agendamentos Salvos")
st.dataframe(df, use_container_width=True)

st.info("Os dados são armazenados localmente no arquivo 'clientes.xlsx'.")
