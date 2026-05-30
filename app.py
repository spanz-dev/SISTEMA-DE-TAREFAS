import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("tarefas.db", check_same_thread=False)
c = conn.cursor()

c.execute('''

          CREATE TABLE IF NOT EXISTS tarefas(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               nome TEXT NOT NULL,
               status TEXT NOT NULL DEFAULT "Pendente"               
          )

''')

conn.commit()

st.title("Gerenciador de tarefas")
st.subheader("Streamlit + SQlite3")

st.markdown("+ Nova Tarefa")

nova_tarefa = st.text_input("O que voce precisa fazer?")

if st.button("Adicionar Tarefa"):
     if nova_tarefa == "":
          st.warning("Digite algo...")
     else:
          c.execute("INSERT INTO tarefas (nome,status) values(?,?)",(nova_tarefa , "pendente"))
          st.success("Voce adicinou uma tarefa")
          conn.commit()
          
st.write("----")

st.markdown("Suas Tarefas")

c.execute("SELECT id , nome , status FROM tarefas")

dados = c.fetchall()

if dados:
     df = pd.DataFrame(dados, columns= ["ID" , "TAREFA" , "STATUS"])
     st.dataframe(df, use_container_width=True, hide_index=True)
     st.markdown("Gerenciar")
     col1,col2 = st.columns(2)

     with col1:
          tarefa_selecionada = st.selectbox("Escolha pelo ID", df["ID"])
     with col2:
          acao = st.radio("Ação", ["Concluir","Excluir"])
     
     if st.button("Confirmar..."):
          if acao == "Concluir":
               c.execute("UPDATE tarefas SET status = 'Concluido' WHERE id = ?" , (tarefa_selecionada,))
               st.success("Tarefa Concluida")
               conn.commit()
          elif acao == "Excluir":
               c.execute("DELETE FROM tarefas WHERE id = ?" , (tarefa_selecionada,))
               st.error("Tarefa Excluida")
               conn.commit()
               
