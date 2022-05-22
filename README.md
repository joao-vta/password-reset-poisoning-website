# host-header-private
Codigo Fonte de um site vulneravel a Host Header Attack.  
Instruções para uso local:

## instalação
- Crie um venv
- - virtualenv -p python3 venv
- Entre no venv Instale o mysqlconnector, flask e requests no venv com PIP
- - source bin/activate
- - pip3 install flask
- - pip3 install mysql-connector-python
- - pip3 install requests
- Crie banco de dados e tabelas no mysql:
- - CREATE DATABASE siteHost;
- - CREATE TABLE siteHost.users (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, username VARCHAR(400), password VARCHAR(400), email VARCHAR(400), token VARCHAR(400));
- - CREATE TABLE siteHost.posts (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, titulo VARCHAR(400), conteudo VARCHAR(400), link VARCHAR(400), author VARCHAR(400));
- Insira manualmente usuários no banco de dados
- - INSERT INTO siteHost.users (username, password, email) VALUES ('nome', 'senha', 'email@gmail.com');
- Altere as credenciais da conexão mysql para sua maquina no codigo

## execução
- Entre no venv navegando até a pasta e executando  'source bin/activate'
- Especifique o app do flask executando 'export FLASK_APP=hello.py'
- - Opcionalmente, execute 'export FLASK_ENV=development' para ativar modo de desenvolvimento
- Inicie o site executando 'flask run'
