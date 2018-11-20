#******************************************************
#   ECE 366     Project 4
#       by: Jonathan Wacker     Base code authors: Trung Le, Weijing Rao
#   Objective: The code's objective is to read HEX 
#      MIPS code and the simulate the code. The DIC
#      and cycle number (for single, multicycle, and
#      pipeline) are also counted.
#******************************************************

# This Python program simulates a restricted subset of MIPS instructions
# and output 
# Settings: Multi-Cycle CPU, i.e lw takes 5 cycles, beq takes 3 cycles, others are 4 cycles

# this is probably wrong:
# MIPS is byte-addressable, so from 0x2000 to 0x3000 is a total of 0x1000 BYTES, which means
# 0x1000 / 4 = 0x0400 words
# we're always lw / sw here, so memory array is assumed to have 1 word per element, hence a total of 0x400 = 1024 elements.


#******************
#   GLOBALS
#******************
mem_space = 1024    # Memory addr starts from 2000 , ends at 3000 thus 1024 memory locations (node: one word is consider 1 address)

#******************
#   FUNCTIONS
#******************

#**     simulate(Instruction,InstructionHex,debugMode):
#*  Simulates the given Instruction array in binary. Supports debugMode.
#*  InstructionHex is used for ref in debug mode.
def simulate(Instruction,InstructionHex,debugMode):
    if(debugMode):
        print("***!!!!!!!! Debug Simulation !!!!!!!!***")
    else:
        print("*********** Starting Simulation ***********")

    # --- Variables ---
    # -- Simulate Data
    Register = [0,0,0,0,0,0,0,0]    # Registers are initialize to 0
    Memory = [0 for i in range(mem_space)]  # Memory is set to what space is supported
    PC = 0  
    DIC = 0

    # -- Cycle count
    # - Single cycle count
    Cycle = 0       # count of total cycles taken for single cycle CPU

    # - Multi cycle counts
    MultiCycle = 0  # count of total cycles taken for multi cycle CPU
    threeCycles = 0 # count of 3 cycles (beq takes 3 cycles)
    fourCycles = 0  # count of 4 cycles (All instruction, excluding beq and lw)
    fiveCycles = 0  # count of 5 cycles (lw takes 5 cycles)

    # - Pipeline count/counters
    PipeCycle = 4   # count of total cycles taken for pipeline CPU (note: all piple has extra 4 cycles at the end)
    lwCycleAdd = 0  # count of lw added cycles
    comCycleAdd = 0 # count of compare added cycles
    beqCycleAdd = 0 # count of branch taken added cycles
    
    # -- Looping
    finished = False

    # --- Now running the instuctions ---
    while(not(finished)):
        # - Status updates
        DIC += 1
        fetch = Instruction[PC]

        # --- Instruction interpertation ---
        # Funct: Deadloop END
        if(fetch[0:32] == '00010000000000001111111111111111'):      # STATUS: TEST
            # -- Cycle updates
            Cycle += 1          # A single cycle being done
            threeCycles += 1    # Beq instruction
            # Note: this instruciton for pipleline is ignored as the code immediately ends

            # -- Execution
            print("!!!Deadloop Detected!!! \nEnding simulation.")
            print("Instruction: 0x" +  InstructionHex[PC])
            finished = True     # ending simulation

        # Funct: ADD
        elif(fetch[0:6] == '000000' and fetch[26:32] == '100000'):  # STATUS: TEST
            # -- Cycle updates
            Cycle += 1      # A single cycle being done
            fourCycles += 1 # Normal instruction

            # - Piple line check
            checking = Instruction[PC + 1]
            if(checking[0:6] == '000100' or checking[0:6] == '000101'):
                if(fetch[16:21] == checking[6:11] or fetch[16:21] == checking[11:16]):
                    comCycleAdd += 1    # comparison delay because either beq or bne doesnt exist after this instruction with the result

            # -- Debug data 
            if(debugMode):
                print("Instruction: 0x" +  InstructionHex[PC] + " :" + "add $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
                print("Current PC: " + str(PC))
                print("PC = " + str(PC*4))
                print("Single cycles count: " + str(Cycle))
                print("Taking 4 cycles in multi\n")

            # -- Execution
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] + Register[int(fetch[11:16],2)]
            PC += 1

        # Funct: SUB
        elif(fetch[0:6] == '000000' and fetch[26:32] == '100010'):  # STATUS: TEST
            # -- Cycle updates
            Cycle += 1      # A single cycle being done
            fourCycles += 1 # Normal instruction

            # - Piple line check
            checking = Instruction[PC + 1]
            if(checking[0:6] == '000100' or checking[0:6] == '000101'):
                if(fetch[16:21] == checking[6:11] or fetch[16:21] == checking[11:16]):
                    comCycleAdd += 1    # comparison delay because either beq or bne exist after this instruction with the result

            # -- Debug data 
            if(debugMode):
                print("Instruction: 0x" +  InstructionHex[PC] + " :" + "sub $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
                print("Current PC: " + str(PC))
                print("PC = " + str(PC*4))
                print("Single cycles count: " + str(Cycle))
                print("Taking 4 cycles in multi\n")

            # -- Execution
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] - Register[int(fetch[11:16],2)]
            PC += 1

        # Funct: XOR
        elif(fetch[0:6] == '000000' and fetch[26:32] == '100110'):  # STATUS: TEST
            # -- Cycle updates
            Cycle += 1      # A single cycle being done
            fourCycles += 1 # Normal instruction

            # - Piple line check
            checking = Instruction[PC + 1]
            if(checking[0:6] == '000100' or checking[0:6] == '000101'):
                if(fetch[16:21] == checking[6:11] or fetch[16:21] == checking[11:16]):
                    comCycleAdd += 1    # comparison delay because either beq or bne exist after this instruction with the result
            
            # -- Debug data 
            if(debugMode):
                print("Instruction: 0x" +  InstructionHex[PC] + " :" + "xor $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
                print("Current PC: " + str(PC))
                print("PC = " + str(PC*4))
                print("Single cycles count: " + str(Cycle))
                print("Taking 4 cycles in multi\n")

            # -- Execution
            Register[int(fetch[16:21],2)] = Register[int(fetch[6:11],2)] ^ Register[int(fetch[11:16],2)]
            PC += 1
        
        # Funct: ADDI
        elif(fetch[0:6] == '001000'):                               # STATUS: TEST
            # -- Cycle updates
            Cycle += 1      # A single cycle being done
            fourCycles += 1 # Normal instruction

            # - Piple line check
            checking = Instruction[PC + 1]
            if(checking[0:6] == '000100' or checking[0:6] == '000101'):
                if(fetch[11:16] == checking[6:11] or fetch[11:16] == checking[11:16]):
                    comCycleAdd += 1    # comparison delay because either beq or bne exist after this instruction with the result

            # -- Debug data 
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -(65535 -int(fetch[16:32],2)+1)    # Converting binary int
            if(debugMode):
                print("Instruction: 0x" +  InstructionHex[PC] + " :" + "addi $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ", " + str(imm) )
                print("Current PC: " + str(PC))
                print("PC = " + str(PC*4))
                print("Single cycles count: " + str(Cycle))
                print("Taking 4 cycles in multi\n")

            # -- Execution
            Register[int(fetch[11:16],2)] = Register[int(fetch[6:11],2)] + imm
            PC += 1

        # Funct: BEQ
        elif(fetch[0:6] == '000100'):                               # STATUS: TEST
            # -- Cycle updates
            Cycle += 1          # A single cycle being done
            threeCycles += 1    # Beq instruction has one less cycle

            # -- Debug data 
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -(65535 -int(fetch[16:32],2)+1)    # Converting binary int
            if(debugMode):
                print("Instruction: 0x" +  InstructionHex[PC] + " :" + "beq $" + str(int(fetch[6:11],2)) + ",$" +str(int(fetch[11:16],2)) + "," + str(imm) )
                print("Current PC: " + str(PC))
                print("PC = " + str(PC*4))
                print("Single cycles count: " + str(Cycle))
                print("Taking 3 cycles in multi\n")

            # -- Execution
            PC += 1
            if(Register[int(fetch[6:11],2)] == Register[int(fetch[11:16],2)]):
                beqCycleAdd += 1    # Flush case as this branch is taken
                PC = PC + imm
            else:
                PC

        # Funct: BNE
        elif(fetch[0:6] == '000101'):                               # STATUS: TEST
            # -- Cycle updates
            Cycle += 1          # A single cycle being done
            threeCycles += 1    # Bne instruction has one less cycle

            # -- Debug data 
            imm = int(fetch[16:32],2) if fetch[16]=='0' else -(65535 -int(fetch[16:32],2)+1)    # Converting binary int
            if(debugMode):
                print("Instruction: 0x" +  InstructionHex[PC] + " :" + "bne $" + str(int(fetch[6:11],2)) + ",$" +str(int(fetch[11:16],2)) + "," + str(imm) )
                print("Current PC: " + str(PC))
                print("PC = " + str(PC*4))
                print("Single cycles count: " + str(Cycle))
                print("Taking 3 cycles in multi\n")

            # -- Execution
            PC += 1
            if(Register[int(fetch[6:11],2)] != Register[int(fetch[11:16],2)]):
                beqCycleAdd += 1    # Flush case as this branch is taken
                PC = PC + imm
            else:
                PC
        
        # Funct: SLT
        elif(fetch[0:6] == '000000' and fetch[26:32] == '101010'):  # STATUS: TEST
            # -- Cycle updates
            Cycle += 1      # A single cycle being done
            fourCycles += 1 # Normal instruction

            # - Piple line check
            checking = Instruction[PC + 1]
            if(checking[0:6] == '000100' or checking[0:6] == '000101'):
                if(fetch[16:21] == checking[6:11] or fetch[16:21] == checking[11:16]):
                    comCycleAdd += 1    # comparison delay because either beq or bne exist after this instruction with the result

            # -- Debug data 
            if(debugMode):
                print("Instruction: 0x" +  InstructionHex[PC] + " :" + "slt $" + str(int(fetch[16:21],2)) + ",$" +str(int(fetch[6:11],2)) + ",$" + str(int(fetch[11:16],2)) )
                print("Current PC: " + str(PC))
                print("PC = " + str(PC*4))
                print("Single cycles count: " + str(Cycle))
                print("Taking 4 cycles in multi\n")

            # -- Execution
            Register[int(fetch[16:21],2)] = 1 if Register[int(fetch[6:11],2)] < Register[int(fetch[11:16],2)] else 0
            PC += 1
        
        # Funct: LW
        elif(fetch[0:6] == '100011'):                               # STATUS: TEST
            # -- Cycle updates
            Cycle += 1      # A single cycle being done
            fiveCycles += 1 # Lw instruction has one more cycle

            # - Piple line check
            checking = Instruction[PC + 1]
            if(checking[0:6] == '000000'):      # R-type cases
                if(fetch[11:16] == checking[6:11] or fetch[11:16] == checking[11:16]):
                    comCycleAdd += 1    # Waiting on the lw to produce the result for next instruction
            elif(checking[0:6] == '001000'):    # Only I-type case
                if(fetch[11:16] == checking[6:11]):
                    comCycleAdd += 1    # Waiting on the lw to produce the result for next instruction

            # -- Error check
            if (int(fetch[30:32])%4 != 0 ):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(fetch,2)))
                exit()
            
            # -- Debug data
            imm = int(fetch[16:32],2)
            if(debugMode):
                print("Instruction: 0x" +  InstructionHex[PC] + " :" + "lw $" + str(int(fetch[6:11],2)) + "," +str(imm + Register[int(fetch[6:11],2)] - 8192) + "(0x2000)" )
                print("Current PC: " + str(PC))
                print("PC = " + str(PC*4))
                print("Single cycles count: " + str(Cycle))
                print("Taking 4 cycles in multi\n")

            # -- Execution
            Register[int(fetch[11:16],2)] = Memory[imm + Register[int(fetch[6:11],2)] - 8192] # Load memory into register
            PC += 1
            
        # Funct: SW
        elif(fetch[0:6] == '101011'):                               # STATUS: TEST
            # -- Cycle updates
            Cycle += 1      # A single cycle being done
            fourCycles += 1 # Normal instruction

            # -- Error check
            if (int(fetch[30:32])%4 != 0 ):
                print("Runtime exception: fetch address not aligned on word boundary. Exiting ")
                print("Instruction causing error:", hex(int(fetch,2)))
                exit()
            
            # -- Debug data
            imm = int(fetch[16:32],2)
            if(debugMode):
                print("Instruction: 0x" +  InstructionHex[PC] + " :" + "sw $" + str(int(fetch[6:11],2)) + "," +str(imm + Register[int(fetch[6:11],2)] - 8192) + "(0x2000)" )
                print("Current PC: " + str(PC))
                print("PC = " + str(PC*4))
                print("Single cycles count: " + str(Cycle))
                print("Taking 4 cycles in multi\n")

            # -- Execution
            Memory[imm + Register[int(fetch[6:11],2)] - 8192]= Register[int(fetch[11:16],2)] # Store word into memory
            PC += 1

    # --- Producing/Printing Results ---
    print("\n*********** Finished Simulation ***********")
    # -- Displaying basic data
    print("-< Simulators results data >-")
    print("Registers: " + str(Register))
    print("Dynamic instructions count: " +str(DIC))
    print("Current PC: " + str(PC))
    print("PC int address = " + str(PC*4))
    #print("Memory: " + str(Memory))    # Checking valid use of memory

    # -- Displaying single cycle
    print("\n-< Single cycle CPU results >-")
    print("Total number cycles done: " + str(Cycle))

    # -- Calculating/Displaying Multi cycle
    print("\n-< Multi cycle CPU results >-")
    MultiCycle = (3 * threeCycles) + (4 * fourCycles) + (5 * fiveCycles)
    print("Total number cycles done: " + str(MultiCycle))
    print("-> Number of 3 cycles: " + str(threeCycles))
    print("-> Number of 4 cycles: " + str(fourCycles))
    print("-> Number of 5 cycles: " + str(fiveCycles))

    # -- Calculating/Displaying Multi cycle
    print("\n-< Pipleline CPU results >-")
    PipeCycle = Cycle + PipeCycle + lwCycleAdd + comCycleAdd + beqCycleAdd
    print("Total number cycles done: " + str(PipeCycle))
    print("-> Number of lw added cycles: " + str(lwCycleAdd))
    print("-> Number of comparison added cycles: " + str(comCycleAdd))
    print("-> Number of beq added cycles: " + str(beqCycleAdd))
    
    print("\n*********** END PROGRAM ***********")
     
   

