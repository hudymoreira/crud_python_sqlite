#by hudymoreira@gmail.com
import sqlite3
#cria banco de dados
con = sqlite3.connect('dados.db')
cur = con.cursor()
#cria tabela
cur.execute("create table if not exists cadastro(id integer primary key autoincrement, nome  text, telefone text, endereco text)")
cur.execute("create table if not exists peso(id integer primary key autoincrement, idCadastro integer, peso float, dataRegistro DATETIME DEFAULT (datetime('now','localtime')))")
con.commit()
#lista os dados
def listar(tipo):
    if tipo == 1:
        for linha in cur.execute("select * from cadastro"):
            print(linha)
    if tipo == 2:
        for linha in cur.execute("select c.nome, p.peso, strftime('%d/%m/%Y %H:%M:%S',p.dataRegistro) from peso p left join cadastro c on c.id = p.idCadastro"):
            print(linha)

def listarCadastro(id):
    cur.execute("select * from cadastro where id = {}".format(id))
    return cur.fetchall()

def inserir(tipo):
    if tipo == 1:
        nome = str(input("Digite o seu nome: "))
        telefone = str(input("Digite o seu telefone: "))
        endereco = str(input("Digite o seu endereco: "))
        cur.execute("insert into cadastro (nome,telefone, endereco) values ('{}','{}','{}')".format(nome, telefone,endereco))
        con.commit()
    if tipo == 2:
        id = int(input("Digite id do cadastro: "))
        peso = float(input("Digite o peso: "))
        dados = listarCadastro(id)
        if len(dados) == 0:
            print("id digitado nao consta no cadastro ")
        else:
            r = str(input("deseja associar o peso {} para {} ? [s/n]  ".format(peso,dados[0][1])))
            if r == 's':
                cur.execute("insert into peso (peso, idCadastro) values ('{}','{}')".format(peso, id))
                con.commit()
while True:
    print ("controle de peso")
    print ("1 cadastrar pessoas ")
    print ("2 ver pessoas cadastadas ")
    print ("3 cadastrar peso ")
    print ("4 ver peso cadastrado")
    print ("5 sair")
    opt = int(input("escolha uma opcao: "))
    print("\n\n")
    if opt == 1:
        print("Novo cadastro\n\n")
        inserir(1)
    elif opt == 2:
        print("Cadastro de pessoas : \n\n")
        listar(1)
    elif opt == 3:
        print("Novo registro de peso \n\n")
        inserir(2)
    elif opt == 4:
        print(" Pesos cadastrados\n\n")
        listar(2)
    elif opt == 5:
        break
    else :
        print("opcao invalida")
        print("\n\n")

con.close()

