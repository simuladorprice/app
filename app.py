import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Pesquisa CEPAL", layout="centered")

st.title("📊 Pesquisa sobre CEPAL e Desenvolvimento")
st.write("Responda de 1 a 5, onde:")
st.write("1 = Discordo totalmente | 5 = Concordo totalmente")

# Perguntas
perguntas = [
    "A CEPAL ainda explica a América Latina de hoje?",
    "Industrialização continua sendo solução?",
    "O foco em desigualdade fortalece ou enfraquece o desenvolvimento?",
    "A CEPAL é uma escola de pensamento, um órgão técnico ou uma agenda política?"
]

# Formulário
with st.form("formulario"):
    respostas = []

    for pergunta in perguntas:
        resposta = st.slider(pergunta, 1, 5, 3)
        respostas.append(resposta)

    comentario = st.text_area("Comentário opcional")

    submit = st.form_submit_button("Enviar resposta")

# Salvar resultados
if submit:
    dados = {
        "Pergunta 1": respostas[0],
        "Pergunta 2": respostas[1],
        "Pergunta 3": respostas[2],
        "Pergunta 4": respostas[3],
        "Comentário": comentario
    }

    df = pd.DataFrame([dados])

    arquivo = "respostas.csv"

    if os.path.exists(arquivo):
        df_antigo = pd.read_csv(arquivo)
        df_final = pd.concat([df_antigo, df], ignore_index=True)
    else:
        df_final = df

    df_final.to_csv(arquivo, index=False)

    st.success("✅ Resposta enviada com sucesso!")

# Mostrar resultados
st.subheader("📈 Resultados até agora")

arquivo = "respostas.csv"

if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)

    media = df.iloc[:, :4].mean()

    st.write("Média das respostas:")
    st.bar_chart(media)

    with st.expander("Ver comentários"):
        comentarios = df["Comentário"].dropna()
        for c in comentarios:
            if c.strip():
                st.write(f"- {c}")
else:
    st.info("Nenhuma resposta registrada ainda.")