#******************
#   MAIN
#******************
def main():
    print("*************Welcome to ECE366 Project 4 MIPS Sim*************\n")

    # --- INPUT ---
    # -- Program A or B?
    print(" Choose the file for instructions be use:")
    fileMode =True if  int(input("1 = Program A         2 = Program B\n=> "))== 1 else False
    
    # -- Debug mode on?
    if(fileMode == 1):
        print("\n Choose the mode of running the Program A:")
    else:
        print("\n Choose the mode of running the Program B:")
    debugMode =True if  int(input("1 = debug mode        2 = normal execution\n=> "))== 1 else False

    # --- USE/SIMULATION ---
    # - Reading instruction file
    if(fileMode == 1):
        I_file = open("i_mem_A.txt","r")
    else:
        I_file = open("i_mem_B.txt","r")
    Instruction = []        # array containing all instructions to execute         
    InstructionHex = []     # Reference array
    for line in I_file:
        if (line == "\n" or line[0] =='#'):     # Ignoring empty lines and comments
            continue
        line = line.replace('\n','')    # Now adding the instuction
        InstructionHex.append(line)     # Referance hex instruction stored
        line = format(int(line,16),"032b")  # Converting Hex to binary
        Instruction.append(line)        # Adding the binary instruction to be used
        
    simulate(Instruction,InstructionHex,debugMode)  # Now simulating the instructions


if __name__ == "__main__":
    main()


