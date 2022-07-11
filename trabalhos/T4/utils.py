inputs = [
    'MEM(+(CONST 1,CONST 2))',
    'MOVE(MEM(+(MEM(+(FP,CONST a)),*(TEMP i,CONST 4))),MEM(+(FP,CONST x)))'
]

JOUETTE_PATTERNS = {
    1: "TEMP r{i}",
    2: "ADD r{i} <- r{j} + r{k}",
    3: "MUL r{i} <- r{j} * r{k}",
    4: "SUB r{i} <- r{j} - r{k}",
    5: "DIV r{i} <- r{j} / r{k}",
    **{i : "ADDI r{i} <- r{j} + {c}" for i in range(6, 9)},
    9: "SUBI r{i} <- r{j} - {c}",
    **{i : "LOAD r{i} <- M[r{j} + {c}]" for i in range(10, 14)},
    **{i : "STORE M[r{j} + {c}] <- r{i}" for i in range(14, 18)},
    18: "MOVEM M[r{j}] <- M[r{i}]",
}