"""
Sistema de Gerenciamento de Estoque
-----------------------------------
Este sistema permite gerenciar o estoque de produtos com as seguintes funcionalidades:
- Cadastro de produtos (adicionar, remover, editar)
- Controle de estoque (entrada e saída de produtos)
- Consulta de produtos (por nome, categoria ou ID)
- Geração de relatórios
"""


import os
import time
import json
from datetime import datetime


# Constantes
ARQUIVO_ESTOQUE = "estoque.json"
ARQUIVO_HISTORICO = "historico.json"
ESTOQUE_MINIMO = 5  # Quantidade mínima para alertas


# Funções auxiliares
def limpar_tela():
    """Limpa a tela do terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    """Pausa a execução até que o usuário pressione Enter."""
    input("\nPressione Enter para continuar...")


def formatar_moeda(valor):
    """Formata um valor como moeda (R$)."""
    return f"R$ {valor:.2f}"


def salvar_dados(produtos):
    """Salva os produtos em um arquivo JSON."""
    with open(ARQUIVO_ESTOQUE, 'w', encoding='utf-8') as arquivo:
        json.dump(produtos, arquivo, indent=4, ensure_ascii=False)


def carregar_dados():
    """Carrega os produtos do arquivo JSON."""
    try:
        with open(ARQUIVO_ESTOQUE, 'r', encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver vazio/corrompido, retorna uma lista vazia
        return []


def salvar_historico(operacao):
    """Salva operações no histórico."""
    try:
        with open(ARQUIVO_HISTORICO, 'r', encoding='utf-8') as arquivo:
            historico = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        historico = []
    
    # Adiciona timestamp à operação
    operacao['timestamp'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    historico.append(operacao)
    
    with open(ARQUIVO_HISTORICO, 'w', encoding='utf-8') as arquivo:
        json.dump(historico, arquivo, indent=4, ensure_ascii=False)


def exibir_cabecalho(titulo):
    """Exibe um cabeçalho formatado."""
    limpar_tela()
    print("=" * 60)
    print(titulo.center(60))
    print("=" * 60)
    print()


def validar_numero(mensagem, tipo=float):
    """Valida entrada numérica do usuário."""
    while True:
        try:
            valor = tipo(input(mensagem))
            return valor
        except ValueError:
            print("Erro: Valor inválido. Tente novamente.")


def obter_proximo_id(produtos):
    """Obtém o próximo ID disponível."""
    if not produtos:
        return 1
    return max(int(produto['id']) for produto in produtos) + 1




# Funções de cadastro de produtos
def adicionar_produto(produtos):
    """Adiciona um novo produto ao estoque."""
    exibir_cabecalho("ADICIONAR NOVO PRODUTO")
    
    # Gera ID automaticamente
    id_produto = obter_proximo_id(produtos)
    
    nome = input("Nome do produto: ").strip()
    while not nome:
        print("O nome não pode estar vazio.")
        nome = input("Nome do produto: ").strip()
    
    # Verifica se já existe produto com este nome
    if any(produto['nome'].lower() == nome.lower() for produto in produtos):
        print(f"\nAVISO: Já existe um produto com o nome '{nome}'.")
        if input("Deseja continuar mesmo assim? (s/n): ").lower() != 's':
            return
    
    categoria = input("Categoria: ").strip()
    while not categoria:
        print("A categoria não pode estar vazia.")
        categoria = input("Categoria: ").strip()
    
    quantidade = validar_numero("Quantidade inicial em estoque: ", int)
    while quantidade < 0:
        print("A quantidade não pode ser negativa.")
        quantidade = validar_numero("Quantidade inicial em estoque: ", int)
    
    preco = validar_numero("Preço (R$): ")
    while preco <= 0:
        print("O preço deve ser maior que zero.")
        preco = validar_numero("Preço (R$): ")
    
    novo_produto = {
        'id': id_produto,
        'nome': nome,
        'categoria': categoria,
        'quantidade': quantidade,
        'preco': preco
    }
    
    produtos.append(novo_produto)
    salvar_dados(produtos)
    
    # Registra no histórico
    salvar_historico({
        'tipo': 'cadastro',
        'produto_id': id_produto,
        'produto_nome': nome,
        'detalhes': f"Produto cadastrado com {quantidade} unidades"
    })
    
    print(f"\nProduto '{nome}' adicionado com sucesso!")
    pausar()


def remover_produto(produtos):
    """Remove um produto do estoque."""
    exibir_cabecalho("REMOVER PRODUTO")
    
    if not produtos:
        print("Não há produtos cadastrados.")
        pausar()
        return
    
    id_produto = validar_numero("ID do produto que deseja remover (0 para cancelar): ", int)
    if id_produto == 0:
        return
    
    # Procura o produto pelo ID
    for i, produto in enumerate(produtos):
        if produto['id'] == id_produto:
            nome = produto['nome']
            
            print(f"\nDetalhes do produto a ser removido:")
            print(f"Nome: {nome}")
            print(f"Categoria: {produto['categoria']}")
            print(f"Quantidade: {produto['quantidade']}")
            print(f"Preço: {formatar_moeda(produto['preco'])}")
            
            confirmacao = input("\nTem certeza que deseja remover este produto? (s/n): ")
            if confirmacao.lower() == 's':
                produtos.pop(i)
                salvar_dados(produtos)
                
                # Registra no histórico
                salvar_historico({
                    'tipo': 'remocao',
                    'produto_id': id_produto,
                    'produto_nome': nome,
                    'detalhes': "Produto removido do sistema"
                })
                
                print(f"\nProduto '{nome}' removido com sucesso!")
            else:
                print("\nOperação cancelada.")
            
            pausar()
            return
    
    print(f"\nProduto com ID {id_produto} não encontrado.")
    pausar()


def editar_produto(produtos):
    """Edita um produto existente."""
    exibir_cabecalho("EDITAR PRODUTO")
    
    if not produtos:
        print("Não há produtos cadastrados.")
        pausar()
        return
    
    id_produto = validar_numero("ID do produto que deseja editar (0 para cancelar): ", int)
    if id_produto == 0:
        return
    
    # Procura o produto pelo ID
    for produto in produtos:
        if produto['id'] == id_produto:
            print(f"\nEditando produto: {produto['nome']}")
            print("Deixe em branco para manter o valor atual.")
            
            nome = input(f"Nome [{produto['nome']}]: ").strip()
            if nome and nome != produto['nome']:
                # Verifica se já existe outro produto com este nome
                if any(p['nome'].lower() == nome.lower() and p['id'] != id_produto for p in produtos):
                    print(f"\nAVISO: Já existe outro produto com o nome '{nome}'.")
                    if input("Deseja continuar mesmo assim? (s/n): ").lower() != 's':
                        return
                produto['nome'] = nome
            
            categoria = input(f"Categoria [{produto['categoria']}]: ").strip()
            if categoria:
                produto['categoria'] = categoria
            
            # Não permiti editar a quantidade diretamente aqui, isso deve ser feito via controle de estoque
            
            preco_str = input(f"Preço [{formatar_moeda(produto['preco'])}]: ").strip()
            if preco_str:
                try:
                    preco = float(preco_str)
                    if preco <= 0:
                        print("O preço deve ser maior que zero. Mantendo o valor atual.")
                    else:
                        produto['preco'] = preco
                except ValueError:
                    print("Valor inválido. Mantendo o preço atual.")
            
            salvar_dados(produtos)
            
            # Registra no histórico
            salvar_historico({
                'tipo': 'edicao',
                'produto_id': id_produto,
                'produto_nome': produto['nome'],
                'detalhes': "Informações do produto atualizadas"
            })
            
            print(f"\nProduto atualizado com sucesso!")
            pausar()
            return
    
    print(f"\nProduto com ID {id_produto} não encontrado.")
    pausar()




# Funções de controle de estoque
def registrar_movimento(produtos, tipo_movimento):
    """Registra entrada ou saída de produtos."""
    titulo = "REGISTRAR ENTRADA DE PRODUTOS" if tipo_movimento == "entrada" else "REGISTRAR SAÍDA DE PRODUTOS"
    exibir_cabecalho(titulo)
    
    if not produtos:
        print("Não há produtos cadastrados.")
        pausar()
        return
    
    id_produto = validar_numero("ID do produto (0 para cancelar): ", int)
    if id_produto == 0:
        return
    
    # Procura o produto pelo ID
    for produto in produtos:
        if produto['id'] == id_produto:
            print(f"\nProduto: {produto['nome']}")
            print(f"Quantidade atual em estoque: {produto['quantidade']}")
            
            quantidade = validar_numero(f"Quantidade para {tipo_movimento}: ", int)
            
            if quantidade <= 0:
                print(f"A quantidade deve ser maior que zero.")
                pausar()
                return
            
            if tipo_movimento == "saida" and quantidade > produto['quantidade']:
                print(f"ERRO: Quantidade insuficiente em estoque. Disponível: {produto['quantidade']}")
                pausar()
                return
            
            # Atualiza a quantidade
            quantidade_anterior = produto['quantidade']
            
            if tipo_movimento == "entrada":
                produto['quantidade'] += quantidade
                mensagem = f"Entrada de {quantidade} unidades registrada."
            else:  # saída
                produto['quantidade'] -= quantidade
                mensagem = f"Saída de {quantidade} unidades registrada."
            
            salvar_dados(produtos)
            
            # Registra no histórico
            salvar_historico({
                'tipo': f'movimento_{tipo_movimento}',
                'produto_id': id_produto,
                'produto_nome': produto['nome'],
                'quantidade': quantidade,
                'quantidade_anterior': quantidade_anterior,
                'quantidade_atual': produto['quantidade'],
                'detalhes': mensagem
            })
            
            print(f"\n{mensagem}")
            print(f"Nova quantidade em estoque: {produto['quantidade']}")
            
            # Alerta de estoque baixo
            if produto['quantidade'] < ESTOQUE_MINIMO:
                print(f"\nALERTA: Estoque baixo para '{produto['nome']}'!")
                print(f"Quantidade atual ({produto['quantidade']}) está abaixo do mínimo recomendado ({ESTOQUE_MINIMO}).")
            
            pausar()
            return
    
    print(f"\nProduto com ID {id_produto} não encontrado.")
    pausar()




# Funções de consulta de produtos
def buscar_produto(produtos):
    """Busca produtos por nome, categoria ou ID."""
    exibir_cabecalho("BUSCAR PRODUTO")
    
    if not produtos:
        print("Não há produtos cadastrados.")
        pausar()
        return
    
    print("Opções de busca:")
    print("1. Buscar por ID")
    print("2. Buscar por Nome")
    print("3. Buscar por Categoria")
    print("0. Voltar")
    
    opcao = validar_numero("\nEscolha uma opção: ", int)
    
    if opcao == 0:
        return
    elif opcao == 1:
        # Busca por ID
        id_busca = validar_numero("Digite o ID do produto: ", int)
        resultados = [p for p in produtos if p['id'] == id_busca]
    elif opcao == 2:
        # Busca por Nome
        nome_busca = input("Digite o nome (ou parte do nome) do produto: ").strip().lower()
        resultados = [p for p in produtos if nome_busca in p['nome'].lower()]
    elif opcao == 3:
        # Busca por Categoria
        categoria_busca = input("Digite a categoria: ").strip().lower()
        resultados = [p for p in produtos if categoria_busca in p['categoria'].lower()]
    else:
        print("Opção inválida.")
        pausar()
        return
    
    if resultados:
        exibir_cabecalho(f"RESULTADOS DA BUSCA ({len(resultados)} produtos encontrados)")
        
        print(f"{'ID':<5} {'Nome':<30} {'Categoria':<20} {'Qtde':<8} {'Preço':<10}")
        print("-" * 75)
        
        for produto in resultados:
            print(f"{produto['id']:<5} {produto['nome'][:30]:<30} {produto['categoria'][:20]:<20} "
                  f"{produto['quantidade']:<8} {formatar_moeda(produto['preco']):<10}")
        
        print("\nDetalhes completos do primeiro resultado:")
        exibir_detalhes_produto(resultados[0])
        
        if len(resultados) > 1:
            print("\nPara ver detalhes de outros produtos, use a opção 'Visualizar Detalhes do Produto' no menu principal.")
    else:
        print("\nNenhum produto encontrado com os critérios especificados.")
    
    pausar()


def exibir_detalhes_produto(produto):
    """Exibe detalhes completos de um produto."""
    print("\nDetalhes do Produto:")
    print(f"ID: {produto['id']}")
    print(f"Nome: {produto['nome']}")
    print(f"Categoria: {produto['categoria']}")
    print(f"Quantidade em estoque: {produto['quantidade']} unidades")
    print(f"Preço unitário: {formatar_moeda(produto['preco'])}")
    print(f"Valor total em estoque: {formatar_moeda(produto['quantidade'] * produto['preco'])}")
    
    # Alerta de estoque baixo
    if produto['quantidade'] < ESTOQUE_MINIMO:
        print(f"\nALERTA: Estoque baixo! Quantidade abaixo do mínimo recomendado ({ESTOQUE_MINIMO}).")


def visualizar_detalhes(produtos):
    """Visualiza detalhes de um produto específico."""
    exibir_cabecalho("VISUALIZAR DETALHES DO PRODUTO")
    
    if not produtos:
        print("Não há produtos cadastrados.")
        pausar()
        return
    
    id_produto = validar_numero("Digite o ID do produto (0 para cancelar): ", int)
    if id_produto == 0:
        return
    
    for produto in produtos:
        if produto['id'] == id_produto:
            exibir_detalhes_produto(produto)
            pausar()
            return
    
    print(f"\nProduto com ID {id_produto} não encontrado.")
    pausar()




# Funções de relatórios
def listar_todos_produtos(produtos):
    """Lista todos os produtos cadastrados."""
    exibir_cabecalho("RELATÓRIO: TODOS OS PRODUTOS")
    
    if not produtos:
        print("Não há produtos cadastrados.")
        pausar()
        return
    
    print(f"Total de produtos cadastrados: {len(produtos)}")
    print(f"\n{'ID':<5} {'Nome':<30} {'Categoria':<20} {'Qtde':<8} {'Preço':<10}")
    print("-" * 75)
    
    for produto in produtos:
        # Alerta visual para produtos com estoque baixo
        alerta = " (!)" if produto['quantidade'] < ESTOQUE_MINIMO else ""
        
        print(f"{produto['id']:<5} {produto['nome'][:30]:<30} {produto['categoria'][:20]:<20} "
              f"{produto['quantidade']}{alerta:<8} {formatar_moeda(produto['preco']):<10}")
    
    # Calcula valor total do estoque
    valor_total = sum(p['quantidade'] * p['preco'] for p in produtos)
    print("\n" + "-" * 75)
    print(f"Valor total em estoque: {formatar_moeda(valor_total)}")
    
    pausar()


def listar_estoque_baixo(produtos):
    """Lista produtos com estoque abaixo do mínimo."""
    exibir_cabecalho("RELATÓRIO: PRODUTOS COM ESTOQUE BAIXO")
    
    if not produtos:
        print("Não há produtos cadastrados.")
        pausar()
        return
    
    produtos_baixo_estoque = [p for p in produtos if p['quantidade'] < ESTOQUE_MINIMO]
    
    if not produtos_baixo_estoque:
        print(f"Não há produtos com estoque abaixo do mínimo ({ESTOQUE_MINIMO}).")
        pausar()
        return
    
    print(f"Total de produtos com estoque baixo: {len(produtos_baixo_estoque)}")
    print(f"\n{'ID':<5} {'Nome':<30} {'Categoria':<20} {'Qtde':<8} {'Mínimo':<8}")
    print("-" * 75)
    
    for produto in produtos_baixo_estoque:
        print(f"{produto['id']:<5} {produto['nome'][:30]:<30} {produto['categoria'][:20]:<20} "
              f"{produto['quantidade']:<8} {ESTOQUE_MINIMO:<8}")
    
    print("\nAÇÃO RECOMENDADA: Faça reposição destes itens o mais breve possível.")
    pausar()


def listar_por_categoria(produtos):
    """Lista produtos agrupados por categoria."""
    exibir_cabecalho("RELATÓRIO: PRODUTOS POR CATEGORIA")
    
    if not produtos:
        print("Não há produtos cadastrados.")
        pausar()
        return
    
    # Obtém todas as categorias únicas
    categorias = sorted(set(p['categoria'] for p in produtos))
    
    for categoria in categorias:
        produtos_categoria = [p for p in produtos if p['categoria'] == categoria]
        
        print(f"\n=== Categoria: {categoria} ({len(produtos_categoria)} produtos) ===")
        print(f"{'ID':<5} {'Nome':<30} {'Qtde':<8} {'Preço':<10}")
        print("-" * 55)
        
        for produto in produtos_categoria:
            alerta = " (!)" if produto['quantidade'] < ESTOQUE_MINIMO else ""
            print(f"{produto['id']:<5} {produto['nome'][:30]:<30} "
                  f"{produto['quantidade']}{alerta:<8} {formatar_moeda(produto['preco']):<10}")
    
    pausar()


def ver_movimentacoes(produtos):
    """Exibe histórico de movimentações do estoque."""
    exibir_cabecalho("HISTÓRICO DE MOVIMENTAÇÕES")
    
    try:
        with open(ARQUIVO_HISTORICO, 'r', encoding='utf-8') as arquivo:
            historico = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Não há histórico de movimentações disponível.")
        pausar()
        return
    
    if not historico:
        print("Não há registros de movimentações.")
        pausar()
        return
    
    # Limita a exibição às últimas 20 movimentações
    ultimas_movimentacoes = historico[-20:] if len(historico) > 20 else historico
    
    print(f"Exibindo as {len(ultimas_movimentacoes)} movimentações mais recentes:")
    print(f"\n{'Data/Hora':<20} {'Tipo':<15} {'Produto':<25} {'Detalhes':<30}")
    print("-" * 90)
    
    for movimento in reversed(ultimas_movimentacoes):
        tipo = movimento['tipo'].replace('movimento_entrada', 'Entrada').replace('movimento_saida', 'Saída')
        tipo = tipo.replace('cadastro', 'Cadastro').replace('edicao', 'Edição').replace('remocao', 'Remoção')
        
        print(f"{movimento['timestamp']:<20} {tipo:<15} {movimento['produto_nome'][:25]:<25} {movimento['detalhes'][:30]:<30}")
    
    print(f"\nTotal de {len(historico)} movimentações no sistema.")
    pausar()




# Menu principal
def menu_principal():
    """Exibe o menu principal e gerencia as opções."""
    produtos = carregar_dados()
    
    while True:
        exibir_cabecalho("SISTEMA DE GERENCIAMENTO DE ESTOQUE")
        
        print("1. Cadastro de Produtos")
        print("2. Controle de Estoque")
        print("3. Consulta de Produtos")
        print("4. Relatórios")
        print("0. Sair do Sistema")
        
        opcao = validar_numero("\nEscolha uma opção: ", int)
        
        if opcao == 0:
            limpar_tela()
            print("Encerrando o sistema... Obrigado por utilizar!")
            time.sleep(1)
            break
        elif opcao == 1:
            menu_cadastro(produtos)
        elif opcao == 2:
            menu_controle_estoque(produtos)
        elif opcao == 3:
            menu_consulta(produtos)
        elif opcao == 4:
            menu_relatorios(produtos)
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)


def menu_cadastro(produtos):
    """Menu de cadastro de produtos."""
    while True:
        exibir_cabecalho("CADASTRO DE PRODUTOS")
        
        print("1. Adicionar Novo Produto")
        print("2. Editar Produto")
        print("3. Remover Produto")
        print("0. Voltar ao Menu Principal")
        
        opcao = validar_numero("\nEscolha uma opção: ", int)
        
        if opcao == 0:
            break
        elif opcao == 1:
            adicionar_produto(produtos)
        elif opcao == 2:
            editar_produto(produtos)
        elif opcao == 3:
            remover_produto(produtos)
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)


def menu_controle_estoque(produtos):
    """Menu de controle de estoque."""
    while True:
        exibir_cabecalho("CONTROLE DE ESTOQUE")
        
        print("1. Registrar Entrada de Produtos")
        print("2. Registrar Saída de Produtos")
        print("3. Visualizar Histórico de Movimentações")
        print("0. Voltar ao Menu Principal")
        
        opcao = validar_numero("\nEscolha uma opção: ", int)
        
        if opcao == 0:
            break
        elif opcao == 1:
            registrar_movimento(produtos, "entrada")
        elif opcao == 2:
            registrar_movimento(produtos, "saida")
        elif opcao == 3:
            ver_movimentacoes(produtos)
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)


def menu_consulta(produtos):
    """Menu de consulta de produtos."""
    while True:
        exibir_cabecalho("CONSULTA DE PRODUTOS")
        
        print("1. Buscar Produto")
        print("2. Visualizar Detalhes do Produto")
        print("0. Voltar ao Menu Principal")
        
        opcao = validar_numero("\nEscolha uma opção: ", int)
        
        if opcao == 0:
            break
        elif opcao == 1:
            buscar_produto(produtos)
        elif opcao == 2:
            visualizar_detalhes(produtos)
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)


def menu_relatorios(produtos):
    """Menu de relatórios."""
    while True:
        exibir_cabecalho("RELATÓRIOS")
        
        print("1. Listar Todos os Produtos")
        print("2. Produtos com Estoque Baixo")
        print("3. Produtos por Categoria")
        print("0. Voltar ao Menu Principal")
        
        opcao = validar_numero("\nEscolha uma opção: ", int)
        
        if opcao == 0:
            break
        elif opcao == 1:
            listar_todos_produtos(produtos)
        elif opcao == 2:
            listar_estoque_baixo(produtos)
        elif opcao == 3:
            listar_por_categoria(produtos)
        else:
            print("Opção inválida. Tente novamente.")
            time.sleep(1)




# Inicialização do sistema
if __name__ == "__main__":
    menu_principal()
