# WebApp - Projeto RPG

Aplicação Web em Python desenvolvida utilizando, principalmente, **Flask**, **Jinja2** e **SQL Alchemy**, com a finalidade de representar um **CRUD** para personagens de RPG.

## 📜 Desenvolvimento do projeto

O site foi projetado como um aprendizado e prática para o desenvolvimento de aplicações WEB utilizando Python e suas diversas bibliotecas que vem a facilitar o processo.
Desenvolvido na disciplina de Programação do segundo ano de **Técnico de Informática no Instituto Federal Catarinense - Campus Blumenau**.

A estrutura e funcionalidade do projeto foram planejadas para a disciplina de **Engenharia de Sofwate** e podem ser econtrados em:

* [Diagrama de Casos de Uso](https://drive.google.com/file/d/1f9U2Ca80Q15Q7hxFw4ebObOhR_xMrVkx/view?usp=sharing) - Divisão das persmissões e limitações de cada nível de usuário.
* [Diagrama de Classes - UML ](https://cdn.discordapp.com/attachments/419058354187403264/777969219946020884/unknown.png) - Utilizado como base para as funcionalidades e lógica das classes.
* [Requisitos Funcionais e Não-Funcionais](https://drive.google.com/file/d/1PWxJt2yFt8fbNCbKFLRKZgQPZ4GM0LYl/view?usp=sharing) - Requisitos levantados para o projeto.
* [Diagrama de Atividade para Login e Edição de Personagens ](https://drive.google.com/file/d/165e2T-PaWqprlfVevT9Vl2jfIrJ6jjBq/view?usp=sharing) - Base para o funcionamento  e restrições do login de usuários e da edição de personagens.


## 🛠 Download e Uso

A aplicação que está disponível para download contem todos os arquivos estruturais, alguns personagem e usuários já registrados para teste e experimentação. Porém, para ainda são necessáriso alguns passos para que tal projeto possa ser enviado à um servidor Linux propriamente dito.

Além de por comandos de terminal, o site pode ser iniciado em um servidor local através da execução do módulo "rodar.py"


### ✔️ Requerimentos

O projeto faz o uso, principalmente, das biblioteca Flask(e vários derivados menores) e SQL Aclhemy, porém tudo deve ser atendido com um simples pip install do arquivo requirements.txt, naturalmente presente no pacote.

Em caso de problemas ou dúvidas, apenas rode o seguinte no terminal, uma vez dentro da pasta:
```
python3 -m pip install -r requirements.txt
```

### ⁉️ Compreensão por terceiros

Como comentado anteriormente, o projeto apresenta todos os arquivos necessáriso para seu funcionamento livres para download e modificação, seguindo boas práticas de organização, identação, blueprints, etcs. ao decorrer de todos os arquivos. 

Toda a funcionalidade é comentada de forma que qualquer usuário consiga compreender as funções, modificá-las e/ou reutilizá-las.

## 🗃 Banco de Dados

A aplicação utiliza a biblioteca SQL Alchemy para o controle do Banco de Dados.
O download do projeto já vem com um bando de dados que contem alguns personagens, usuários e avaliações.
A estrutura e o dados podem ser visualizados com a utilização de uma série de programas, como o [DB Browser](https://sqlitebrowser.org/)

[![db1.png](https://i.ibb.co/JFZ8LX9/db1.png)](https://i.ibb.co/JFZ8LX9/db1.png)

## 🧑‍🤝‍🧑 Usuários

No sistema, existem basicamente três tipos de usuários: o não logado, o logado e o admin. 
Cada um possuí um nível próprio de acesso ao dados de outros usuários e dos personagens registrados(tal nível é representados ao lado do nome do usuário quando o mesmo é visto no site, vide screenshot abaixo).
Esses níveis de acesso podem ser melhor visualizados no * [Diagrama de Casos de Uso](https://drive.google.com/file/d/1f9U2Ca80Q15Q7hxFw4ebObOhR_xMrVkx/view?usp=sharing) do projeto.

Além disso, cada um tem seu perfil pessoal, com seus personagens registrados indexados.

[![perf1.png](https://i.ibb.co/H4VGw8H/perf1.png)](https://i.ibb.co/H4VGw8H/perf1.png)

### 🔑 Login e recuperação de senha

Como na maioria dos sites, o ProjetoRPG possuí um sistema de registro e login de usuários.
Caso algum venha a perder seus dados, o mesmo pode resquisitar um e-mail de redefinição de senha para o endereço informado no momento do registro da conta.

[![log1.png](https://i.ibb.co/W3h7TCd/log1.png)](https://i.ibb.co/W3h7TCd/log1.png)


## ⚔️ Estrutura de personagens

O site foi desenvolvido de maneira que funcionasse como um repositório para personages de RPG criados pela comunidade, tendo também perfis para os usuários e permitindo que cada personagem seja avaliado com um texto e nota.

Tal propósito já é visto na página inicial, aonde há uma seção com os personagens mais recentemente registrados, apresentando também seus dados principais e nota.

[![home1.png](https://i.ibb.co/HTTTrVt/home1.png)](https://i.ibb.co/HTTTrVt/home1.png)

### Registro de novos personagens e edição
Uma vez que o usuário está logado no site, ele pode registrar um personagem, informando uma série de dados e uma foto opcional, tal formulário é o mesmo que é utilizado para a posterior edição de algum personagem.

[![reg2.png](https://i.ibb.co/dJcwLQs/reg2.png)](https://i.ibb.co/dJcwLQs/reg2.png)

### 🔍 Sitema de busca

Para buscar por um personagem, pode-se escolher preencher uma série de campos sobre o mesmo e então receber todos os que corespondem ao dados.
(Os campos que não forem preenchidos, serão desconsiderados na pesquisa do DB uma vez que a querry será um like com "%%" - onde não há nenhuma dado entre os sinais de porcentagem)

[![pesq1.png](https://i.ibb.co/G2XQkgK/pesq1.png)](https://i.ibb.co/G2XQkgK/pesq1.png)

Tal processo de pesquisar seguinda alguns parametros informados, ou nãom, pode ser visto de forma resumida nessa parte do código:

```python
personagens = db.session.query(Personagem).filter(
                                                 Personagem.nome.like(f"%{form_procurar_pers.nome.data}%"),
                                                 Personagem.raca.like(f"%{form_procurar_pers.raca.data}%"),
                                                 Personagem.classe.like(f"%{form_procurar_pers.classe.data}%"),
                                                 ).from_self().paginate(page=1, per_page=9)
```

### Página específica do personagem

Ao clicar na imagem ou nome de um personagem, o usuário é redirecionado para uma página própria, com as informações mais detalhadas do mesmo e as avaliações feitas pela comunidade.
Caso ainda não tenha, o usuário pode avaliar o personagem, ou também editar caso já possua alguma.

[![rev1.png](https://i.ibb.co/VCrv7W2/rev1.png)](https://i.ibb.co/VCrv7W2/rev1.png)



