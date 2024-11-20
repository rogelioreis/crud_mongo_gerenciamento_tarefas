from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_usuario import Controller_Usuario
from controller.controller_tarefa import Controller_Tarefa
from conexion.mongo_queries import MongoQueries

# Inicializa as classes
mongo = MongoQueries()
mongo.connect()
tela_inicial = SplashScreen(mongo)
relatorio = Relatorio()
ctrl_usuario = Controller_Usuario()
ctrl_tarefa = Controller_Tarefa()

# Relatórios
def relatorios(opcao_relatorio: int = 0):
    if opcao_relatorio == 1:
        print("Relatório de Usuários")
        relatorio.get_relatorio_usuarios()
    elif opcao_relatorio == 2:
        print("Relatório de Tarefas")
        relatorio.get_relatorio_tarefas()
    elif opcao_relatorio == 3:
        print("Relatório de Tarefas Concluídas")
        relatorio.get_relatorio_tarefas_concluidas()
    elif opcao_relatorio == 4:
        print("Relatório de Qtde Tarefas por Usuario")
        relatorio.get_relatorio_tarefas_por_usuario()

# Inserir
def inserir(opcao_inserir: int = 0):
    if opcao_inserir == 1:
        ctrl_usuario.inserir_usuario()
    elif opcao_inserir == 2:
        ctrl_tarefa.inserir_tarefa()

    if(config.novamente()):
        inserir(opcao_inserir)


# Atualizar
def atualizar(opcao_atualizar: int = 0):
    if opcao_atualizar == 1:
        ctrl_usuario.atualizar_usuario()
    elif opcao_atualizar == 2:
        ctrl_tarefa.atualizar_tarefa()

    if(config.novamente()):
        atualizar(opcao_atualizar)

# Excluir
def excluir(opcao_excluir: int = 0):
    if opcao_excluir == 1:
        ctrl_usuario.excluir_usuario()
    elif opcao_excluir == 2:
        ctrl_tarefa.excluir_tarefa()
    
    if(config.novamente()):
        excluir(opcao_excluir)

# Principal
def run():  
    while True:
        tela_inicial.exibir()
        config.clear_console()

        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)
        
        if opcao == 1:  # Relatórios
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [0-4]: "))
            config.clear_console(1)
            relatorios(opcao_relatorio)
            config.clear_console(1)

        elif opcao == 2:  # Inserir
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-2]: "))
            config.clear_console(1)
            inserir(opcao_inserir=opcao_inserir)
            config.clear_console()

        elif opcao == 3:  # Atualizar
            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-2]: "))
            config.clear_console(1)
            atualizar(opcao_atualizar=opcao_atualizar)
            config.clear_console()

        elif opcao == 4:  # Excluir
            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-2]: "))
            config.clear_console(1)
            excluir(opcao_excluir=opcao_excluir)
            config.clear_console()

        elif opcao == 5:  # Sair
            tela_inicial.exibir()
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()
