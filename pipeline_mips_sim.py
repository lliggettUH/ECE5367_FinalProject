from dataclasses import dataclass
from typing      import Optional

@dataclass
class Instruction:
    type: str = None # R, I, or J
    op  : str = None
    rs  : Optional[str] = None
    rt  : Optional[str] = None
    rd  : Optional[str] = None # only if R type
    imm : Optional[int] = None # only if I type
    addr: Optional[int] = None # only if J tpye

    def __str__(self):
        if self.op is None:
            return "nop"

        # R-type:
        if self.type == "R":
            return f"{self.op} ${self.rd}, ${self.rs}, ${self.rt}"

        # I-type
        elif self.type == "I":
            if self.op in ("lw", "sw"):
                return f"{self.op} ${self.rt}, {self.imm}(${self.rs})"
            elif self.op in ("beq", "bne"):
                return f"{self.op} ${self.rs}, ${self.rt}, {self.imm}"
            else:
                return f"{self.op} ${self.rt}, ${self.rs}, {self.imm}"

        # J-type: j addr
        elif self.type == "J":
            return f"{self.op} {self.addr}"

        return "unknown"

instruction_type_map = {
    "add" : "R",
    "addu": "R",
    "sub" : "R",
    "subu": "R",
    "and" : "R",
    "or"  : "R",
    "xor" : "R",
    "nor" : "R",
    "sll" : "R",
    "srl" : "R",
    "sra" : "R",
    "mult": "R",
    "div" : "R",

    "addi" : "I",
    "addui": "I",
    "subi" : "I",
    "subui": "I",
    "andi" : "I",
    "ori"  : "I",
    "xori" : "I",
    "nori" : "I",
    "slli" : "I",
    "srli" : "I",
    "srai" : "I",
    "lui"  : "I",
    "lw"   : "I",
    "sw"   : "I",
    "lb"   : "I",
    "sb"   : "I",
    "lh"   : "I",
    "sh"   : "I",

    "b"      : "I",
    "bne"    : "I",
    "bgt"    : "I",
    "bge"    : "I",
    "blt"    : "I",
    "ble"    : "I",
    "beq"    : "I",

    "j"    : "J",
    "jal"  : "J",
    "jr"   : "J",
}

ALUOp_map = {
    "add":  "ADD",
    "addu": "ADD",
    "addi": "ADD",
    "addui":"ADD",
    "lw":   "ADD",
    "sw":   "ADD",
    "lb":   "ADD",
    "sb":   "ADD",
    "lh":   "ADD",
    "sh":   "ADD",
    "lui":  "ADD",

    "sub":  "SUB",
    "subu": "SUB",
    "beq":  "SUB",
    "bne":  "SUB",
    "blt":  "SUB",
    "bgt":  "SUB",
    "ble":  "SUB",
    "bge":  "SUB",

    "and":  "AND",
    "andi": "AND",

    "or":   "OR",
    "ori":  "OR",

    "xor":  "XOR",
    "xori": "XOR",
}

opcode_map = {
    0x02: "j",
    0x03: "jal",

    0x01: "REGIMM",
    0x04: "beq",
    0x05: "bne",

    0x08: "addi",
    0x09: "addiu",
    0x0A: "slti",
    0x0B: "sltiu",

    0x0C: "andi",
    0x0D: "ori",
    0x0E: "xori",
    0x0F: "lui",

    0x20: "lb",
    0x21: "lh",
    0x23: "lw",

    0x28: "sb",
    0x29: "sh",
    0x2B: "sw"
}

funct_map = {
    0x20: "add",
    0x21: "addu",
    0x22: "sub",
    0x23: "subu",

    0x24: "and",
    0x25: "or",
    0x26: "xor",
    0x27: "nor",

    0x2A: "slt",
    0x2B: "sltu",

    0x00: "sll",
    0x02: "srl",
    0x03: "sra",
    0x04: "sllv",
    0x06: "srlv",
    0x07: "srav",

    0x08: "jr",
    0x09: "jalr",

    0x18: "mult",
    0x19: "multu",
    0x1A: "div",
    0x1B: "divu",

    0x10: "mfhi",
    0x12: "mflo",
    0x11: "mthi",
    0x13: "mtlo"
}

