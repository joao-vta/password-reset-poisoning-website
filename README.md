# host-header-private
Site Vulneravel a Host Header Attack
Instruções para uso local:
- crie um venv
- copie o codigo fonte
- installe o mysqlconnector e o flask no venv
- crie banco de dados e tabelas no mysql:
- - CREATE DATABASE siteHost;
- - CREATE TABLE siteHost.users (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, username VARCHAR(400), password VARCHAR(400), email VARCHAR(400), token VARCHAR(400));
- - CREATE TABLE siteHost.posts (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, titulo VARCHAR(400), conteudo VARCHAR(400), link VARCHAR(400), author VARCHAR(400));
- Insira manualmente usuários no banco de dados
- entre no venv navegando até a pasta e executando  '. bin/activate'
- determine o app do flask executando 'export FLASK_APP=hello.py'
- inicie o site executando 'flask run'
