# Sistema de Gerenciamento de Tarefas

### Trabalho academico de Banco de Dados

Um sistema de controle de tarefas e usuários, com relatórios de tarefas concluídas e tempo gasto.

### Projeto criado por:
- Rogelio Soares Reis Filho
- Jordhan Fernandes de Assis
- Mariana Lopes Ferreira
- Murilo da Silva Soares

### Passo a passo para rodar o programa no sistema linux
#### 3 - No terminal, caminhe até a pasta "src" do programa. Ex:
```shell
cd /caminho/para/projetos/gerenciamento-tarefas/src
```

#### 4 - O sistema exige que tabelas existam. Para criar as tabelas e registros execute o codigo:
```shell
python criar_colecoes_e_dados.py
```
#### Atenção: tendo em vista que esse projeto é continuidade do crud_oracle_gerenciamento_tarefas, é importante que as tabelas do Oracle existam e estejam preenchidas, pois o script criar_colecoes_e_dados.py irá realizar uma consulta em cada uma das tabelas e preencher as collections com os novos documents.

#### 5 - Para executar o programa execute o codigo do programa principal:
```shell
python principal.py
```
### Testar conexão com o Banco:
```shell
python test.py
```
### Para deletar as tabelas caso necessario:
```shell
python deletar_tabelas.py
```

## Link video explicativo:
```shell
https://www.youtube.com/watch?v=s4mJg1oIwI0
```
