from datetime import datetime
from model.usuarios import Usuario  

class Tarefa:
    def __init__(self, 
                 codigo_tarefa: int = None,
                 titulo: str = None,
                 descricao: str = None,
                 data_criacao: datetime = None,
                 data_conclusao: datetime = None,
                 status: int = 0,  # 0 para pendente, 1 para concluída
                 usuario: Usuario = None
                 ):
        self.set_codigo_tarefa(codigo_tarefa)
        self.set_titulo(titulo)
        self.set_descricao(descricao)
        self.set_data_criacao(data_criacao or datetime.now())
        self.set_data_conclusao(data_conclusao)
        self.set_status(status)
        self.set_usuario(usuario)

    def set_codigo_tarefa(self, codigo_tarefa: int):
        self.codigo_tarefa = codigo_tarefa

    def set_titulo(self, titulo: str):
        self.titulo = titulo

    def set_descricao(self, descricao: str):
        self.descricao = descricao

    def set_data_criacao(self, data_criacao: datetime):
        self.data_criacao = data_criacao

    def set_data_conclusao(self, data_conclusao: datetime):
        self.data_conclusao = data_conclusao

    def set_status(self, status: int):
        self.status = status  
        if status == 1:  
            self.set_data_conclusao(datetime.now())

    def set_usuario(self, usuario: Usuario):
        self.usuario = usuario

    def get_codigo_tarefa(self) -> int:
        return self.codigo_tarefa

    def get_titulo(self) -> str:
        return self.titulo

    def get_descricao(self) -> str:
        return self.descricao

    def get_data_criacao(self) -> datetime:
        return self.data_criacao

    def get_data_conclusao(self) -> datetime:
        return self.data_conclusao

    def get_status(self) -> int:
        return self.status

    def get_usuario(self) -> Usuario:
        return self.usuario

    def to_string(self) -> str:
        return (f"Tarefa: {self.get_codigo_tarefa()} | "
                f"Título: {self.get_titulo()} | "
                f"Descrição: {self.get_descricao()} | "
                f"Data de Criação: {self.get_data_criacao()} | "
                f"Data de Conclusão: {self.get_data_conclusao().strftime('%Y-%m-%d %H:%M:%S') if self.get_data_conclusao() else 'N/A'} | "
                f"Status: {'Concluída' if self.get_status() == 1 else 'Pendente'} | "
                f"Usuário: {self.get_usuario().get_nome() if self.get_usuario() else 'N/A'}")
