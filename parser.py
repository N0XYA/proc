class Parser:
    def __init__(self, file_path, processor):
        self.instruction_set = {
            "PUSH": 0,
            "READ": 1,
            "LDC": 2,
            "DUP": 3,
            "CMPC": 4,
            "DEC": 5,
            "JZ": 6,
            "JP": 7,
            "HLT": 8
        }
        self.labels = {}  # Для хранения меток и их адресов
        self.file_path = file_path
        self.processor = processor
        self.program = []
        self.data = []

    def assemble_command(self, command):
        """Преобразует строку команды в машинный код."""
        parts = command.split()
        opcode = self.instruction_set.get(parts[0], parts[0])
        addr1 = int(parts[1]) if len(parts) > 1 else 0
        return (int(opcode) << 24 | (addr1 << 16))

    def parse_data_section(self, lines):
        """Обрабатывает секцию данных."""
        for line in lines:
            if ':' in line:
                label, value = line.split(':')
                self.labels[label.strip()] = len(self.data)
                self.data.append(int(value.strip(), 2))
            else:
                self.data.append(int(line.strip(), 2))

    def replace_labels(self, line):
        """Заменяет метки на соответствующие адреса."""
        parts = line.split()
        for i, part in enumerate(parts):
            if part in self.labels:  # Заменяем метку на её адрес
                parts[i] = str(self.labels[part])
        return " ".join(parts)

    def run(self):
        """Запускает трансляцию программы с двухпроходной обработкой."""
        with open(self.file_path, "r") as file:
            lines = file.readlines()

        # Разделение на секции данных и кода
        data_section, code_section = [], []
        is_data_section = True
        for line in lines:
            line = line.split("#")[0].strip()  # Убираем комментарии
            if not line:
                continue
            if is_data_section and "START:" in line:
                is_data_section = False
            if is_data_section:
                data_section.append(line)
            else:
                code_section.append(line)

        # Первый проход: сбор меток
        current_address = 0
        for line in code_section:
            if ':' in line:  # Если есть метка
                label, rest = line.split(':', 1)
                self.labels[label.strip()] = current_address
                line = rest.strip()
            if line:  # Если строка не пустая
                current_address += 1

        # Второй проход: трансляция команд
        self.parse_data_section(data_section)

        for line in code_section:
            if ':' in line:  # Убираем метку, если она есть
                _, line = line.split(':', 1)
            if line:  # Если строка не пустая
                rep_labels = self.replace_labels(line.strip())
                self.program.append(self.assemble_command(rep_labels))
        # Загрузка данных и программы в процессор
        self.processor.load_data(self.data)
        self.processor.load_program(self.program)

        # Сохранение программы в машинном коде для отладки
        with open("assembled_program.txt", "w") as assembled_file:
            for instruction in self.program:
                assembled_file.write(f"{bin(instruction)[2:].zfill(32)}\n")

    def get_program(self):
        """Возвращает скомпилированную программу."""
        return self.program
