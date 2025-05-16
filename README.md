# Projeto de Notas

---

## 🎯 Objetivo do Projeto

Este projeto tem como objetivo criar uma aplicação para fazer **anotações rápidas e organizadas**, permitindo **registrar, editar e excluir notas** com facilidade.

---

## 🚀 Como Utilizar o Projeto

### Banco de Dados  
Crie um banco de dados **PostgreSQL** na [Neon.tech](https://neon.tech/).

### Variáveis de Ambiente  
Configure as variáveis de ambiente no arquivo `.env` com as credenciais do banco de dados. Exemplo:

```env
DATABASE_URL=postgres://usuario:senha@endereco_do_banco:porta/nome_do_banco
```

```env
SECRET_KEY = senha_super_secretauhuhuh
```

### Tabelas no banco de dados
O sistema utiliza uma única tabela para armazenar as notas, aqui esta tabela:

**Table "public.NOTAS_GERAIS"**

| Coluna       | Tipo                    | Collation | Nullable | Default                      |
|--------------|-------------------------|-----------|----------|------------------------------|
| id           | integer                 |           | **not null** | generated always as identity |
| titulo       | character varying(60)   |           |          |                              |
| descricao    | character varying(1000) |           |          |                              |
| data_criacao | timestamp without time zone |       |          |                              |

**Índices:**

| Nome do Índice       | Tipo    | Colunas |
|----------------------|---------|---------|
| NOTAS_GERAIS_pkey    | PRIMARY KEY, btree | id |

## 📚 O que Foi Aprendido
- Manipulação de banco de dados PostgreSQL, desde a criação até a conexão com a aplicação
- Uso de variáveis de ambiente para configurar a aplicação de forma segura e flexível
- Conectividade com as requisições do Back-end utilizando javascript
- Criação de rotas dinâmicas utilizando Flask


