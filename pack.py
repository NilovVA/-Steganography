import datetime
import io

print("Введите путь до контейнер-файла: ", end='')
container_filepath = input()
container = open(container_filepath, "r").read()

print("Введите путь до файла со скрываемой фразой: ", end='')
to_hide_filepath = input()
to_hide = io.open(to_hide_filepath, "r").read()

to_hide_bits = ''
for ch in to_hide:
    char_bits = bin(int.from_bytes(bytes(ch, encoding='cp1251'), 'big'))[2:]
    char_bits = ''.join('0' for _ in range(8 - len(char_bits))) + char_bits
    to_hide_bits += char_bits

to_hide_len = len(to_hide_bits)

to_hide_len_bits = ''
for cifra in str(to_hide_len):
    len_bits = bin(int(cifra))[2:]
    len_bits = ''.join('0' for _ in range(8 - len(len_bits))) + len_bits
    to_hide_len_bits += len_bits
to_hide_len_bits = to_hide_len_bits + "00100000"


to_hide_bits = to_hide_len_bits + to_hide_bits


container_lines = container.split('\n')
container_size = len(container_lines)

if len(to_hide_bits) > container_size:
    print("Представленный контейнер слишком маленький, чтобы спрятать в него заданную фразу")
    exit(1)


output_filepath = container_filepath + "_" + str(datetime.datetime.now())
output_file = open(output_filepath, "w")


container_index = 0
for b in to_hide_bits:
    if b == '1':
        output_file.write(container_lines[container_index] + " " + "\n")
    else:
        output_file.write(container_lines[container_index] + "\n")
    output_file.flush()
    container_index += 1


output_file.writelines(container_lines[container_index:])

print("Путь до результирующего контейнера: " + output_filepath)