regimm_map = {
    0x00: "bltz",
    0x01: "bgez",
    0x10: "bltzal",
    0x11: "bgezal"
}

reg_names = [
    "zero","at","v0","v1","a0","a1","a2","a3",
    "t0","t1","t2","t3","t4","t5","t6","t7",
    "s0","s1","s2","s3","s4","s5","s6","s7",
    "t8","t9","k0","k1","gp","sp","fp","ra"
]

registers = {
    "zero": 0, # constant 0
    "at"  : 0, # reserved
    "v0"  : 0, # expression evaluation and function results
    "v1"  : 0, # expression evaluation and function results
    "a0"  : 0, # arguments passed to functions
    "a1"  : 0, # arguments passed to functions
    "a2"  : 0, # arguments passed to functions
    "a3"  : 0, # arguments passed to functions
    "t0"  : 0, # temporary storage
    "t1"  : 0, # temporary storage 
    "t2"  : 0, # temporary storage
    "t3"  : 0, # temporary storage
    "t4"  : 0, # temporary storage
    "t5"  : 0, # temporary storage
    "t6"  : 0, # temporary storage
    "t7"  : 0, # temporary storage
    "s0"  : 0, # variable storage
    "s1"  : 0, # variable storage
    "s2"  : 0, # variable storage
    "s3"  : 0, # variable storage
    "s4"  : 0, # variable storage
    "s5"  : 0, # variable storage
    "s6"  : 0, # variable storage
    "s7"  : 0, # variable storage
    "t8"  : 0, # temporary storage
    "t9"  : 0, # temporary storage
    "k0"  : 0, # reserved
    "k1"  : 0, # reserved 
    "gp"  : 0, # global area pointer
    "sp"  : 0, # stack pointer
    "fp"  : 0, # frame pointer
    "ra"  : 0, # return address pointer
}
pc = 0
stallFlag = False
stack = [0] * 1024 

flush_ifid = 0
flush_idex = 0
taken = 0
forwardA = 0
forwardB = 0

branch_taken = 0
branch_target_reg = 0

IF_inst = None

# Pipeline registers (global variables)
IF_ID  = { # Holds fetched instruction and incremented PC (PC + 1)

} 
IF_ID_NEXT = IF_ID.copy()

ID_EX = { # Stores decoded instruction info
    "inst": None, 
    "pc": 0,
    "rs": None,
    "rt": None,
    "rd": None,
    "rs_val": 0,
    "rt_val": 0,
    "imm": 0,
    "RegDst": 0,
    "ALUSrc": 0,
    "ALUOp": None,
    "MemRead": 0,
    "MemWrite": 0,
    "RegWrite": 0,
    "MemToReg": 0,
    "Branch": 0,
} 
ID_EX_NEXT = ID_EX.copy()

EX_MEM = { # Holds ALU result, branch target, data for storing, and destination register

} 
EX_MEM_NEXT = EX_MEM.copy()

MEM_WB = { # Stores data loaded from memory, ALU output, which are passed to register file for final write back
    
}
MEM_WB_NEXT = MEM_WB.copy()

label_map = {}
cleaned_program = []

def map_labels(program):
    label_map = {}
    cleaned_program = []

    pc = 0
    for line in program:
        line = line.strip()

        if line.endswith(":"):
            label = line[:-1]
            label_map[label] = pc
        else:
            cleaned_program.append(line)
            pc += 1

    return cleaned_program, label_map

def is_binary_string(s):
    s = s.strip()
    return len(s) > 0 and all(c in "01" for c in s)

