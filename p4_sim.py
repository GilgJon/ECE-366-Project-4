#******************************************************
#   ECE 366     Project 4
#       by: Jonathan Wacker     Base code authors: Trung Le, Weijing Rao
#   Objective: The code's objective is to read HEX 
#      MIPS code and the simulate the code. The DIC
#      and cycle number (for single, multicycle, and
#      pipeline) are also counted.
#******************************************************

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
def simulate(Instruction,InstructionHex,debugMode,cacheCase):
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

    # -- Cache stat tracking
    CHits = 0   # number of hits
    CMiss = 0   # number of misses
    logData = open("log_data.txt", "w") # Log data file opened
    
    # - Case1=> DM; 4 words; 2 blk total
    if(cacheCase == 1):
        Avalid = 0  # Valid blk?
        Atag = "0"  # Blk's tag
        
        Bvalid = 0
        Btag = "0"
        
    # - Case2=> DM; 2 words; 4 blk total
    elif(cacheCase == 2):
        Avalid = 0  # Valid blk?
        Atag = "0"  # Blk's tag
        
        Bvalid = 0
        Btag = "0"
        
        Cvalid = 0
        Ctag = "0"
        
        Dvalid = 0
        Dtag = "0"
        
    # - Case3=> FA; 2 words; 4 blk total
    elif(cacheCase == 3):
        SOtags = []     # Tags in the 1 set
        SOvalid = 0     # Valid blk?
        SOoverwrite = 0 # Allow overwrite?
        SOupdate = 0    # Update address
        
    # - Case4=> 2-way; 2 words; 4 sets; 8 blk total
    elif(cacheCase == 4):
        SOtags = []     # Tags in the 1 set
        SOvalid = 0     # Valid blk?
        SOoverwrite = 0 # Allow overwrite?
        SOupdate = 0    # Update address
        
        STtags = []     # Tags in the 2 set
        STvalid = 0     # Valid blk?
        SToverwrite = 0 # Allow overwrite?
        STupdate = 0    # Update address

        SEtags = []     # Tags in the 3 or "E" set
        SEvalid = 0     # Valid blk?
        SEoverwrite = 0 # Allow overwrite?
        SEupdate = 0    # Update address

        SFtags = []     # Tags in the 4 set
        SFvalid = 0     # Valid blk?
        SFoverwrite = 0 # Allow overwrite?
        SFupdate = 0    # Update address
    
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
                    lwCycleAdd += 1    # Waiting on the lw to produce the result for next instruction
            elif(checking[0:6] == '001000'):    # Only I-type case
                if(fetch[11:16] == checking[6:11]):
                    lwCycleAdd += 1    # Waiting on the lw to produce the result for next instruction

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
            outAddress = imm + Register[int(fetch[6:11],2)] - 8192
            Register[int(fetch[11:16],2)] = Memory[imm + Register[int(fetch[6:11],2)] - 8192] # Load memory into register
            PC += 1


            # --- Cache Checking --- 
            # - Getting data for current memory address.
            BoutAddress = str(format(int(outAddress), "016b"))
            
            # -- Case1=> DM; 4 words; 2 blk total
            if(cacheCase == 1):
                cTag = BoutAddress[0:13]   # Current blk tag
                #cBlk = BoutAddress[13]   # Current blk ID
                cPos = BoutAddress[14:16]   # Off
                logData.write("=> Now accessing address 0x" + BoutAddress + " (tag: " + cTag + ")\n")
                if(BoutAddress[13] == "0"):       # Blk 1 Check
                    if(Avalid == 1):
                        if(cTag == Atag):
                            logData.write("-->HIT<-- \\\Blk 1 (tag:" + Atag + ")///")
                            CHits += 1      # New Hit
                        else:
                            Atag = cTag
                            logData.write("-->MISS<-- \\\Blk 1 (new tag:" + Atag + ")///")
                            CMiss += 1      # New Miss
                    else:
                        Atag = cTag     # Now using new blk data
                        Avalid = 1
                        logData.write("-->MISS<-- \\\ New Blk 1 (new tag:" + Atag + ")///")
                        CMiss += 1      # New Miss

                else:                   # Blk 2 Check
                    if(Bvalid == 1):
                        if(cTag == Btag):
                            logData.write("-->HIT<-- \\\Blk 2 (tag:" + Btag + ")///")
                            CHits += 1      # New Hit
                        else:
                            Btag = cTag
                            logData.write("-->MISS<-- \\\Blk 2 (new tag:" + Btag + ")///")
                            CMiss += 1      # New Miss
                    else:
                        Btag = cTag     # Now using new blk data
                        Bvalid = 1
                        logData.write("-->MISS<-- \\\ New Blk 2 (new tag:" + Btag + ")///")
                        CMiss += 1      # New Miss
                        
                        
            # -- Case2=> DM; 2 words; 4 blk total
            elif(cacheCase == 2):
                ccTag = BoutAddress[0:13]   # Current blk tag
                logData.write("=> Now accessing address 0x" + BoutAddress + "00 (tag: " + ccTag + ")\n")
                if(BoutAddress[13:15] == "00"):       # Blk 1 Check
                    if(Avalid == 1):
                        if(ccTag == Atag):
                            logData.write("-->HIT<-- \\\Blk 1 (tag:" + Atag + ")///")
                            CHits += 1      # New Hit
                        else:
                            Atag = ccTag
                            logData.write("-->MISS<-- \\\Blk 1 (new tag:" + Atag + ")///")
                            CMiss += 1      # New Miss
                    else:
                        Atag = ccTag     # Now using new blk data
                        Avalid = 1
                        logData.write("-->MISS<-- \\\Blk 1 (new tag:" + Atag + ")///")
                        CMiss += 1      # New Miss
                        
                elif(BoutAddress[13:15] == "01"):     # Blk 2 Check
                    if(Bvalid == 1):
                        if(ccTag == Btag):
                            logData.write("-->HIT<-- \\\Blk 2 (tag:" + Btag + ")///")
                            CHits += 1      # New Hit
                        else:
                            Btag = ccTag
                            logData.write("-->MISS<-- \\\Blk 2 (new tag:" + Btag + ")///")
                            CMiss += 1      # New Miss
                    else:
                        Btag = ccTag     # Now using new blk data
                        Bvalid = 1
                        logData.write("-->MISS<-- \\\Blk 2 (new tag:" + Btag + ")///")
                        CMiss += 1      # New Miss
                        
                elif(BoutAddress[13:15] == "10"):     # Blk 3 Check
                    if(Cvalid == 1):
                        if(ccTag == Ctag):
                            logData.write("-->HIT<-- \\\Blk 3 (tag:" + Ctag + ")///")
                            CHits += 1      # New Hit
                        else:
                            Atag = ccTag
                            logData.write("-->MISS<-- \\\Blk 3 (new tag:" + Ctag + ")///")
                            CMiss += 1      # New Miss
                    else:
                        Ctag = ccTag     # Now using new blk data
                        Cvalid = 1
                        logData.write("-->MISS<-- \\\Blk 3 (new tag:" + Ctag + ")///")
                        CMiss += 1      # New Miss
                        
                elif(BoutAddress[13:15] == "11"):     # Blk 4 Check
                    if(Dvalid == 1):
                        if(ccTag == Dtag):
                            logData.write("-->HIT<-- \\\Blk 4 (tag:" + Dtag + ")///")
                            CHits += 1      # New Hit
                        else:
                            Dtag = ccTag
                            logData.write("-->MISS<-- \\\Blk 4 (new tag:" + Dtag + ")///")
                            CMiss += 1      # New Miss
                    else:
                        Dtag = ccTag     # Now using new blk data
                        Dvalid = 1
                        logData.write("-->MISS<-- \\\Blk 4 (new tag:" + Dtag + ")///")
                        CMiss += 1      # New Miss
            

            # -- Case3=> FA; 2 words; 4 blk total
            elif(cacheCase == 3):
                ccTag = BoutAddress[0:15]   # Current blk tag
                logData.write("=> Now accessing address 0x" + BoutAddress + " (tag: " + ccTag + ")\n")
                match = 0                   # Resetting com var
                if(SOvalid == 0):
                    # - Adding address to block to define it
                    SOtags.append(ccTag)
                    logData.write("-->MISS<-- \\\Set 1{1} (new tag: Given Tag above)///")
                    SOvalid = 1
                    SOupdate += 1
                    CMiss += 1      # New Miss
                else:
                    # - Checking if address exist in block currently
                    max = range(len(SOtags))
                    for i in max:
                        logData.write("-->CHECK<-- \\\Set 1{" + str(i + 1) + "} (tag:" + SOtags[i] + ")///\n")
                        if(SOtags[i] == ccTag):
                            k = i   # Holding index for result
                            match = 1
                        else:
                            continue
                    if(match == 1): # Tag in block
                        logData.write("-->HIT<-- \\\Set 1{" + str(k) + "} (tag:" + SOtags[k] + ")///")
                        CHits += 1      # New Hit
                    else:   # Tag is not in block
                        eco = SOupdate
                        if(SOoverwrite == 0):
                            SOtags.append(ccTag)   # Adding to list
                            SOupdate += 1
                            if(SOupdate == 4):
                                SOupdate = 0
                                SOoverwrite = 1
                        else:
                            SOtags[SOupdate] = ccTag
                            SOupdate += 1
                            if(SOupdate == 4):
                                SOupdate = 0
                        logData.write("-->MISS<-- \\\Set 1{" + str(eco + 1) + "} (new tag: " + SOtags[SOupdate - 1] + ")///")
                        CMiss += 1      # New Miss

            
            # -- Case4=> 2-way; 2 words; 4 sets; 8 blk total
            elif(cacheCase == 4):
                ccTag = BoutAddress[0:13]   # Current blk tag
                match = 0                   # Resetting com var
                logData.write("=> Now accessing address 0x" + BoutAddress + " (tag: " + ccTag + ")\n")
                if[BoutAddress[13:15] == "00"]:       # Set 1 Check
                    if(SOvalid == 0):
                        # - Adding address to block to define it
                        SOtags.append(ccTag)
                        logData.write("-->MISS<-- \\\Set 1{1} (new tag: Given Tag above)///")
                        SOvalid = 1
                        SOupdate += 1
                        CMiss += 1      # New Miss
                    else:
                        # - Checking if address exist in block currently
                        max = range(len(SOtags))
                        for i in max:
                            logData.write("-->CHECK<-- \\\Set 1{" + str(i + 1) + "} (tag:" + SOtags[i] + ")///\n")
                            if(SOtags[i] == ccTag):
                                k = i   # Holding index for result
                                match = 1
                            else:
                                continue
                        if(match == 1): # Tag in block
                            logData.write("-->HIT<-- \\\Set 1{" + str(k + 1) + "} (tag:" + SOtags[k] + ")///")
                            CHits += 1      # New Hit
                        else:   # Tag is not in block
                            eco = SOupdate
                            if(SOoverwrite == 0):
                                SOtags.append(ccTag)   # Adding to list
                                SOupdate += 1
                                if(SOupdate == 8):
                                    SOupdate = 0
                                    SOoverwrite = 1
                            else:
                                SOtags[SOupdate] = ccTag
                                SOupdate += 1
                                if(SOupdate == 8):
                                    SOupdate = 0
                            logData.write("-->MISS<-- \\\Set 1{" + str(eco + 1) + "} (new tag: " + SOtags[SOupdate - 1] + ")///")
                            CMiss += 1      # New Miss
                        
                elif[BoutAddress[13:15] == "01"]:     # Set 2 Check
                    if(STvalid == 0):
                        # - Adding address to block to define it
                        STtags.append(ccTag)
                        logData.write("-->MISS<-- \\\Set 2{1} (new tag: Given Tag above)///")
                        STvalid = 1
                        STupdate += 1
                        CMiss += 1      # New Miss
                    else:
                        # - Checking if address exist in block currently
                        max = range(len(STtags))
                        for i in max:
                            logData.write("-->CHECK<-- \\\Set 2{" + str(i + 1) + "} (tag:" + STtags[i] + ")///\n")
                            if(STtags[i] == ccTag):
                                k = i   # Holding index for result
                                match = 1
                            else:
                                continue
                        if(match == 1): # Tag in block
                            logData.write("-->HIT<-- \\\Set 2{" + str(k) + "} (tag:" + STtags[k] + ")///")
                            CHits += 1      # New Hit
                        else:   # Tag is not in block
                            eco = STupdate
                            if(SToverwrite == 0):
                                STtags.append(ccTag)   # Adding to list
                                STupdate += 1
                                if(STupdate == 8):
                                    STupdate = 0
                                    SToverwrite = 1
                            else:
                                STtags[STupdate] = ccTag
                                STupdate += 1
                                if(STupdate == 8):
                                    STupdate = 0
                            logData.write("-->MISS<-- \\\Set 2{" + str(eco + 1) + "} (new tag: " + STtags[STupdate - 1] + ")///")
                            CMiss += 1      # New Miss
                        
                elif[BoutAddress[13:15] == "10"]:     # Set 3 Check
                    if(SEvalid == 0):
                        # - Adding address to block to define it
                        SEtags.append(ccTag)
                        logData.write("-->MISS<-- \\\Set 3{1} (new tag: Given Tag above)///")
                        SEvalid = 1
                        SEupdate += 1
                        CMiss += 1      # New Miss
                    else:
                        # - Checking if address exist in block currently
                        max = range(len(SEtags))
                        for i in max:
                            logData.write("-->CHECK<-- \\\Set 3{" + str(i + 1) + "} (tag:" + SEtags[i] + ")///\n")
                            if(SEtags[i] == ccTag):
                                k = i   # Holding index for result
                                match = 1
                            else:
                                continue
                        if(match == 1): # Tag in block
                            logData.write("-->HIT<-- \\\Set 3{" + str(k) + "} (tag:" + SEtags[k] + ")///")
                            CHits += 1      # New Hit
                        else:   # Tag is not in block
                            eco = SEupdate
                            if(SEoverwrite == 0):
                                SEtags.append(ccTag)   # Adding to list
                                SEupdate += 1
                                if(SEupdate == 8):
                                    SEupdate = 0
                                    SEoverwrite = 1
                            else:
                                SEtags[SEupdate] = ccTag
                                SEupdate += 1
                                if(SEupdate == 8):
                                    SEupdate = 0
                            logData.write("-->MISS<-- \\\Blk 1{" + str(eco + 1) + "} (new tag: " + SEtags[SEupdate - 1] + ")///")
                            CMiss += 1      # New Miss
                        
                elif[BoutAddress[13:15] == "11"]:     # Set 4 Check
                    if(SFvalid == 0):
                        # - Adding address to block to define it
                        SFtags.append(ccTag)
                        logData.write("-->MISS<-- \\\Set 4{1} (new tag: Given Tag above)///")
                        SFvalid = 1
                        SFupdate += 1
                        CMiss += 1      # New Miss
                    else:
                        # - Checking if address exist in block currently
                        max = range(len(SFtags))
                        for i in max:
                            logData.write("-->CHECK<-- \\\Set 4{" + str(i + 1) + "} (tag:" + SFtags[i] + ")///\n")
                            if(SFtags[i] == ccTag):
                                k = i   # Holding index for result
                                match = 1
                            else:
                                continue
                        if(match == 1): # Tag in block
                            logData.write("-->HIT<-- \\\Set 4{" + str(k) + "} (tag:" + SFtags[k] + ")///")
                            CHits += 1      # New Hit
                        else:   # Tag is not in block
                            eco = SFupdate
                            if(SFoverwrite == 0):
                                SFtags.append(ccTag)   # Adding to list
                                SFupdate += 1
                                if(SFupdate == 8):
                                    SFupdate = 0
                                    SFoverwrite = 1
                            else:
                                SFtags[SFupdate] = ccTag
                                SFupdate += 1
                                if(SFupdate == 8):
                                    SFupdate = 0
                            logData.write("-->MISS<-- \\\Set 4{" + str(eco + 1) + "} (new tag: " + SFtags[SFupdate - 1] + ")///")
                            CMiss += 1      # New Miss
                            
            logData.write("\n")
            
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
        if(debugMode):
            input("Press any key to continue")
            print()
        else:
             continue

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

    # -- Calculating/Displaying Pipeline cycle
    print("\n-< Pipeline CPU results >-")
    PipeCycle = Cycle + PipeCycle + lwCycleAdd + comCycleAdd + beqCycleAdd
    print("Total number cycles done: " + str(PipeCycle))
    print("-> Number of lw added cycles: " + str(lwCycleAdd))
    print("-> Number of comparison added cycles: " + str(comCycleAdd))
    print("-> Number of beq added cycles: " + str(beqCycleAdd))

    # -- Calculating/Displaying Cache data
    print("\n-< Cache results with given type >-")
    CRatio = (CHits/(CHits + CMiss))
    print("Number of Hits: " + str(CHits))
    print("Number of Miss: " + str(CMiss))
    print("Rate ratio: " + str(CRatio))
    
    print("\n*********** END PROGRAM ***********")
    logData.close()     # Closing the log file
     
   

