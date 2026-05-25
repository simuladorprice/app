import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Pesquisa CEPAL", layout="centered")

st.title("📊 Pesquisa sobre CEPAL")
st.write("Responda às perguntas com **Sim ou Não**.")

# Perguntas
perguntas = [
    "A CEPAL ainda explica a América Latina de hoje?",
    "De acordo com a CEPAL a industrialização é um fim em si?",
    "O foco em desigualdade fortalece o desenvolvimento?",
    "A CEPAL é uma escola de pensamento?",
    "A CEPAL é um órgão técnico?",
    "A CEPAL é uma agenda política?"
]

# Formulário
with st.form("formulario"):
    respostas = []

    for pergunta in perguntas:
        resposta = st.radio(pergunta, ["Sim", "Não"])
        respostas.append(resposta)

    comentario = st.text_area("Comentário opcional")

    submit = st.form_submit_button("Enviar resposta")

# Salvar
if submit:
    dados = {
        perguntas[i]: respostas[i] for i in range(len(perguntas))
    }
    dados["Comentário"] = comentario

    df = pd.DataFrame([dados])

    arquivo = "respostas.csv"

    if os.path.exists(arquivo):
        df_antigo = pd.read_csv(arquivo)
        df_final = pd.concat([df_antigo, df], ignore_index=True)
    else:
        df_final = df

    df_final.to_csv(arquivo, index=False)

    st.success("✅ Resposta enviada com sucesso!")

# 📈 Resultados
st.subheader("📊 Resultados")

arquivo = "respostas.csv"

if os.path.exists(arquivo):
    df = pd.read_csv(arquivo)

    for pergunta in perguntas:
        st.write(f"**{pergunta}**")

        contagem = df[pergunta].value_counts()

        # garantir que apareça sim e não mesmo se faltar um
        contagem = contagem.reindex(["Sim", "Não"], fill_value=0)

        st.bar_chart(contagem)

    # Comentários
    with st.expander("Ver comentários"):
        comentarios = df["Comentário"].dropna()
        for c in comentarios:
            if c.strip():
                st.write(f"- {c}")

else:
    st.info("Nenhuma resposta registrada ainda.")
