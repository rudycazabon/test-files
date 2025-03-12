import sys

# Constants
EXIT = 0x00
INT_STORE = 0x01
INT_PRINT = 0x02
INT_TOSTRING = 0x03
INT_RANDOM = 0x04
JUMP_TO = 0x10
JUMP_Z = 0x11
JUMP_NZ = 0x12
XOR_OP = 0x20
ADD_OP = 0x21
SUB_OP = 0x22
MUL_OP = 0x23
DIV_OP = 0x24
INC_OP = 0x25
DEC_OP = 0x26
AND_OP = 0x27
OR_OP = 0x28
STRING_STORE = 0x30
STRING_PRINT = 0x31
STRING_CONCAT = 0x32
STRING_SYSTEM = 0x33
STRING_TOINT = 0x34
CMP_REG = 0x40
CMP_IMMEDIATE = 0x41
CMP_STRING = 0x42
IS_STRING = 0x43
IS_INTEGER = 0x44
NOP_OP = 0x50
REG_STORE = 0x51
PEEK = 0x60
POKE = 0x61
MEMCPY = 0x62
STACK_PUSH = 0x70
STACK_POP = 0x71
STACK_RET = 0x72
STACK_CALL = 0x73

def main(files):
    for file in files:
        labels = {}
        updates = []
        output = file.rsplit('.', 1)[0] + ".raw"
        
        with open(file, 'r') as infile, open(output, 'wb') as outfile:
            offset = 0

            for line in infile:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                if line.startswith(':'):
                    name = line[1:]
                    if name in labels:
                        print(f"WARNING: Label name '{name}' defined multiple times!")
                        print("         Picking first occurrence.")
                        print("         This is probably your bug.")
                    if name.startswith('0x') or name.isdigit():
                        print(f"WARNING: Label named '{name}' WILL be confused for an address")
                        print("         Strongly consider changing this")
                    labels[name] = offset
                
                elif line.startswith('store'):
                    parts = line.split(',')
                    reg = int(parts[0].split('#')[1])
                    if '"' in parts[1]:
                        str_val = parts[1].split('"')[1]
                        str_val = str_val.replace('\\n', '\n').replace('\\t', '\t')
                        len_val = len(str_val)
                        len1 = len_val % 256
                        len2 = (len_val - len1) // 256
                        outfile.write(bytes([STRING_STORE, reg, len1, len2]) + str_val.encode())
                        offset += 4 + len_val
                    elif parts[1].startswith('#'):
                        src = int(parts[1].split('#')[1])
                        outfile.write(bytes([REG_STORE, reg, src]))
                        offset += 3
                    else:
                        val = parts[1].strip()
                        if val.startswith('0x') or val.isdigit():
                            val = int(val, 16) if val.startswith('0x') else int(val)
                            if val > 65535:
                                raise ValueError("Int too large")
                            val1 = val % 256
                            val2 = (val - val1) // 256
                            outfile.write(bytes([INT_STORE, reg, val1, val2]))
                            offset += 4
                        else:
                            outfile.write(bytes([INT_STORE, reg, 0x00, 0x00]))
                            offset += 4
                            updates.append({'offset': offset - 2, 'label': val})
                
                elif line == 'exit':
                    outfile.write(bytes([EXIT]))
                    offset += 1
                elif line == 'nop':
                    outfile.write(bytes([NOP_OP]))
                    offset += 1
                elif line.startswith('print_int'):
                    reg = int(line.split('#')[1])
                    outfile.write(bytes([INT_PRINT, reg]))
                    offset += 2
                elif line.startswith('print_str'):
                    reg = int(line.split('#')[1])
                    outfile.write(bytes([STRING_PRINT, reg]))
                    offset += 2
                elif line.startswith('system'):
                    reg = int(line.split('#')[1])
                    outfile.write(bytes([STRING_SYSTEM, reg]))
                    offset += 2
                elif line.startswith(('goto', 'jmp', 'jmpz', 'jmpnz', 'call')):
                    parts = line.split()
                    type_ = parts[0]
                    dest = parts[1]
                    types = {'goto': JUMP_TO, 'jmp': JUMP_TO, 'jmpz': JUMP_Z, 'jmpnz': JUMP_NZ, 'call': STACK_CALL}
                    if dest.startswith('0x') or dest.isdigit():
                        dest = int(dest, 16) if dest.startswith('0x') else int(dest)
                        a1 = dest % 256
                        a2 = (dest - a1) // 256
                        outfile.write(bytes([types[type_], a1, a2]))
                        offset += 3
                    else:
                        outfile.write(bytes([types[type_], 0, 0]))
                        offset += 3
                        updates.append({'offset': offset - 2, 'label': dest})
                
                elif line.split()[0] in ('add', 'and', 'sub', 'mul', 'div', 'or', 'xor', 'concat'):
                    parts = line.split(',')
                    opr = line.split()[0]
                    dest = int(parts[0].split('#')[1])
                    src1 = int(parts[1].split('#')[1])
                    src2 = int(parts[2].split('#')[1])
                    maths = {'add': ADD_OP, 'and': AND_OP, 'or': OR_OP, 'sub': SUB_OP, 'mul': MUL_OP, 'div': DIV_OP, 'xor': XOR_OP, 'concat': STRING_CONCAT}
                    outfile.write(bytes([maths[opr], dest, src1, src2]))
                    offset += 4
                
                elif line.startswith('dec'):
                    reg = int(line.split('#')[1])
                    outfile.write(bytes([DEC_OP, reg]))
                    offset += 2
                elif line.startswith('inc'):
                    reg = int(line.split('#')[1])
                    outfile.write(bytes([INC_OP, reg]))
                    offset += 2
                elif line.startswith('int2string'):
                    reg = int(line.split('#')[1])
                    outfile.write(bytes([INT_TOSTRING, reg]))
                    offset += 2
                elif line.startswith('random'):
                    reg = int(line.split('#')[1])
                    outfile.write(bytes([INT_RANDOM, reg]))
                    offset += 2
                elif line.startswith('string2int'):
                    reg = int(line.split('#')[1])
                    outfile.write(bytes([STRING_TOINT, reg]))
                    offset += 2
                elif line.startswith('cmp'):
                    parts = line.split(',')
                    reg1 = int(parts[0].split('#')[1])
                    if '"' in parts[1]:
                        str_val = parts[1].split('"')[1]
                        len_val = len(str_val)
                        len1 = len_val % 256
                        len2 = (len_val - len1) // 256
                        outfile.write(bytes([CMP_STRING, reg1, len1, len2]) + str_val.encode())
                        offset += 4 + len_val
                    else:
                        val = parts[1].strip()
                        if val.startswith('0x') or val.isdigit():
                            val = int(val, 16) if val.startswith('0x') else int(val)
                            val1 = val % 256
                            val2 = (val - val1) // 256
                            outfile.write(bytes([CMP_IMMEDIATE, reg1, val1, val2]))
                            offset += 4
                        else:
                            reg2 = int(parts[1].split('#')[1])
                            outfile.write(bytes([CMP_REG, reg1, reg2]))
                            offset += 3
                
                elif line.startswith(('is_string', 'is_integer')):
                    parts = line.split('#')
                    type_ = parts[0].split('_')[1]
                    reg = int(parts[1])
                    if type_ == 'string':
                        outfile.write(bytes([IS_STRING, reg]))
                    elif type_ == 'integer':
                        outfile.write(bytes([IS_INTEGER, reg]))
                    offset += 2
                
                elif line.startswith('peek'):
                    parts = line.split(',')
                    reg = int(parts[0].split('#')[1])
                    addr = int(parts[1].split('#')[1])
                    outfile.write(bytes([PEEK, reg, addr]))
                    offset += 3
                elif line.startswith('poke'):
                    parts = line.split(',')
                    reg = int(parts[0].split('#')[1])
                    addr = int(parts[1].split('#')[1])
                    outfile.write(bytes([POKE, reg, addr]))
                    offset += 3
                elif line.startswith('memcpy'):
                    parts = line.split(',')
                    src = int(parts[0].split('#')[1])
                    dst = int(parts[1].split('#')[1])
                    len_ = int(parts[2].split('#')[1])
                    outfile.write(bytes([MEMCPY, src, dst, len_]))
                    offset += 4
                elif line.startswith(('push', 'pop')):
                    parts = line.split('#')
                    opr = parts[0].strip()
                    reg = int(parts[1])
                    if opr == 'push':
                        outfile.write(bytes([STACK_PUSH, reg]))
                    elif opr == 'pop':
                        outfile.write(bytes([STACK_POP, reg]))
                    offset += 2
                elif line == 'ret':
                    outfile.write(bytes([STACK_RET]))
                    offset += 1
                elif line.startswith(('db', 'data')):
                    parts = line.split()
                    data = parts[1]
                    for db in data.split(','):
                        db = db.strip()
                        if not db:
                            continue
                        if db.startswith('0x'):
                            db = int(db, 16)
                        else:
                            db = int(db)
                        if db > 255:
                            raise ValueError(f"Data too large for a byte: {db}")
                        outfile.write(bytes([db]))
                        offset += 1
                else:
                    print(f"WARNING UNKNOWN LINE: {line}")
            
            if offset < 1:
                print("WARNING: Didn't generate any code")
        
        if updates:
            with open(output, 'r+b') as tmpfile:
                for update in updates:
                    offset = update['offset']
                    label = update['label']
                    if label not in labels:
                        raise ValueError(f"No target for label '{label}' - Label not defined!")
                    target = labels[label]
                    t1 = target % 256
                    t2 = (target - t1) // 256
                    tmpfile.seek(offset)
                    tmpfile.write(bytes([t1, t2]))

if __name__ == "__main__":
    main(sys.argv[1:])