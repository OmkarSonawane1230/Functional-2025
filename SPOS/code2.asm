; Example assembly code with macro definition and usage
MACRO INCR &ARG
    MOVER AREG, &ARG
    ADD AREG, ='1'
    MOVEM AREG, &ARG
MEND

START 100
INCR X
INCR Y
X DC 5
Y DC 10
END