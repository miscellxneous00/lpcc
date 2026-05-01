%{
  #include <stdio.h>
  #include <stdlib.h>
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


  void yyerror(char *s);
  int yylex();
  double symbols[26];

%}

%union {
 int id;
 double num;
}

%token <id> VAR
%token <num> NUM
%token COS SIN LOG EXP

%type <num> expr

%right '='
%left '+' '-'
%left '*' '/'
%right '^'

%%

program : 
	 program statement '\n'
	 |
	 ;

statement : 
	   expr			{printf("Answer : %g\n",$1);}
	  | VAR '=' expr         {symbols[$1]=$3; printf("Assign : %c = %g\n",$1 + 'a',$3);}
	  ;


expr :
	  VAR			{$$ = symbols[$1];}
	  | NUM			{$$ = $1;} 
	  | expr '+' expr	{$$ = $1 + $3;}
	  | expr '-' expr	{$$ = $1 - $3;}
	  | expr '*' expr	{$$ = $1 * $3;}
	  | expr '/' expr	{if($3==0) {yyerror("Divide by Zero ERROR"); $$ = 0;} else $$ = $1 / $3 ;}
	  | expr '^' expr	{$$ = pow($1,$3);}
	  | '('  expr ')'	{$$ = $2;}
	  | SIN '(' expr ')'	{$$ = sin($3);}
	  | COS '(' expr ')'	{$$ = cos($3);}
	  | LOG '(' expr ')'     {$$ = log($3);}
	  | EXP '(' expr ')'     {$$ = exp($3);}
	  ;
%%


void yyerror(char *s){
  fprintf(stderr,"Error : %s \n",s);
}

int main(void){
  for(int i=0; i<26; i++){
  symbols[i] = 0.0;
}

yyparse();

return 0;

}
