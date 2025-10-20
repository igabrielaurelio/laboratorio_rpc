import grpc
from concurrent import futures
import time

# Importar os módulos gerados
import calculadora_pb2
import calculadora_pb2_grpc

# Classe que implementa os serviços da calculadora
class CalculadoraServicer(calculadora_pb2_grpc.CalculadoraServicer):
    def Somar(self, request, context):
        resultado = request.num1 + request.num2
        print(f"Recebida requisição de soma: {request.num1} + {request.num2} = {resultado}")
        return calculadora_pb2.OperacaoResponse(resultado=resultado)

    def Subtrair(self, request, context):
        resultado = request.num1 - request.num2
        print(f"Recebida requisição de subtração: {request.num1} - {request.num2} = {resultado}")
        return calculadora_pb2.OperacaoResponse(resultado=resultado)

    def Multiplicar(self, request, context):
        resultado = request.num1 * request.num2
        print(f"Recebida requisição de multiplicação: {request.num1} * {request.num2} = {resultado}")
        return calculadora_pb2.OperacaoResponse(resultado=resultado)

    def Dividir(self, request, context):
        if request.num2 == 0:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Divisão por zero não é permitida.")
            return calculadora_pb2.OperacaoResponse()
        resultado = request.num1 / request.num2
        print(f"Recebida requisição de divisão: {request.num1} / {request.num2} = {resultado}")
        return calculadora_pb2.OperacaoResponse(resultado=resultado)

# Função para iniciar o servidor
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    calculadora_pb2_grpc.add_CalculadoraServicer_to_server(CalculadoraServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Servidor da Calculadora iniciado na porta 50051.")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()