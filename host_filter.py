from logging import error
from os import urandom
from flask import Flask, session, render_template, request, redirect, url_for
import mysql.connector
import smtplib, ssl
import string
import random
import requests
import json

#variaveis não importantes
app = Flask(__name__)
app.secret_key = urandom(20)

email_falso = 'falsiano@fake.service.com'

SQL_config = {
    'user':'debian-sys-maint',
    'password':'26QutYzITxdC6Aa7',
    'host':'127.0.0.1',
    'database':'siteHost'
}

forward_hosts =[
"X-Host",
"X-Forwarded-Host",
"X-Forwarded-Server",
"X-HTTP-Host-Override",
"Forwarded"
]

host = "127.0.0.1:5000"

sender_address = 'bad.site.no.reply@gmail.com'
sender_password = 'badjoao1234'

erro_host_errado = "erro, host invalido  >:("

def correct_host(headers):
    for possible_header in forward_hosts:
        if possible_header in headers:
            print(possible_header)
            return headers[possible_header]
    if headers['host'] == host:
        return headers['host']
    else:
        return False
    
#função auxiliar para realizar query no banco de dados    
def executeQuery(query, param=None):
    
    #Se exister executando, troque user e password aqui para acessar o seu mysql local
    mysqlConnection = mysql.connector.connect(**SQL_config)
    myCursor = mysqlConnection.cursor()
    if param == None:
        myCursor.execute(query)
    else:
        myCursor.execute(query, param)
    res = myCursor.fetchall()
    mysqlConnection.commit()
    myCursor.close()
    mysqlConnection.close()
    return res
    
#funcao auxiliar que envia email():
def send_email(receiver_address, message):
    port = 465 

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_address, sender_password)
        server.sendmail(sender_address, receiver_address, message)




@app.route('/login', methods=['GET', 'POST'])
def login():
    if not correct_host(request.headers):
        return render_template('erro.html', error="Host invalido >:(")
    
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('index'))
        else:
            return render_template('login.html')

    elif request.method == 'POST':
        
        #pega senha certa do banco de dados, se existe
        realPass = executeQuery("SELECT password FROM siteHost.users WHERE username = %s;", (request.form['username'],))

        #loga o usuario usando session se a senha que mandou esta igual a do banco de dados
        if (len(realPass) > 0  and request.form['password'] == realPass[0][0]):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Senha ou nome de usuario errado')


@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if not correct_host(request.headers):
        return render_template('erro.html', error="Host invalido >:(")
    
    if request.method == 'GET':
        if 'username' in session:
            return redirect(url_for('index'))
        else:
            return render_template('cadastro.html')

    elif request.method == 'POST':
        
        #verifica se o nome de usuario existe
        user = executeQuery("SELECT * FROM siteHost.users WHERE username = %s;", (request.form['username'],))
        
        if len(user) > 0:
            return render_template('cadastro.html', error='Nome de usuario ja existe')
        
        #insere dados no banco de dados
        executeQuery("INSERT INTO siteHost.users (username, password, email) VALUES (%s, %s, %s);", 
                     (request.form['username'],request.form['password'],request.form['email']))
        
        return redirect(url_for('login'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if not correct_host(request.headers):
        return render_template('erro.html', error="Host invalido >:(")
    
    if 'username' in session:
        if request.method == 'GET':

            #seleciona 5 ultimos posts e renderiza eles 
            posts = executeQuery('SELECT * FROM siteHost.posts ORDER BY id DESC LIMIT 5;')
            return render_template('index.html', posts=posts)
        
        elif request.method == 'POST':
            
            #cria link baseado no ID
            queryRes = executeQuery('''SELECT `AUTO_INCREMENT`
                                    FROM  INFORMATION_SCHEMA.TABLES
                                    WHERE TABLE_SCHEMA = 'siteHost'
                                    AND   TABLE_NAME   = 'posts';''')
            nextID = int(queryRes[0][0])            
            myLink = '/seepost?id='+str(nextID)
            
            #insere no banco de dados novo post
            executeQuery("INSERT INTO siteHost.posts (titulo, conteudo, link, author) VALUES (%s, %s, %s, %s);", (request.form['title'], request.form['content'], myLink, session['username']))
            return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))
    

@app.route('/resetPassSend', methods=['GET', 'POST'])
def reset():
    if not correct_host(request.headers):
        return render_template('erro.html', error="Host invalido >:(")
        
    if request.method == 'GET':
        
        return render_template('resetPassSend.html')

    elif request.method == 'POST':
        
        #verifica que o nome de usuario existe
        user = executeQuery("SELECT * FROM siteHost.users WHERE username = %s;", (request.form['username'],))
        if len(user) > 0:
            
            #cria um token de reset de senha
            token = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
            
            #associa o token a conta do usuario
            executeQuery("UPDATE siteHost.users SET token = %s WHERE username = %s;", (token, request.form['username']))
            
            #gera link de reset de senha com token
            resetLink = 'http://'+ correct_host(request.headers) +'/resetPassReceive?token='+token
            
            #descobre o email do usuario
            user_email = executeQuery("SELECT email FROM siteHost.users WHERE username = %s;", (request.form['username'],))[0][0]
            
            #Se for a vitima, acessa o link
            if user_email == email_falso:
                print(resetLink)
                resp = requests.get(resetLink)
            else:
                #Senao, envia o token para o email do usuario
                message = """\
                Subject: password reset

                ola, ouvi falar que tu quer mudar tua senha.
                To aqui o link:
                """ + resetLink
                send_email(user_email, message)
            
            return render_template('resetPassSend.html', aviso="Link de reset enviado pro email :)")
        else:
            return render_template('resetPassSend.html', error="Nome de usuario errado D:")


@app.route('/resetPassReceive', methods=['GET', 'POST'])
def receive():
    if not correct_host(request.headers):
        return render_template('erro.html', error="Host invalido >:(")
    
    if request.method == 'GET':
        
        if 'token' in request.args:

            #seleciona conta que tem o token do usuario, se existe
            account = executeQuery("SELECT * FROM siteHost.users WHERE token=%s", (request.args.get('token'),))

            if len(account)>0:
                return render_template('resetPassReceive.html', token=request.args.get('token'))
            else:
                print(request.args.get('token'))
                return render_template('resetPassReceive.html')
            pass
        else:
            return render_template('resetPassReceive.html')
    elif request.method == 'POST':
        executeQuery("UPDATE siteHost.users SET password = %s, token = NULL WHERE token = %s", (request.form['password'],request.form['token']))
        return redirect(url_for('login'))
    

@app.route('/seepost')
def seepost():
    if not correct_host(request.headers):
        return render_template('erro.html', error="Host invalido >:(")
    
    postID = request.args.get('id')
    postInfo = executeQuery('SELECT titulo, conteudo, link, author FROM siteHost.posts WHERE id=%s;', (postID,))
    print(postInfo)
    return render_template('singlepost.html', post=postInfo[0])
    
    
@app.route('/logout')
def logout():
    if not correct_host(request.headers):
        return render_template('erro.html', error="Host invalido >:(")
    
    session.clear()
    return redirect(url_for('login'))


if (__name__ == "__main__"):
    app.run(host='0.0.0.0')