class Processor:
    def __init__(self):
        self.memory = []      # Память машины
        self.stack = []       # Стек
        self.counter = 0      # Счетчик команд
        self.register = 0     # Регистр-счетчик
        self.commands_mem = []
        self.running = True

    def load_program(self, program):
        """Загрузка программы в память команд."""
        self.commands_mem = program

    def load_data(self, data):
        """Загрузка данных в память данных."""
        self.memory = data

    def fetch(self):
        """Извлечение команды из памяти."""
        if self.counter < len(self.commands_mem):
            instruction = self.commands_mem[self.counter]
            self.counter += 1
            return instruction
        else:
            self.running = False
            return None

    def execute(self, instruction):
        command = (instruction >> 24) & 0xFF
        label = (instruction >> 16) & 0xFF
        print(f"command: {command}, label: {label}")
        if command == 0:
            print("PUSH")
            print(self.counter)
            print(self.commands_mem[self.counter] >> 24)
            value = self.commands_mem[self.counter] >> 24
            self.stack.append(value)
            self.counter += 1
        elif command == 1:
            if self.stack:
                address = self.stack.pop()
                self.stack.append(self.memory[address])
        elif command == 2:
            self.register = self.stack.pop()
        elif command == 3:
            self.stack.append(self.stack[-1])
        elif command == 4:
            b = self.register
            a = self.stack.pop()
            self.register = a if a > b else b
        elif command == 5:
            self.stack[-1] -= 1
        elif command == 6:
            if self.stack[-1] == 0:
                self.counter = label
        elif command == 7:
            self.counter = label
        elif command == 8:
            self.running = False
        else:
            raise ValueError(f"Unknown command: {command}")

    def run(self):
        """Запуск выполнения программы."""
        while self.running:
            instruction = self.fetch()
            self.execute(instruction)
            self.dump()
            print("-------------------------------------")

    def dump(self):
        """Вывод состояния процессора."""
        print(f"PC: {self.counter}\nRAM: {self.memory[:16]}\nSTACK: {self.stack}\nACC: {self.register}\n===========")
