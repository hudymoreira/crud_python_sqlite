# by hudymoreira@gmail.com
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
        for linha in cur.execute("select p.id, c.nome, p.peso, strftime('%d/%m/%Y %H:%M:%S',p.dataRegistro) from peso p left join cadastro c on c.id = p.idCadastro"):
            print(linha)

def listarCadastro(id):
    cur.execute("select * from cadastro where id = {}".format(id))
    return cur.fetchall()

def listarPeso(id):
    cur.execute("select p.peso, c.nome, strftime('%d/%m/%Y %H:%M:%S',p.dataRegistro) from peso p left join cadastro c on c.id = p.idCadastro where p.id = {}".format(id))
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
def editar(tipo):
    if tipo == 1:
        id = int(input("Digite o id do peso: "))
        peso = listarPeso(id)
        if len(peso) == 0:
            print("id digitado nao consta no cadastro")
        else:
            peso = peso[0]
            valor = int(input("digite o valor do peso: "))
            r = str(input("Deseja editar o peso de {} de {} do dia {} para {} ? [s/n] ".format(peso[1],peso[0],peso[2],valor)))
            if r == 's':
                cur.execute("update peso set peso = {} where id = {} ".format(valor, id))
                con.commit()
    if tipo == 2:
        id = int(input("Digite id do cadastro: "))
        dados = listarCadastro(id)
        if len(dados) == 0:
            print("id digitado nao consta no cadastro ")
        else:
            nome = str(input("Digite o nome: "))
            telefone = str(input("Digite o telefone: "))
            endereco = str(input("Digite o endereco: "))
            dados = dados[0]
            print("antes: \n")
            print("nome: {}".format(dados[1]))
            print("telefone: {}".format(dados[2]))
            print("endereco: {}".format(dados[3]))
            print("depois: \n")
            print("nome: {}".format(nome))
            print("telefone: {}".format(telefone))
            print("endereco: {} \n".format(endereco))
            r = str(input("deseja efetuar essa alteracao? [s/n] "))
            if r == 's':
                cur.execute("update cadastro set nome = '{}', telefone = '{}', endereco = '{}'where id = {} ".format(nome,telefone,endereco, id))
                con.commit()

def apagar(tipo):
    if tipo == 1:
        id = int(input("Digite id do cadastro: "))
        dados = listarCadastro(id)
        if len(dados) == 0:
            print("id digitado nao consta no cadastro ")
        else:
            dados = dados[0]
            print ("Apagar esse registro ?")
            print(dados)
            r = str(input("[s/n]: "))
            if r == 's':
                cur.execute("delete from cadastro where id = {}".format(id))
                con.commit()
    if tipo == 2:
        id = int(input("Digite id do peso: "))
        dados = listarPeso(id)
        if len(dados) == 0:
            print("id digitado nao consta no banco ")
        else:
            dados = dados[0]
            print ("Apagar esse registro ?")
            print(dados)
            r = str(input("[s/n]: "))
            if r == 's':
                cur.execute("delete from peso where id = {}".format(id))
                con.commit()


while True:
    print ("controle de peso")
    print ("1 cadastrar pessoas ")
    print ("2 ver pessoas cadastadas ")
    print ("3 cadastrar peso ")
    print ("4 ver peso cadastrado")
    print ("5 editar cadastro")
    print ("6 editar peso")
    print ("7 apagar cadastro")
    print ("8 apagar peso")
    print ("9 sair")

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
        print("Editar cadastro")
        editar(2)
    elif opt == 6:
        print("Editar peso")
        editar(1)
    elif opt == 7:
        print("Apagar cadastro")
        apagar(1)
    elif opt == 8:
        print("Apagar peso")
        apagar(2)
    elif opt == 9:
        break
    else :
        print("opcao invalida")
        print("\n\n")



con.close()

