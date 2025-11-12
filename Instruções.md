# Guia de Execução - Laboratório RPC
Este guia mostra os passos necessários para compilar e executar as aplicações de Calculadora e Minerador de Criptomoedas.
Recomendamos que possua a versão mais atualizada do Python em sua máquina e ativar o "PATH".
# Pré-requisitos
Antes de começar, você precisa ter o Python instalado. Depois, instale as bibliotecas gRPC com o comando abaixo no seu terminal:

```pip install grpcio grpcio-tools```

# Atividade 1: Calculadora
Siga os passos abaixo para executar a calculadora remota.

1. Navegue até a pasta da calculadora

   ```cd caminho/para/o/projeto/calculadora```

2. Gere os arquivos de código a partir do .proto

   ```python -m grpc_tools.protoc -I./proto --python_out=. --pyi_out=. --grpc_python_out=. ./proto/calculadora.proto```

3. Inicie o Servidor

No terminal atual, execute o comando:

```python server.py```

Deixe este terminal aberto. Ele precisa ficar rodando.

4. Inicie o cliente

Abra um novo terminal.

Navegue para a mesma pasta calculadora/.

Execute o comando, especificando o endereço do servidor:

```python client.py localhost:50051```

O menu da calculadora aparecerá e você poderá começar a interagir.

# Atividade 2: Minerador de Criptomoedas

Siga os passos para executar o protótipo de mineração.

1. Navegue até a pasta do minerador

	 ```cd caminho/para/o/projeto/minerador```

2. Gere os arquivos de código a partir do .proto

   ```python -m grpc_tools.protoc -I./proto --python_out=. --pyi_out=. --grpc_python_out=. ./proto/minerador.proto```

	 3. Inicie o Servidor

No terminal atual, execute o comando:

```python server.py```

Deixe este terminal aberto.

4. Inicie o Cliente

Abra um novo terminal (você pode abrir vários para simular múltiplos mineradores).

Navegue para a mesma pasta minerador/.

Execute o comando, especificando o endereço do servidor:

```python client.py localhost:50052```

O menu do minerador aparecerá e você poderá começar a interagir.
