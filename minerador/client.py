import grpc
import hashlib
import random
import sys

import minerador_pb2
import minerador_pb2_grpc

def mine_challenge(challenge_val, base_str="solucao"):
    """
    Função para encontrar uma solução para o desafio localmente.
    Usa força bruta para encontrar um nonce que satisfaça o desafio.
    """
    print(f"Iniciando mineração para um desafio de {challenge_val} zeros...")
    sufixo_zeros = '0' * challenge_val
    nonce = 0
    while True:
        tentativa = f"{base_str}{nonce}"
        hash_obj = hashlib.sha1(tentativa.encode()).hexdigest()
        if hash_obj.endswith(sufixo_zeros):
            print(f"Solução encontrada! Nonce: {nonce}, Hash: {hash_obj}")
            return tentativa
        nonce += 1

def run(server_address, client_id):
    with grpc.insecure_channel(server_address) as channel:
        stub = minerador_pb2_grpc.MineradorStub(channel)

        while True:
            print("\n--- Menu do Minerador ---")
            print("1. getTransactionID")
            print("2. getChallenge")
            print("3. getTransactionStatus")
            print("4. getWinner")
            print("5. getSolution")
            print("6. Mine")
            print("7. Sair")

            escolha = input("Escolha uma opção: ")

            if escolha == '7':
                break
            
            try:
                if escolha == '1':
                    response = stub.getTransactionID(minerador_pb2.Empty())
                    print(f"ID da transação atual: {response.transactionID}")
                
                elif escolha in ['2', '3', '4', '5']:
                    t_id = int(input("Digite o TransactionID: "))
                    request = minerador_pb2.TransactionRequest(transactionID=t_id)
                    if escolha == '2':
                        response = stub.getChallenge(request)
                        print(f"Desafio: {response.challenge}" if response.challenge != -1 else "TransactionID inválido.")
                    elif escolha == '3':
                        response = stub.getTransactionStatus(request)
                        status_map = {0: "Resolvido", 1: "Pendente", -1: "Inválido"}
                        print(f"Status: {status_map.get(response.status, 'Desconhecido')}")
                    elif escolha == '4':
                        response = stub.getWinner(request)
                        print(f"Vencedor ClientID: {response.winnerID}")
                    elif escolha == '5':
                        response = stub.getSolution(request)
                        if response.status.status != -1:
                            print(f"Desafio: {response.challenge}, Solução: '{response.solution}'")
                        else:
                            print("TransactionID inválido.")

                elif escolha == '6':
                    # Passo 1: Buscar transactionID atual
                    id_resp = stub.getTransactionID(minerador_pb2.Empty())
                    t_id_atual = id_resp.transactionID
                    print(f"1. TransactionID atual para minerar: {t_id_atual}")

                    # Passo 2: Buscar o desafio
                    challenge_req = minerador_pb2.TransactionRequest(transactionID=t_id_atual)
                    challenge_resp = stub.getChallenge(challenge_req)
                    challenge = challenge_resp.challenge
                    print(f"2. Desafio associado: {challenge}")

                    # Passo 3: Minerar localmente
                    solucao_encontrada = mine_challenge(challenge)
                    print(f"3/4. Solução encontrada localmente: '{solucao_encontrada}'")
                    
                    # Passo 5: Submeter a solução
                    submit_req = minerador_pb2.SubmitRequest(transactionID=t_id_atual, clientID=client_id, solution=solucao_encontrada)
                    submit_resp = stub.submitChallenge(submit_req)
                    
                    # Passo 6: Decodificar resposta
                    result_map = {
                        1: "Solução VÁLIDA e aceita!",
                        0: "Solução INVÁLIDA!",
                        2: "Desafio JÁ FOI SOLUCIONADO por outro cliente.",
                        -1: "TransactionID se tornou INVÁLIDO durante a mineração."
                    }
                    print(f"5/6. Resposta do servidor: {result_map.get(submit_resp.result_code, 'Desconhecida')}")

                else:
                    print("Opção inválida.")
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")
            except grpc.RpcError as e:
                print(f"Erro de comunicação com o servidor: {e.details()}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python client.py <endereço_do_servidor>")
        sys.exit(1)
    
    server_addr = sys.argv[1]
    client_unique_id = random.randint(1000, 9999)
    print(f"Cliente iniciado com ID: {client_unique_id}")
    run(server_addr, client_unique_id)