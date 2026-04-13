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
    "slr" : "R",
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
    "slri" : "I",
    "srai" : "I",
    "multi": "I",
    "divi" : "I",
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
stack = [0] * 1024 

# Pipeline registers (global variables)
IF_ID  = { # Holds fetched instruction and incremented PC (PC + 1)

} 

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

EX_MEM = { # Holds ALU result, branch target, data for storing, and destination register

} 

MEM_WB = { # Stores data loaded from memory, ALU output, which are passed to register file for final write back
    
}

def ID(raw_inst: str): # for testing-passing in raw instruction. in future it should pull it from global IF_ID
    # raw_inst = IF_ID["inst"]
    raw_inst = raw_inst.replace(",", "")
    raw_inst = raw_inst.replace("$", "")
    split_inst = raw_inst.split()
    inst = Instruction()

    inst.op = split_inst[0]
    type = instruction_type_map.get(split_inst[0])
    inst.type = type

    if type == "R":  # rd, rs, rt
        inst.rd   = split_inst[1]
        inst.rs   = split_inst[2]
        inst.rt   = split_inst[3]
    elif type == "I": # rt, rs, imm
        if inst.op not in {"lw", "lb", "lh", "sw", "sb", "sh"}:
            inst.rt   = split_inst[1]
            inst.rs   = split_inst[2]
            inst.imm  = int(split_inst[3])
        else:
            inst.rt     = split_inst[1]
            offset_base = split_inst[2]
            imm_part    = offset_base[:offset_base.index("(")]
            rs_part     = offset_base[offset_base.index("(")+1 : offset_base.index(")")]
            inst.imm    = int(imm_part)
            inst.rs     = rs_part
    elif type == "J":
        inst.addr = int(split_inst[1])

    branch = inst.op in {"beq", "bne", "bgez", "bgtz", "blez", "bltz", "bgt", "blt", "bge", "ble"}

    global ID_EX # allow for modification of global from inside function

    ID_EX["inst"]   = inst
    # ID_EX["pc"]   = IF_ID["pc"]
    ID_EX["rs"]     = inst.rs
    ID_EX["rt"]     = inst.rt
    ID_EX["rd"]     = inst.rd
    ID_EX["imm"]    = inst.imm
    ID_EX["rs_val"] = registers.get(inst.rs)
    ID_EX["rt_val"] = registers.get(inst.rt)

    ID_EX["Branch"]   = 1 if branch else 0
    ID_EX["ALUOp"]    = ALUOp_map.get(inst.op)
    ID_EX["ALUSrc"]   = 1 if inst.op in {"addi","addui","subi","andi","ori","xori","lui", "lw","lb","lh","sw","sb","sh"} else 0
    ID_EX["MemRead"]  = 1 if inst.op in {"lw", "lb", "lh"} else 0
    ID_EX["MemToReg"] = 1 if inst.op in {"lw", "lb", "lh"} else 0
    ID_EX["MemWrite"] = 1 if inst.op in {"sw", "sb", "sh"} else 0
    ID_EX["RegDst"]   = 1 if inst.type == "R" else 0
    ID_EX["RegWrite"] = 1 if inst.op in {
                                            "add","addu","sub","subu","and","or","xor","nor",
                                            "sll","sra","slr",
                                            "addi","addui","subi","andi","ori","xori","lui",
                                            "lw","lb","lh",
                                            "jal"
                                        } else 0

def run(program): 
    # while pc < len(program) * 4:
    for inst in program:
        # WB
        # MEM
        # EX
        ID(inst) # passing raw instruction for test
        # IF

program = [
    "addi $t0, $zero, 1",
    "addi $t1, $zero, 2",   
    "add  $t2, $t1,  $t0",
    "add  $t3, $t2,  $t1",
    "lw   $t4, 4($t1)",
    "j 1000",
]

run(program)
