# Copyright 2021-2024 Zhijie Shi. All rights reserved. See LICENSE.txt.
# tag: 885524cea1934bb3ee410ddb185fa63e

from myhdl import * 

from hardware.register import RegisterE
from hardware.memory import Ram, Rom
from hardware.mux import Mux2
from hardware.gates import And2
from hardware.alu import ALU
from hardware.adder import Adder
from hardware.registerfile import RegisterFile

from sc_signals import RISCVSignals
from immgen import ImmGen 
from maincontrol import MainControl
from alucontrol import ALUControl

@block
def     RISCVCore(imem_data, dmem_data, rf, reset, clock, env):
    """
    All signals are input

    imem_data:   instruction memory. A Python dictionary
    dmem_data:   data memory. A Python dictionary
    rf:     register file. A list of 32 integers
    clock:  clock 
    reset:  reset
    env:    additonal info, mainly for controlling print

    env.done:   asserted when simulation is done
    """

    # find max and min of instruction addresses
    # always start from the first instruction in the instruction memory
    max_pc = max(imem_data.keys()) 
    init_pc = min(imem_data.keys()) 

    # signals
    sig = RISCVSignals(init_pc)

    ##### Do NOT change the lines above
    # instantiate hardware modules 
    # check the diagram, make sure nothing is missing
    # and signals are connected correctly
    # 
    # The memory modules are in hardware/memory.py
    # Use Rom for instruction memory and Ram for data memory
    # imem_data and dmem_data will be passed to memory as data

    # for example, PC register is instantiated with the following line
    # sig.signal1 is always 1, which means that PC is always updated in this
    # implementation
    u_PC = RegisterE(sig.PC, sig.NextPC, sig.signal1, clock, reset)

    # Instruction Memory
    u_Imem = Rom(sig.instruction, sig.PC, imem_data)

    #Main Control
    u_Main_control = MainControl(sig.opcode, sig.ALUOp, sig.ALUSrc, sig.Branch, sig.MemRead, sig.MemWrite, sig.MemtoReg, sig.RegWrite)

    #Registers
    u_Registers = RegisterFile(sig.ReadData1, sig.ReadData2, sig.rs1, sig.rs2, sig.rd, sig.WriteData, sig.RegWrite, rf, clock )

    #ImmGen
    u_Imm_Gen = ImmGen(sig.immediate, sig.instruction)

    #ALUControl
    u_ALU_Con = ALUControl(sig.ALUOp, sig.instr30, sig.funct3, sig.ALUOperation)

    #MUX1
    u_Mux1 = Mux2(sig.ALUInput2, sig.ReadData2, sig.immediate, sig.ALUSrc)

    #ALU
    u_ALU = ALU(sig.ALUResult, sig.Zero, sig.ReadData1, sig.ALUInput2, sig.ALUOperation)

    #Data Memory
    u_Data_Memory = Ram(sig.MemReadData, sig.ReadData2, sig.ALUResult, sig.MemRead, sig.MemWrite, dmem_data, clock)

    #MUX2
    u_Mux2 = Mux2(sig.WriteData, sig.ALUResult, sig.MemReadData, sig.MemtoReg)

    #Adder1
    u_Adder1 = Adder(sig.PC4, sig.PC, sig.Const4)

    #Adder2
    u_Adder2 = Adder(sig.BranchTarget, sig.PC, sig.immediate)

    #And
    u_and = And2(sig.PCSrc, sig.Branch, sig.Zero)

    #MUX3
    u_Mux3 = Mux2(sig.NextPC, sig.PC4, sig.BranchTarget, sig.PCSrc)

    ##### Do NOT change the lines below
    @always_comb
    def set_done():
        env.done.next = sig.PC > max_pc  

    # print at the negative edge. for simulation only 
    @always(clock.negedge)
    def print_logic():
        if env.print_enable:
            sig.print(env.cycle_number, env.print_option)

    return instances()

if __name__ == "__main__" :
    print("Error: Please start the simulation with rvsim.py")
    exit(1)