def split_machine_code(inst):
    inst = inst.replace("0x", "")
    if is_binary_string(inst):
        inst = int(inst, 2)
    else:
        inst = int(inst, 16)

    opcode = (inst & 0xFC000000) >> 26
    rs     = (inst & 0x03E00000) >> 21
    rt     = (inst & 0x001F0000) >> 16
    rd     = (inst & 0x0000F800) >> 11
    shamt  = (inst & 0x000007C0) >> 6
    funct  = (inst & 0x0000003F)
    target = inst & 0x03FFFFFF
    imm = inst & 0x0000FFFF
    if imm & 0x8000: # for signed
        imm -= 0x10000
    return opcode, rs, rt, rd, shamt, funct, target, imm

def machine_to_asm(opcode, rs, rt, rd, shamt, funct, target, imm):
    readable_inst = ""

    if opcode == 0x00:
        op = funct_map.get(funct, "unknown")

        rs_n = reg_names[rs]
        rt_n = reg_names[rt]
        rd_n = reg_names[rd]

        if op in ["sll", "srl", "sra"]:
            readable_inst = f"{op} {rd_n}, {rt_n}, {shamt}"

        elif op in ["mult", "div", "multu", "divu"]:
            readable_inst = f"{op} {rs_n}, {rt_n}"

        else:
            readable_inst = f"{op} {rd_n}, {rs_n}, {rt_n}"

    else:
        op_name = opcode_map.get(opcode, "unknown")

        if op_name in ["j", "jal"]:
            addr = target << 2
            readable_inst = f"{op_name} {hex(addr)}"

        elif op_name in ["lw", "sw", "lb", "sb", "lh", "sh"]:
            rt_n = reg_names[rt]   # value register
            rs_n = reg_names[rs]   # base register
            readable_inst = f"{op_name} {rt_n}, {imm}({rs_n})"

        elif op_name in ["addi", "addiu", "andi", "ori", "xori", "slti"]:
            rt_n = reg_names[rt]
            rs_n = reg_names[rs]
            readable_inst = f"{op_name} {rt_n}, {rs_n}, {imm}"

        elif op_name == "REGIMM":
            op = regimm_map.get(rt, "unknown")
            rs_n = reg_names[rs]
            readable_inst = f"{op} {rs_n}, {imm}"

        elif op_name in ["beq", "bne", "bgt", "bge", "blt", "ble"]:
            rs_n = reg_names[rs]
            rt_n = reg_names[rt]
            readable_inst = f"{op_name} {rs_n}, {rt_n}, {imm}"

        else:
            readable_inst = f"{op_name} (unhandled)"

    return readable_inst

def decode(raw_inst: str, label_map: dict) -> Instruction:
    if raw_inst is None:
        return None

    raw_inst = raw_inst.replace(",", "")
    raw_inst = raw_inst.replace("$", "")
    split_inst = raw_inst.split()
    inst = Instruction()

    inst.op   = split_inst[0]
    type      = instruction_type_map.get(split_inst[0])
    inst.type = type

    if type == "R":
        inst.rd = split_inst[1]
        inst.rs = split_inst[2]
        inst.rt = split_inst[3]
    elif type == "I":
        if inst.op in {"lw", "sw", "lb", "sb", "lh", "sh"}:
            inst.rt = split_inst[1]
            offset_base = split_inst[2]
            imm_part = offset_base[:offset_base.index("(")]
            rs_part  = offset_base[offset_base.index("(")+1 : offset_base.index(")")]
            inst.imm = int(imm_part)
            inst.rs  = rs_part
        # branch
        else:
            inst.rt = split_inst[1]
            inst.rs = split_inst[2]
            imm = split_inst[3]
            if imm in label_map:
                inst.imm = label_map[imm] - pc
            else:
                inst.imm = int(imm)
    elif type == "J":
        inst.addr = int(split_inst[1], 16) if split_inst[1].startswith("0x") else int(split_inst[1])

    return inst

def IF():
    global IF_ID_NEXT, pc, IF_inst, branch_taken, branch_target_reg

    if branch_taken:
        pc = branch_target_reg
        branch_taken = 0

    # If stall, don't update IF/ID
    if stallFlag:
        return

    elif pc < len(program) and not flush_ifid:
        IF_inst = program[pc]
        IF_ID_NEXT["inst"] = program[pc] 
        IF_ID_NEXT["pc"]   = pc + 1
        pc += 1
    else:
        IF_inst = None
        IF_ID_NEXT["inst"] = None  # pipeline bubble

