from flask import Flask, render_template, redirect, request
import psycopg2

app = Flask(__name__)

def ligar_banco():
    banco = psycopg2.connect(
        host="localhost",
        dbname="estoque",
        user="postgres",
        password="senai",
        port="5432"
    )
    return banco

@app.route("/")
def inicio():
    return render_template('index.html')

@app.route('/fornecedor')
def fornecedor():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_fornecedor, nome_fornecedor, cidade_fornecedor, prazo_dias, data_cadastro FROM fornecedor ORDER BY id_fornecedor")
    lista = cursor.fetchall()
    banco.close()
    return render_template("fornecedores.html", fornecedores=lista)

@app.route("/fornecedores/enviar", methods=["POST"])
def enviar_tarefa():
    nome = request.form.get("nome_fornecedor")
    cidade = request.form.get("cidade_fornecedor")
    prazo = request.form.get("prazo_dias")
    data = request.form.get("data_cadastro")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO fornecedor (nome_fornecedor, cidade_fornecedor, prazo_dias, data_cadastro)
        VALUES (%s, %s, %s, %s)""", (nome, cidade, prazo, data))
    banco.commit()
    banco.close()
    return redirect("/fornecedor")

@app.route("/fornecedores/editar/<int:id>")
def editar_fornecedor(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_fornecedor, nome_fornecedor, cidade_fornecedor, prazo_dias, data_cadastro FROM fornecedor WHERE id_fornecedor = %s", (id,))
    fornecedor = cursor.fetchone()
    banco.close()

    if fornecedor is None:
        return redirect("/")
    return render_template("editar_fornecedores.html", fornecedor=fornecedor)

@app.route("/fornecedores/atualizar/<int:id>", methods=["POST"])
def atualizar_tarefa(id):
    nome = request.form.get("nome_fornecedor")
    cidade = request.form.get("cidade_fornecedor")
    prazo = request.form.get("prazo_dias")
    data = request.form.get("data_cadastro")

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""UPDATE fornecedor 
                      SET nome_fornecedor   = %s,
                          cidade_fornecedor = %s,
                          prazo_dias        = %s,
                          data_cadastro     = %s
                      WHERE id_fornecedor = %s
                   """, (nome, cidade, prazo, data, id))
    banco.commit()
    banco.close()
    return redirect("/fornecedor")

@app.route("/fornecedores/excluir/<int:id>", methods=["POST"])
def excluir_tarefa(id):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("DELETE FROM fornecedor WHERE id_fornecedor = %s", (id,))
    banco.commit()
    banco.close()
    return redirect("/fornecedor")

@app.route('/produto')
def produtos():
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("SELECT id_produto, nome_produto, categoria_produto, quantidade_produto, preco_produto FROM produto ORDER BY id_produto")
    lista = cursor.fetchall()
    banco.close()
    return render_template("produto.html", produto=lista)

@app.route('/produto/enviar', methods=['POST'])
def enviar_produto():
    nome_produto = request.form.get('nome_produto')
    categoria_produto = request.form.get('categoria_produto')
    quantidade_produto = request.form.get('quantidade_produto')
    preco_produto = request.form.get('preco_produto')

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""INSERT INTO produto (nome_produto, categoria_produto, quantidade_produto, preco_produto) VALUES (%s,%s,%s,%s)""", (nome_produto, categoria_produto, quantidade_produto, preco_produto))
    banco.commit()
    banco.close()
    return redirect('/produto')


@app.route('/produto/editar/<int:id_produto>')
def editar_produto(id_produto):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(
        "SELECT nome_produto, categoria_produto, quantidade_produto, preco_produto FROM produto WHERE id_produto = %s", (id_produto,))
    produto = cursor.fetchone()
    banco.close()

    if produto is None:
        return redirect('produto/enviar')

    return render_template("editar_produto.html", produto=produto, id_produto=id_produto)


@app.route('/produto/atualizar/<int:id_produto>', methods=['POST'])
def atualizar_produto(id_produto):
    nome_produto = request.form.get('nome_produto')
    categoria_produto = request.form.get('categoria_produto')
    quantidade_produto = request.form.get('quantidade_produto')
    preco_produto = request.form.get('preco_produto')

    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute("""
        UPDATE produto SET nome_produto = %s, categoria_produto = %s, quantidade_produto = %s, preco_produto = %s WHERE id_produto = %s
    """, (nome_produto, categoria_produto, quantidade_produto, preco_produto, id_produto))
    banco.commit()
    banco.close()
    return redirect('/produto')


@app.route('/produto/excluir/<int:id_produto>', methods=['POST'])
def excluir_produto(id_produto):
    banco = ligar_banco()
    cursor = banco.cursor()
    cursor.execute(
        "DELETE FROM produto WHERE id_produto = %s", (id_produto,))
    banco.commit()
    banco.close()
    return redirect('/produto')




if __name__ == '__main__':
    app.run()
