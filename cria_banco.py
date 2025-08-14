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