def ID():
    global ID_EX_NEXT, pc, IF_ID_NEXT
    global flush_idex, flush_ifid

    raw_inst = IF_ID.get("inst")
    if raw_inst is None or flush_idex:  # bubble — clear the pipeline register and do nothing
        id_ex_nop()
        return

    inst = decode(raw_inst, label_map)

    findHazard(inst)

    # Insert bubble
    if stallFlag:
        id_ex_nop()
        IF_inst = raw_inst
        IF_ID_NEXT = IF_ID
        return

    branch = inst.op in {"beq", "bne", "bgez", "bgtz", "blez", "bltz", "bgt", "blt", "bge", "ble"}

    # Update all instruction values for next ID/EX pipeline register
    ID_EX_NEXT["inst"]     = inst
    ID_EX_NEXT["pc"]       = IF_ID["pc"] 
    ID_EX_NEXT["rs"]       = inst.rs
    ID_EX_NEXT["rt"]       = inst.rt
    ID_EX_NEXT["rd"]       = inst.rd
    ID_EX_NEXT["imm"]      = inst.imm
    ID_EX_NEXT["rs_val"]   = registers.get(inst.rs, 0)
    ID_EX_NEXT["rt_val"]   = registers.get(inst.rt, 0)

    # Update control signals of next ID/EX pipeline register
    ID_EX_NEXT["Branch"]   = 1 if branch else 0
    ID_EX_NEXT["ALUOp"]    = ALUOp_map.get(inst.op)
    ID_EX_NEXT["ALUSrc"]   = 1 if inst.op in {"addi","addui","subi","andi","ori","xori","lui",
                                               "lw","lb","lh","sw","sb","sh"} else 0
    ID_EX_NEXT["MemRead"]  = 1 if inst.op in {"lw", "lb", "lh"} else 0
    ID_EX_NEXT["MemToReg"] = 1 if inst.op in {"lw", "lb", "lh"} else 0
    ID_EX_NEXT["MemWrite"] = 1 if inst.op in {"sw", "sb", "sh"} else 0
    ID_EX_NEXT["RegDst"]   = 1 if inst.type == "R" else 0
    ID_EX_NEXT["RegWrite"] = 1 if inst.op in {
                                        "add","addu","sub","subu","and","or","xor","nor",
                                        "sll","sra","srl",
                                        "addi","addui","subi","andi","ori","xori","lui",
                                        "lw","lb","lh",
                                        "jal"
                                    } else 0
    
    if inst.op == "j":
        pc = inst.addr
        flush_ifid = 1
        flush_idex = 1
        IF_ID_NEXT["inst"] = None
        ID_EX_NEXT["inst"] = None
        return


def MEM(): 
    global MEM_WB_NEXT, stack, pc

    # grabbing results from previous pipeline output
    alu_result = EX_MEM.get("alu_result", 0)
    rt_val = EX_MEM.get("rt_val", 0)
    inst = EX_MEM.get("inst")
    branch_target = EX_MEM.get("branch_target", 0)

    mem_read = EX_MEM.get("MemRead",  0)
    mem_write  = EX_MEM.get("MemWrite", 0)
    reg_write = EX_MEM.get("RegWrite", 0)
    mem_to_reg = EX_MEM.get("MemToReg", 0)
    dest_reg = EX_MEM.get("dst_reg",  None)
    branch = EX_MEM.get("Branch",   0)
    zero = EX_MEM.get("zero",     0)
    mem_data = 0

    alu_result = EX_MEM.get("alu_result", 0)  # already fetched above

    if mem_read:
        addr = alu_result
        if addr >= 0 and addr < len(stack):
            mem_data = stack[addr]
        else:
            raise IndexError(f"MEM: Load address {addr} out of bounds")

    elif mem_write:
        addr = alu_result
        if addr >= 0 and addr < len(stack):
            stack[addr] = rt_val
        else:
            raise IndexError(f"MEM: Store address {addr} out of bounds")
        
    MEM_WB_NEXT["inst"]          = inst
    MEM_WB_NEXT["alu_result"]    = alu_result    # 4 WB if MemToReg = 0
    MEM_WB_NEXT["mem_data"]      = mem_data      # 4 WB if MemToReg = 1
    MEM_WB_NEXT["dest_reg"]      = dest_reg
    MEM_WB_NEXT["RegWrite"]      = reg_write
    MEM_WB_NEXT["MemToReg"]      = mem_to_reg
    # MEM_WB_NEXT["pc_src"]        = pc_src        
    MEM_WB_NEXT["branch_target"] = branch_target 

