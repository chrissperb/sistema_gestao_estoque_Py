# Sistema de Gerenciamento de Estoque

Um sistema completo de gerenciamento de estoque desenvolvido em Python, com interface via terminal.

## Visão Geral

Este sistema permite gerenciar o estoque de produtos de forma eficiente, fornecendo funcionalidades para cadastro, controle de estoque, consultas e relatórios, com persistência de dados em arquivos JSON.

## Funcionalidades

### 1. Cadastro de Produtos
- Adicionar novos produtos com informações detalhadas
- Editar informações de produtos existentes
- Remover produtos do sistema

### 2. Controle de Estoque
- Registrar entrada de produtos
- Registrar saída de produtos
- Atualização automática de quantidades
- Alertas para estoque baixo
- Histórico de movimentações

### 3. Consulta de Produtos
- Busca por ID, nome ou categoria
- Visualização detalhada de informações de produtos

### 4. Relatórios
- Listagem de todos os produtos
- Relatório de produtos com estoque baixo
- Listagem de produtos por categoria
- Cálculo de valor total em estoque

## Requisitos

- Python 3.6 ou superior
- Nenhuma biblioteca externa necessária (apenas bibliotecas padrão do Python)

## Instalação

1. Clone este repositório ou baixe o arquivo `sistema_gerenciamento_estoque.py`
2. Certifique-se de que o Python está instalado no seu sistema

## Como Usar

Execute o sistema com o comando:

```
python sistema_gerenciamento_estoque.py
```

### Primeira Execução

Na primeira execução, o sistema criará automaticamente os arquivos de dados necessários:
- `estoque.json` - Armazena informações dos produtos
- `historico.json` - Armazena o histórico de todas as movimentações

### Navegação pelo Sistema

O sistema apresenta um menu interativo com as seguintes opções principais:

1. **Cadastro de Produtos**
   - Adicionar, editar e remover produtos

2. **Controle de Estoque**
   - Registrar entradas e saídas de produtos
   - Visualizar histórico de movimentações

3. **Consulta de Produtos**
   - Buscar produtos
   - Visualizar detalhes de produtos específicos

4. **Relatórios**
   - Visualizar diferentes tipos de relatórios sobre o estoque

## Estrutura de Dados

Cada produto é representado por um dicionário com os seguintes campos:
- `id`: Identificador único do produto (número inteiro)
- `nome`: Nome do produto (string)
- `categoria`: Categoria do produto (string)
- `quantidade`: Quantidade atual em estoque (número inteiro)
- `preco`: Preço unitário do produto (número decimal)

## Recursos Técnicos

- **Persistência de dados** com arquivos JSON
- **Interface de terminal** amigável com menus interativos
- **Validação de entrada** para prevenir erros
- **Formatação de moeda** para valores monetários
- **Alertas visuais** para produtos com estoque baixo
- **Rastreamento de operações** com histórico detalhado

## Limitações

- Interface gráfica não disponível (apenas terminal)
- Não possui sistema de autenticação de usuários
- Não suporta múltiplos usuários simultâneos

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para enviar pull requests com melhorias ou correções.

## Possíveis Melhorias Futuras

- Adicionar interface gráfica
- Implementar sistema de autenticação
- Adicionar suporte a múltiplos usuários
- Implementar backup automático dos dados
- Adicionar suporte a banco de dados SQL
- Criar relatórios mais avançados com gráficos

## Autor

Christian Sperb

## Licença

Este projeto está licenciado sob a Licença MIT - consulte o arquivo LICENSE para obter detalhes.
