import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('escola.db')
cursor = conn.cursor()

# -- Apagar tabelas existentes para um começo limpo --
cursor.execute("DROP TABLE IF EXISTS notas")
cursor.execute("DROP TABLE IF EXISTS alunos")
cursor.execute("DROP TABLE IF EXISTS disciplinas")

# -- Criar as tabelas --
# Tabela de Alunos
cursor.execute("""
CREATE TABLE alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);
""")

# Tabela de Disciplinas
cursor.execute("""
CREATE TABLE disciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);
""")

# Tabela de Notas (relaciona alunos, disciplinas e a nota)
cursor.execute("""
CREATE TABLE notas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER,
    disciplina_id INTEGER,
    nota REAL NOT NULL,
    FOREIGN KEY (aluno_id) REFERENCES alunos(id),
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas(id)
);
""")

# -- Inserir dados de exemplo --
# Alunos
alunos = [('Ana Silva',), ('Bruno Costa',), ('Carla Dias',)]
cursor.executemany("INSERT INTO alunos (nome) VALUES (?)", alunos)

# Disciplinas
disciplinas = [('Matemática',), ('Português',), ('História',), ('Ciências',)]
cursor.executemany("INSERT INTO disciplinas (nome) VALUES (?)", disciplinas)

# Notas de Exemplo para a aluna 'Ana Silva' (ID 1)
notas_ana = [(1, 1, 8.5), (1, 2, 9.0), (1, 3, 7.5)] # Ana: Mat, Port, Hist
cursor.executemany("INSERT INTO notas (aluno_id, disciplina_id, nota) VALUES (?, ?, ?)", notas_ana)

# Notas de Exemplo para o aluno 'Bruno Costa' (ID 2)
notas_bruno = [(2, 1, 6.5), (2, 4, 9.5)] # Bruno: Mat, Cien
cursor.executemany("INSERT INTO notas (aluno_id, disciplina_id, nota) VALUES (?, ?, ?)", notas_bruno)


# Salvar as mudanças e fechar a conexão
conn.commit()
conn.close()

print("Banco de dados 'escola.db' criado com sucesso e populado com dados de exemplo.")

Passo 2: O Aplicativo Streamlit
Agora, o arquivo principal. Apague o app.py que você tem e use este. Ele é completo, comentado e focado no nosso MVP.

Crie um arquivo chamado app.py:

Python

# app.py
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
    # Usamos o pandas para ler o SQL e já transformar em um DataFrame
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
    # Passamos o ID do aluno como parâmetro para a consulta
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

# Selectbox para escolher o aluno
# Usamos o dataframe de alunos para popular as opções
aluno_selecionado_nome = st.selectbox(
    'Selecione o Aluno:',
    options=alunos_df['nome'],
    index=None, # Faz com que nada seja selecionado por padrão
    placeholder="Escolha um aluno..."
)

# Se um aluno foi selecionado, o código dentro do "if" é executado
if aluno_selecionado_nome:
    # Encontra o ID do aluno selecionado
    aluno_id_selecionado = alunos_df[alunos_df['nome'] == aluno_selecionado_nome]['id'].iloc[0]

    st.subheader(f"Notas de {aluno_selecionado_nome}")

    # Busca e exibe as notas do aluno
    notas_df = get_notas_aluno(aluno_id_selecionado)

    if notas_df.empty:
        st.warning("Este aluno ainda não possui notas lançadas.")
    else:
        st.dataframe(notas_df, use_container_width=True)

    st.markdown("---")

    # --- FORMULÁRIO PARA ADICIONAR NOVA NOTA ---
    st.subheader("Adicionar Nova Nota")

    # st.form ajuda a agrupar vários inputs e um botão
    # A ação só é executada quando o botão dentro do form é clicado
    with st.form("form_add_nota"):
        # Selectbox para escolher a disciplina
        disciplina_selecionada_nome = st.selectbox(
            'Disciplina:',
            options=disciplinas_df['nome']
        )
        
        # Input numérico para a nota
        nova_nota = st.number_input('Nota:', min_value=0.0, max_value=10.0, step=0.5)
        
        # Botão de envio do formulário
        submitted = st.form_submit_button("Lançar Nota")

        if submitted:
            # Encontra o ID da disciplina selecionada
            disciplina_id_selecionada = disciplinas_df[disciplinas_df['nome'] == disciplina_selecionada_nome]['id'].iloc[0]
            
            # Chama a função para adicionar a nota no banco
            adicionar_nota(aluno_id_selecionado, disciplina_id_selecionada, nova_nota)
            
            # Exibe uma mensagem de sucesso
            st.success(f"Nota {nova_nota} em {disciplina_selecionada_nome} lançada com sucesso para {aluno_selecionado_nome}!")
            st.info("A tabela de notas será atualizada automaticamente.")
            
            # Recarrega a página para mostrar a nova nota na tabela acima.
            # Em apps maiores, existem técnicas mais avançadas, mas para este caso, é perfeito.
            st.rerun()
