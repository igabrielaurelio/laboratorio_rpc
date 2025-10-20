import grpc

# Importar os módulos gerados
import calculadora_pb2
import calculadora_pb2_grpc

def run():
    # Conecta-se ao servidor gRPC
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = calculadora_pb2_grpc.CalculadoraStub(channel)

        while True:
            print("\n--- Menu da Calculadora RPC ---")
            print("1. Somar")
            print("2. Subtrair")
            print("3. Multiplicar")
            print("4. Dividir")
            print("5. Sair")
            
            escolha = input("Escolha uma opção: ")

            if escolha == '5':
                break

            if escolha not in ['1', '2', '3', '4']:
                print("Opção inválida.")
                continue

            try:
                num1 = float(input("Digite o primeiro número: "))
                num2 = float(input("Digite o segundo número: "))
            except ValueError:
                print("Entrada inválida. Por favor, insira números.")
                continue

            request = calculadora_pb2.OperacaoRequest(num1=num1, num2=num2)

            try:
                if escolha == '1':
                    response = stub.Somar(request)
                elif escolha == '2':
                    response = stub.Subtrair(request)
                elif escolha == '3':
                    response = stub.Multiplicar(request)
                elif escolha == '4':
                    response = stub.Dividir(request)
                
                print(f"Resultado: {response.resultado}")

            except grpc.RpcError as e:
                print(f"Ocorreu um erro: {e.details()}")

if __name__ == '__main__':
    run()