def WB():
    
    # Get Results from previous Pipeline
    inst = MEM_WB.get("inst")
    memToReg = MEM_WB.get("MemToReg", 0) 
    aluResult = MEM_WB.get("alu_result", 0)
    memData = MEM_WB.get("mem_data", 0)
    destReg = MEM_WB.get("dest_reg", None)
    regWrite = MEM_WB.get("RegWrite", 0)
    pcSrc = MEM_WB.get("pc_src", 0)                 # Still don't know what do w/ these 2
    branchTarget = MEM_WB.get("branch_target", 0)   #

    # Test part 1 (finding value in reg before write back)
    # print(f'register destReg, value {registers[destReg]}')

    if regWrite and destReg is not None:
        if destReg != "zero" and destReg != "at" and destReg != "k0" and destReg != "k1":
            if destReg != "gp" and destReg != "sp" and destReg != "fp" and destReg != "ra":   
                if memToReg:
                    registers[destReg] = memData
                else:
                    registers[destReg] = aluResult
    
    # Test part 2 (See if register was updated)
    #print(f'register destReg, value {registers[destReg]}')
    
def EX():
    global EX_MEM_NEXT

    def resolve_reg(reg, base_value):
        # EX/MEM has priority
        if EX_MEM.get("RegWrite") and EX_MEM.get("dst_reg") == reg and reg != "zero":
            return EX_MEM["alu_result"], 1

        # MEM/WB fallback
        if MEM_WB.get("RegWrite") and MEM_WB.get("dest_reg") == reg and reg != "zero":
            val = MEM_WB["mem_data"] if MEM_WB.get("MemToReg") else MEM_WB["alu_result"]
            return val, 2

        # register file
        return base_value, 0

    # Printing test input values from ID_EX for debugging
    # print(f"EX | {ID_EX['inst'].op:4} | rs={ID_EX['rs']}({ID_EX['rs_val']}) "
      # f"rt={ID_EX['rt']}({ID_EX['rt_val']}) imm={ID_EX['imm']} "
      # f"ALUSrc={ID_EX['ALUSrc']}")

    # Operand selection
    A = ID_EX["rs_val"]

    # ALUSrc MUX: 1 → use immediate, 0 → use rt_val
    B = ID_EX["imm"] if ID_EX["ALUSrc"] else ID_EX["rt_val"]

    # forwarding
    global forwardA, forwardB
    rs = ID_EX.get('rs')
    rt = ID_EX.get('rt')
    forwardA = 0
    forwardB = 0

    # ALUSrc first (only affects B base value)
    A_base = ID_EX["rs_val"]
    B_base = ID_EX["imm"] if ID_EX["ALUSrc"] else ID_EX["rt_val"]

    # resolve operands independently BUT consistently
    A, forwardA = resolve_reg(rs, A_base)

    if ID_EX["ALUSrc"]:
        B = B_base
        forwardB = 0
    else:
        B, forwardB = resolve_reg(rt, B_base)

    # RegDst MUX: 1 → rd (R-type), 0 → rt (I-type)
    dst_reg = ID_EX["rd"] if ID_EX["RegDst"] else ID_EX["rt"]

    # ALU
    op = ID_EX["ALUOp"]
    alu_result = 0

    if   op == "ADD": alu_result = A + B
    elif op == "SUB": alu_result = A - B
    elif op == "AND": alu_result = A & B
    elif op == "OR" : alu_result = A | B
    elif op == "XOR": alu_result = A ^ B
    elif op == "NOR": alu_result = ~(A | B)
    elif op == "SLL": alu_result = A << B
    elif op == "SRL": alu_result = A >> B 
    elif op == "SRA": alu_result = A >> B 
    # op is None for J-type (j, jal, jr) — alu_result stays 0

    zero = 1 if alu_result == 0 else 0        # zero flag used by branch logic in MEM

    # Branch target adder 
    # Runs in parallel with the ALU; MEM stage decides whether to use it
    # branch_target = ID_EX["pc"] + ID_EX["imm"] 
    global taken, flush_ifid, flush_idex, pc, branch_target_reg, branch_taken
    if ID_EX["Branch"]:
        imm = ID_EX["imm"] if ID_EX["imm"] is not None else 0
        branch_target = ID_EX["pc"] + imm

        op = ID_EX["inst"].op
        take = False
        if op == "beq" and zero == 1:
            take = True
        elif op == "bne" and zero == 0:
            take = True
        elif op == "bgt" and alu_result > 0:
            take = True
        elif op == "blt" and alu_result < 0:
            take = True
        elif op == "bge" and alu_result >= 0:
            take = True
        elif op == "ble" and alu_result <= 0:
            take = True
        if take:
            taken = 1
            branch_taken = 1
            branch_target_reg = branch_target
            flush_ifid = 1
            flush_idex = 1
    else:
        branch_target = 0

    # Write to EX_MEM 
    EX_MEM_NEXT["alu_result"]    = alu_result
    EX_MEM_NEXT["branch_target"] = branch_target
    EX_MEM_NEXT["zero"]          = zero
    EX_MEM_NEXT["rt_val"]        = ID_EX["rt_val"]   # store data passthrough (sw/sb/sh)
    EX_MEM_NEXT["dst_reg"]       = dst_reg

    # Control signals pass through to MEM and WB
    EX_MEM_NEXT["Branch"]        = ID_EX["Branch"]
    EX_MEM_NEXT["MemRead"]       = ID_EX["MemRead"]
    EX_MEM_NEXT["MemWrite"]      = ID_EX["MemWrite"]
    EX_MEM_NEXT["RegWrite"]      = ID_EX["RegWrite"]
    EX_MEM_NEXT["MemToReg"]      = ID_EX["MemToReg"]
    EX_MEM_NEXT["inst"]          = ID_EX["inst"]      # useful for debugging

    # print("EX result:", alu_result, "dest:", dst_reg)

