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
IF_ID_NEXT = IF_ID

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
ID_EX_NEXT = ID_EX

EX_MEM = { # Holds ALU result, branch target, data for storing, and destination register

} 
EX_MEM_NEXT = EX_MEM

MEM_WB = { # Stores data loaded from memory, ALU output, which are passed to register file for final write back
    
}
MEM_WB_NEXT = MEM_WB

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

    global ID_EX_NEXT # allow for modification of global from inside function

    ID_EX_NEXT["inst"]   = inst
    # ID_EX["pc"]   = IF_ID["pc"]
    ID_EX_NEXT["rs"]     = inst.rs
    ID_EX_NEXT["rt"]     = inst.rt
    ID_EX_NEXT["rd"]     = inst.rd
    ID_EX_NEXT["imm"]    = inst.imm
    ID_EX_NEXT["rs_val"] = registers.get(inst.rs)
    ID_EX_NEXT["rt_val"] = registers.get(inst.rt)

    ID_EX_NEXT["Branch"]   = 1 if branch else 0
    ID_EX_NEXT["ALUOp"]    = ALUOp_map.get(inst.op)
    ID_EX_NEXT["ALUSrc"]   = 1 if inst.op in {"addi","addui","subi","andi","ori","xori","lui", "lw","lb","lh","sw","sb","sh"} else 0
    ID_EX_NEXT["MemRead"]  = 1 if inst.op in {"lw", "lb", "lh"} else 0
    ID_EX_NEXT["MemToReg"] = 1 if inst.op in {"lw", "lb", "lh"} else 0
    ID_EX_NEXT["MemWrite"] = 1 if inst.op in {"sw", "sb", "sh"} else 0
    ID_EX_NEXT["RegDst"]   = 1 if inst.type == "R" else 0
    ID_EX_NEXT["RegWrite"] = 1 if inst.op in {
                                            "add","addu","sub","subu","and","or","xor","nor",
                                            "sll","sra","slr",
                                            "addi","addui","subi","andi","ori","xori","lui",
                                            "lw","lb","lh",
                                            "jal"
                                        } else 0


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

    pc_src = 1 if (branch and zero) else 0
    if pc_src:
        pc = branch_target

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
    MEM_WB_NEXT["pc_src"]        = pc_src        
    MEM_WB_NEXT["branch_target"] = branch_target 

def WB():
    
    # Get Results from previous Pipeline
    inst = MEM_WB.get("inst")
    memToReg = MEM_WB.get("MemToReg", 0) 
    aluResult = MEM_WB.get("alu_result", 0)
    memData = MEM_WB.get("mem_data", 0)
    destReg = MEM_WB.get("dest_reg", None)
    regWrite = MEM_WB.get("RegWrite", 0)
    pcSrc = MEM_WB.get("pc_src", 0)
    branchTarget = MEM_WB.get("branch_target", 0)

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

    # Printing test input values from ID_EX for debugging
    # print(f"EX | {ID_EX['inst'].op:4} | rs={ID_EX['rs']}({ID_EX['rs_val']}) "
      # f"rt={ID_EX['rt']}({ID_EX['rt_val']}) imm={ID_EX['imm']} "
      # f"ALUSrc={ID_EX['ALUSrc']}")

    # Operand selection
    A = ID_EX["rs_val"]

    # ALUSrc MUX: 1 → use immediate, 0 → use rt_val
    B = ID_EX["imm"] if ID_EX["ALUSrc"] else ID_EX["rt_val"]

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
    if ID_EX["Branch"]:
        imm = ID_EX["imm"] if ID_EX["imm"] is not None else 0
        branch_target = ID_EX["pc"] + imm
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

def run(program): 
    global IF_ID, IF_ID_NEXT, ID_EX, ID_EX_NEXT, EX_MEM, EX_MEM_NEXT, MEM_WB, MEM_WB_NEXT

    # while pc < len(program):
    for inst in program:
        WB()
        # MEM
        ID(inst) # passing raw instruction for test
        EX() 
        # IF

        IF_ID = IF_ID_NEXT 
        ID_EX = ID_EX_NEXT 
        EX_MEM = EX_MEM_NEXT
        MEM_WB = MEM_WB_NEXT

program = [
    "addi $t0, $zero, 1",
    "addi $t1, $zero, 2",   
    "add  $t2, $t1,  $t0",
    "add  $t3, $t2,  $t1",
    "lw   $t4, 4($t1)",
    "j 1000",
]

run(program)
