import hashlib
import datetime as date


# construtor para criar um bloco
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    # método que calcula o hash
    def calculate_hash(self):
        sha = hashlib.sha256()  # função da lib
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   str(self.data).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8'))
        return sha.hexdigest()  # converte para hexadecimal -> que é o formato do hash

# inicia a blockchain com um bloco 'gênesis' -> o primeiro bloco da lista
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
    
    # método que cria o primeiro bloco da chain    
    def create_genesis_block(self):
        return Block(0, date.datetime.now(), 'Genesis Block', '0')
    
    def add_block(self, new_block):
        new_block.previous_hash = self.chain[-1].hash  # atribui o hash do bloco anterior
        new_block.hash = new_block.calculate_hash()  # calcula o hash do novo bloco
        self.chain.append(new_block)  # adiciona o bloco à cadeia
        
    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # verifica se o hash atual é igual ao recalculado
            if current_block.hash != current_block.calculate_hash():
                return False
            # verifica se o hash do bloco anterior é válido
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True  # retorna True se todos os blocos forem válidos

# criação de uma nova blockchain
blockchain = Blockchain()

# adicionando blocos a blockchain
blockchain.add_block(Block(1, date.datetime.now(), 'Segundo bloco', blockchain.chain[-1].hash))
blockchain.add_block(Block(2, date.datetime.now(), 'Terceiro bloco', blockchain.chain[-1].hash))

# exibindo os blocos da blockchain
for block in blockchain.chain:
    print(f'Índice: {block.index}')
    print(f'Timestamp: {block.timestamp}')
    print(f'Dados: {block.data}')
    print(f'Hash Atual: {block.hash}')
    print(f'Hash Anterior: {block.previous_hash}')
    print('---')

# verificando se a blockchain e valida
print(f'Blockchain é válida? {blockchain.is_valid()}')