# Check for Load-use hazard
def findHazard(inst):
    global stallFlag, ID_EX_NEXT

    stallFlag = False

    # Load hazard (need to stall for one cycle)
    producer = ID_EX.get("rt")     
    producer_memread = ID_EX.get("MemRead", 0)

    rs = inst.rs # same as IF_ID rs
    rt = inst.rt # same as IF_ID rt

    if producer_memread and producer is not None:
        if producer == rs or producer == rt and producer != 'zero':
            stallFlag = True

def id_ex_nop():
    global ID_EX_NEXT

    ID_EX_NEXT = {
    "inst": None,
    "rs": None,
    "rt": None,
    "rd": None,
    "imm": 0,
    "rs_val": 0,
    "rt_val": 0,
    "ALUOp": None,
    "RegWrite": 0,
    "MemRead": 0,
    "MemWrite": 0,
    "MemToReg": 0,
    "RegDst": 0,
    "ALUSrc": 0,
    "Branch": 0,
    "pc": 0
}
            
def format_inst(inst):
    if inst is None:
        return "nop"
    if isinstance(inst, str):
        parts = inst.split()
        if len(parts) == 0:
            return "nop"
        if len(parts) == 1:
            return parts[0]
        
        op = parts[0]
        operands = parts[1:]
        correct_operands = []

        for i in range(len(operands)):
            operands[i] = operands[i].replace(",", "")
            if operands[i].replace("$", "") in reg_names:
                correct_operands.append(f"${operands[i]}")
            else:
                correct_operands.append(operands[i])
            

        return f"{op} " + ", ".join(correct_operands)
    if isinstance(inst, Instruction):
        return str(inst)
    return inst 

