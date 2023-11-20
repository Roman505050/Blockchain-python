# -*- coding: utf-8 -*-

from hashlib import sha256
import json
from time import time




class Block:

    def __init__(self, timestamp=None, data=None):
        self.timestamp = timestamp or time()
        # У this.data повинна зберігатися інформація, на кшталт відомостей про транзакції.
        self.data = [] if data is None else data
        self.prevHash = None # Хеш минулого блока
        self.nonce = 0
        self.hash = self.getHash()

    def getHash(self):

        hash = sha256()
        hash.update(str(self.prevHash).encode('utf-8'))
        hash.update(str(self.timestamp).encode('utf-8'))
        hash.update(str(self.data).encode('utf-8'))
        hash.update(str(self.nonce).encode('utf-8'))
        return hash.hexdigest()

    def mine(self, difficulty):
        # Тут запускається цикл, що працює до тих пір, поки хеш не буде починатися з рядка
        # 0...000 довжини <difficulty>.
        a = 0
        while self.hash[:difficulty] != '0' * difficulty:
            print("process",a)
            a += 1
            # Інкрементуємо nonce, що дозволяє отримати абсолютно новий хеш.
            self.nonce += 1
            # Перераховуємо хеш блоку з урахуванням нового значення nonce.
            self.hash = self.getHash()

class Blockchain:

    def __init__(self):
        # У цій властивості будуть утримуватися всі блоки.
        self.chain = [Block(str(int(time())))]
        self.difficulty = 1
        self.blockTime = 30000

    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]

    def addBlock(self, block):
          # Оскільки ми додаємо новий блок, prevHash буде хешем попереднього останнього блоку.
        block.prevHash = self.getLastBlock().hash
        # Оскільки тепер в prevHash є значення, ми повинні перерахувати хеш блоку.
        block.hash = block.getHash()
        block.mine(self.difficulty)
        self.chain.append(block)

        self.difficulty += (-1, 1)[int(time()) - int(self.getLastBlock().timestamp) < self.blockTime]

    def isValid(self):
        # Перед перебором ланцюжка блоків необхідно встановити i в 1, оскільки до первинного блоку жодних блоків немає. В результаті ми починаємо з другого блоку.
        for i in range(1, len(self.chain)):
            currentBlock = self.chain[i]
            prevBlock = self.chain[i - 1]

            # Перевірка
            if (currentBlock.hash != currentBlock.getHash() or prevBlock.hash != currentBlock.prevHash):
                return False

        return True

    def __repr__(self):
        return json.dumps([{'data': item.data, 'timestamp': item.timestamp, 'nonce': item.nonce, 'hash': item.hash, 'prevHash': item.prevHash} for item in self.chain], indent=4)


JeChain = Blockchain()

# Додамо новий блок
JeChain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 1001})))
JeChain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 1001})))
JeChain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 1001})))
JeChain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 1001})))
JeChain.addBlock(Block(str(int(time())), ({"from": "John", "to": "Bob", "amount": 1001})))





# Вивід оновленого блокчейна
print(JeChain)