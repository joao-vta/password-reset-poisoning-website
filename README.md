# host-header-private
Codigo Fonte de um site vulneravel a Host Header Attack.  
Instruções para uso local:
- Crie um venv
- Copie o codigo fonte
- Instale o mysqlconnector e o flask no venv com PIP
- Crie banco de dados e tabelas no mysql:
- - CREATE DATABASE siteHost;
- - CREATE TABLE siteHost.users (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, username VARCHAR(400), password VARCHAR(400), email VARCHAR(400), token VARCHAR(400));
- - CREATE TABLE siteHost.posts (id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY, titulo VARCHAR(400), conteudo VARCHAR(400), link VARCHAR(400), author VARCHAR(400));
- Insira manualmente usuários no banco de dados
- Entre no venv navegando até a pasta e executando  '. bin/activate'
- Especifique o app do flask executando 'export FLASK_APP=hello.py'
- - Opcionalmente, execute 'export FLASK_ENV=development' para ativar modo de desenvolvimento
- Inicie o site executando 'flask run'
