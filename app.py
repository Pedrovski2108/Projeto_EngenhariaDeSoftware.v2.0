import streamlit as st
import pandas as pd
import sqlite3

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Sistema de Gestão Escolar",
    page_icon="📚",
    layout="centered"
)

# --- FUNÇÕES DE BANCO DE DADOS ---

# Função para criar uma conexão com o banco de dados
def get_db_connection():
    conn = sqlite3.connect('escola.db')
    return conn

# Função para buscar todos os alunos
def get_alunos():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM alunos ORDER BY nome", conn)
    conn.close()
    return df

# Função para buscar todas as disciplinas
def get_disciplinas():
    conn = get_db_connection()
    df = pd.read_sql_query("SELECT * FROM disciplinas ORDER BY nome", conn)
    conn.close()
    return df

# Função para buscar as notas de um aluno específico
def get_notas_aluno(aluno_id):
    conn = get_db_connection()
    query = """
    SELECT 
        d.nome as Disciplina, 
        n.nota as Nota
    FROM notas n
    JOIN disciplinas d ON n.disciplina_id = d.id
    WHERE n.aluno_id = ?
    """
    df = pd.read_sql_query(query, conn, params=(aluno_id,))
    conn.close()
    return df

# Função para inserir uma nova nota no banco de dados
def adicionar_nota(aluno_id, disciplina_id, nota):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notas (aluno_id, disciplina_id, nota) VALUES (?, ?, ?)",
        (aluno_id, disciplina_id, nota)
    )
    conn.commit()
    conn.close()

# --- INTERFACE DA APLICAÇÃO ---

st.title("📚 Sistema de Gestão de Notas")
st.markdown("Bem-vindo ao portal de gestão de notas. Selecione um aluno para visualizar ou adicionar notas.")

# Carrega os dados dos alunos e disciplinas uma vez
alunos_df = get_alunos()
disciplinas_df = get_disciplinas()

# --- SEÇÃO DE VISUALIZAÇÃO E CADASTRO ---

st.header("Consulta e Lançamento de Notas")

aluno_selecionado_nome = st.selectbox(
    'Selecione o Aluno:',
    options=alunos_df['nome'],
    index=None, 
    placeholder="Escolha um aluno..."
)

if aluno_selecionado_nome:
    # CORREÇÃO APLICADA AQUI: Adicionado .iloc[0] para pegar o valor numérico do ID
    aluno_id_selecionado = alunos_df[alunos_df['nome'] == aluno_selecionado_nome]['id'].iloc[0]

    st.subheader(f"Notas de {aluno_selecionado_nome}")

    notas_df = get_notas_aluno(aluno_id_selecionado)

    if notas_df.empty:
        st.warning("Este aluno ainda não possui notas lançadas.")
    else:
        st.dataframe(notas_df, use_container_width=True)

    st.markdown("---")

    st.subheader("Adicionar Nova Nota")

    with st.form("form_add_nota"):
        disciplina_selecionada_nome = st.selectbox(
            'Disciplina:',
            options=disciplinas_df['nome']
        )
        
        nova_nota = st.number_input('Nota:', min_value=0.0, max_value=10.0, step=0.5)
        
        submitted = st.form_submit_button("Lançar Nota")

        if submitted:
            # CORREÇÃO APLICADA AQUI: Adicionado .iloc[0] para pegar o valor numérico do ID
            disciplina_id_selecionada = disciplinas_df[disciplinas_df['nome'] == disciplina_selecionada_nome]['id'].iloc[0]
            
            adicionar_nota(aluno_id_selecionado, disciplina_id_selecionada, nova_nota)
            
            st.success(f"Nota {nova_nota} em {disciplina_selecionada_nome} lançada com sucesso para {aluno_selecionado_nome}!")
            st.info("A tabela de notas será atualizada automaticamente.")
            
            st.rerun()