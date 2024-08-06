import favorite_pb2
from google.protobuf.json_format import MessageToJson

def parse_protobuf(serialized_data):
    # Cria uma instância da mensagem FavoriteList
    favorite_list = favorite_pb2.FavoriteList()
    # Preenche a mensagem com os dados serializados
    favorite_list.ParseFromString(serialized_data)
    # Converte a mensagem para JSON
    return MessageToJson(favorite_list)

try:
    # Abra o arquivo protobuf para leitura binária
    with open('protobuf.pb', 'rb') as f:
        serialized_data = f.read()

    # Decodifica os dados e converte para JSON
    decoded_data = parse_protobuf(serialized_data)
    print(decoded_data)  # Exibe o resultado em JSON

except FileNotFoundError:
    print("O arquivo favorites.pb não foi encontrado. Verifique o nome e o local do arquivo.")
except Exception as e:
    print(f"Erro ao processar o arquivo protobuf: {e}")