def fmt_forward(forward: int) -> str:
    if forward == 0:
        return "ID/EX"
    elif forward == 1:
        return "EX/MEM"
    elif forward == 2:
        return "MEM/WB"

def run(output_file_name): 
    global IF_ID, IF_ID_NEXT, ID_EX, ID_EX_NEXT, EX_MEM, EX_MEM_NEXT, MEM_WB, MEM_WB_NEXT
    global taken, flush_idex, flush_ifid, forwardA, forwardB

    result = ""

    current_cycle = 1

    while True:
        WB()
        MEM()
        EX()
        ID()
        IF()

        # print(f"Cycle {current_cycle}")

        # print(f"IF  : {IF_inst if IF_inst is not None else "nop"}")
        # print(f"ID  : {IF_ID.get('inst') if IF_ID.get('inst') is not None else "nop"}")
        # print(f"EX  : {format_inst(ID_EX.get('inst'))}")
        # print(f"MEM : {format_inst(EX_MEM.get('inst'))}")
        # print(f"WB  : {format_inst(MEM_WB.get('inst'))}")
        # print(f"stall={stallFlag} flush_ifid={flush_ifid} flush_idex={flush_idex} taken={taken}")
        # print(f"forwardA={fmt_forward(forwardA)} forwardB={fmt_forward(forwardB)}")
        # # print(f"t4={registers.get("t4")}")
        # print(f"Next PC: 0x{(pc * 4):08x}\n")

        result += f"Cycle {current_cycle}\n"

        result += f"IF  : {IF_inst if IF_inst is not None else "nop"}\n"
        result += f"ID  : {IF_ID.get('inst') if IF_ID.get('inst') is not None else "nop"}\n"
        result += f"EX  : {format_inst(ID_EX.get('inst'))}\n"
        result += f"MEM : {format_inst(EX_MEM.get('inst'))}\n"
        result += f"WB  : {format_inst(MEM_WB.get('inst'))}\n"
        result += f"stall={stallFlag} flush_ifid={flush_ifid} flush_idex={flush_idex} taken={taken}\n"
        result += f"forwardA={fmt_forward(forwardA)} forwardB={fmt_forward(forwardB)}\n"
        # print(f"t4={registers.get("t4")}")
        result += f"Next PC: 0x{(pc * 4):08x}\n\n"

        # Update the pipeline registers
        IF_ID  = IF_ID_NEXT.copy()
        ID_EX  = ID_EX_NEXT.copy()
        EX_MEM = EX_MEM_NEXT.copy()
        MEM_WB = MEM_WB_NEXT.copy()

        taken = 0
        flush_ifid = 0
        flush_idex = 0

        current_cycle += 1

        # Condition means the program has completed
        if IF_ID.get('inst') is None and ID_EX.get('inst') is None and EX_MEM.get('inst') is None and MEM_WB.get('inst') is None:
            break

    with open(output_file_name, "w", encoding="utf-8") as file:
        file.write(result)

program = []

program_path = "test_program1.asm"

with open(program_path, "r") as f:
    program = f.readlines()

cleaned_program, label_map = map_labels(program)

# Clean instructions for parsing
for i in range(len(cleaned_program)):
    line = cleaned_program[i].strip()
    if line.startswith("0x") or is_binary_string(line): 
        cleaned_program[i] = machine_to_asm(*split_machine_code(line))
        cleaned_program[i] = cleaned_program[i].replace("\n", "")
        cleaned_program[i] = cleaned_program[i].replace(",", "")
        cleaned_program[i] = cleaned_program[i].replace("$", "")
    
# print(cleaned_program)
# print(label_map)

program = cleaned_program

run(program_path.replace(".asm", ".txt"))
