%{

#include "y.tab.h"
#include <math.h>

/*
Commands to compile and run:

sudo apt update
sudo apt install flex bison byacc

lex calc.l
yacc -d calc.y
gcc y.tab.c lex.yy.c -lm -o final

Run:
./final
*/

%}

%%
[a-z]             { yylval.id = yytext[0] - 'a'; return VAR; }
[0-9]+(\.[0-9]+)? { yylval.num = atof(yytext); return NUM; }
"sin"             { return SIN; }
"cos"             { return COS; }
"log"             { return LOG; }
"exp"             { return EXP; }
[-+*/=^()\n]      { return yytext[0]; }
[ \t]             { /* Ignore spaces and tabs */ }
.                 { printf("Invalid character\n"); }
%%

int yywrap() { 
    return 1; 
}
