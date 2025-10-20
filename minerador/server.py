import grpc
from concurrent import futures
import time
import random
import hashlib
import threading

import minerador_pb2
import minerador_pb2_grpc

# Classe para representar uma transação
class Transacao:
    def __init__(self, t_id, challenge):
        self.transactionID = t_id
        self.challenge = challenge
        self.solution = ""
        self.winner = -1 # -1 indica que não foi solucionado

# Servidor que implementa a lógica da mineração
class MineradorServicer(minerador_pb2_grpc.MineradorServicer):
    def __init__(self):
        self.tabela_transacoes = {}
        self.lock = threading.Lock()
        self.proximo_transaction_id = 0
        self._criar_novo_desafio()

    def _criar_novo_desafio(self):
        with self.lock:
            t_id = self.proximo_transaction_id
            # Desafio: número de zeros no final do hash SHA-1
            challenge = random.randint(1, 5) # Desafio de 1 a 5 para ser rápido
            self.tabela_transacoes[t_id] = Transacao(t_id, challenge)
            print(f"Novo desafio criado: TransactionID={t_id}, Challenge={challenge}")
            self.proximo_transaction_id += 1

    def getTransactionID(self, request, context):
        id_pendente = self.proximo_transaction_id - 1
        return minerador_pb2.TransactionIDResponse(transactionID=id_pendente)

    def getChallenge(self, request, context):
        t_id = request.transactionID
        if t_id in self.tabela_transacoes:
            return minerador_pb2.ChallengeResponse(challenge=self.tabela_transacoes[t_id].challenge)
        return minerador_pb2.ChallengeResponse(challenge=-1)

    def getTransactionStatus(self, request, context):
        t_id = request.transactionID
        if t_id in self.tabela_transacoes:
            transacao = self.tabela_transacoes[t_id]
            status = 1 if transacao.winner == -1 else 0 # 1 para pendente, 0 para resolvido
            return minerador_pb2.StatusResponse(status=status)
        return minerador_pb2.StatusResponse(status=-1) # Inválido

    def submitChallenge(self, request, context):
        t_id = request.transactionID
        with self.lock:
            if t_id not in self.tabela_transacoes:
                return minerador_pb2.SubmitResponse(result_code=-1) # transactionID inválida

            transacao = self.tabela_transacoes[t_id]
            if transacao.winner != -1:
                return minerador_pb2.SubmitResponse(result_code=2) # Já foi solucionado

            # Valida a solução
            hash_solution = hashlib.sha1(request.solution.encode()).hexdigest()
            challenge = transacao.challenge
            sufixo_zeros = '0' * challenge

            if hash_solution.endswith(sufixo_zeros):
                transacao.solution = request.solution
                transacao.winner = request.clientID
                print(f"Solução VÁLIDA recebida para T_ID={t_id} do ClienteID={request.clientID}")
                self._criar_novo_desafio() # Cria o próximo desafio
                return minerador_pb2.SubmitResponse(result_code=1) # Solução válida
            else:
                print(f"Solução INVÁLIDA recebida para T_ID={t_id}")
                return minerador_pb2.SubmitResponse(result_code=0) # Solução inválida
    
    def getWinner(self, request, context):
        t_id = request.transactionID
        if t_id in self.tabela_transacoes:
            transacao = self.tabela_transacoes[t_id]
            winner_id = transacao.winner if transacao.winner != -1 else 0
            return minerador_pb2.WinnerResponse(winnerID=winner_id)
        return minerador_pb2.WinnerResponse(winnerID=-1)

    def getSolution(self, request, context):
        t_id = request.transactionID
        if t_id in self.tabela_transacoes:
            transacao = self.tabela_transacoes[t_id]
            status_val = 1 if transacao.winner == -1 else 0
            status_resp = minerador_pb2.StatusResponse(status=status_val)
            return minerador_pb2.SolutionResponse(status=status_resp, solution=transacao.solution, challenge=transacao.challenge)
        
        # Transação inválida
        invalid_status = minerador_pb2.StatusResponse(status=-1)
        return minerador_pb2.SolutionResponse(status=invalid_status)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    minerador_pb2_grpc.add_MineradorServicer_to_server(MineradorServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Servidor de Mineração iniciado na porta 50052.")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()