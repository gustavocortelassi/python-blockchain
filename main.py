import hashlib
import datetime as date

# construtor para criar um agente
class Agent:
    def __init__(self, name):
        self.name = name

    def create_block(self, blockchain, data):
        index = len(blockchain.chain)
        timestamp = date.datetime.now()
        previous_hash = blockchain.chain[-1].hash
        new_block = Block(index, timestamp, data, previous_hash)
        blockchain.add_block(new_block, self)

    def validate_block(self, blockchain, block):
        return blockchain.is_valid()

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
    
    def add_block(self, new_block, agent):
        if self.is_valid():
            new_block.previous_hash = self.chain[-1].hash  # atribui o hash do bloco anterior
            new_block.hash = new_block.calculate_hash()  # calcula o hash do novo bloco
            self.chain.append(new_block)  # adiciona o bloco à cadeia
            print(f"Block added by {agent.name}")
        else:
            print(f"Failed to add block by {agent.name}")
            
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

# Criação da blockchain
blockchain = Blockchain()

# Criação dos agentes
agent1 = Agent("Alice")
agent2 = Agent("Bob")

# Agentes adicionam blocos
agent1.create_block(blockchain, 'Segundo bloco')
agent2.create_block(blockchain, 'Terceiro bloco')

# Exibindo os blocos da blockchain
for block in blockchain.chain:
    print(f'Índice: {block.index}')
    print(f'Timestamp: {block.timestamp}')
    print(f'Dados: {block.data}')
    print(f'Hash Atual: {block.hash}')
    print(f'Hash Anterior: {block.previous_hash}')
    print('---')

# Verificando se a blockchain é válida
print(f'Blockchain é válida? {blockchain.is_valid()}')