#******************
#   MAIN
#******************
def main():
    print("*************Welcome to ECE366 Project 4 MIPS Sim*************\n")

    # --- INPUT ---
    # -- Program A or B?
    print(" Choose the file for instructions be use:")
    fileMode =True if  int(input("1 = Program A         2 = Program B\n=> "))== 1 else False
    if(fileMode == 1):
        openType =True if  int(input("1 = Ver A1         2 = Ver B1\n=> "))== 1 else False
        if(openType == 1):
            I_file = open("p4_imem_A1.txt","r")
        else:
            I_file = open("p4_imem_A2.txt","r")
    else:
        openType =True if  int(input("1 = Ver A1         2 = Ver B1\n=> "))== 1 else False
        if(openType == 1):
            I_file = open("p4_imem_B1.txt","r")
        else:
            I_file = open("p4_imem_B2.txt","r")
    
    # -- Debug mode on?
    if(fileMode == 1):
        print("\n Choose the mode of running the Program A:")
    else:
        print("\n Choose the mode of running the Program B:")
    debugMode =True if  int(input("1 = debug mode        2 = normal execution\n=> "))== 1 else False

    # -- Cache type
    print(" Choose cache type be use:")
    cacheMode =True if  int(input("1 = DM Types        2 = Associated types\n=> "))== 1 else False

    # - Getting desired cache type
    if(cacheMode == 1):
        print("\n Choose the configuration for the DM:")
        cacheCase =True if  int(input("1 = 4 words, 2 blk   2 = 2 words, 4 blk\n=> "))== 1 else False
        if(cacheCase == 1):
            cacheCase = 1
        else:
            cacheCase = 2
    else:
        print("\n Choose the configuration for the Assocaiated type:")
        cacheCase =True if  int(input("1 = FA 2 words, 4 blk    2 = 2-way 2 words, 4 sets, total 8 blks\n=> "))== 1 else False
        if(cacheCase == 1):
            cacheCase = 3
        else:
            cacheCase = 4
        
    # --- USE/SIMULATION ---
    # - Using instruction file
    Instruction = []        # array containing all instructions to execute         
    InstructionHex = []     # Reference array
    for line in I_file:
        if (line == "\n" or line[0] =='#'):     # Ignoring empty lines and comments
            continue
        line = line.replace('\n','')    # Now adding the instuction
        InstructionHex.append(line)     # Referance hex instruction stored
        line = format(int(line,16),"032b")  # Converting Hex to binary
        Instruction.append(line)        # Adding the binary instruction to be used
        
    simulate(Instruction,InstructionHex,debugMode,cacheCase)  # Now simulating the instructions


if __name__ == "__main__":
    main()


