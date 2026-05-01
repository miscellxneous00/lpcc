%{
    /* 
     * SECTION 1: C Declarations 
     * Everything inside %{ and %} is copied directly into the generated C file.
     */
    #include <stdio.h>
%}

/* 
 * SECTION 2: Rules 
 * Format is: [Regular Expression] { C Code to execute when matched }
 */
%%

[\t ]+      { /* Ignore spaces and tabs */ }

is|am|are|was|were|be|do|does|did|go|went|read|write { 
    printf("%s: VERB\n", yytext); 
}

he|she|it|they|we|I|you|him|her|them { 
    printf("%s: PRONOUN\n", yytext); 
}

and|or|but|because|if|then { 
    printf("%s: CONJUNCTION\n", yytext); 
}

in|on|at|under|over|with|by|about { 
    printf("%s: PREPOSITION\n", yytext); 
}

good|bad|happy|sad|big|small|fast|slow|quick { 
    printf("%s: ADJECTIVE\n", yytext); 
}

[a-zA-Z]+ { 
    /* 
     * Catch-all: If a word consists of letters but didn't match the 
     * lists above, we classify it as a NOUN. 
     * Note: In Lex, order matters! This must come LAST.
     */
    printf("%s: NOUN (or unclassified)\n", yytext); 
}

.|\n        { /* Ignore punctuation and newlines */ }

%%

/* 
 * SECTION 3: C Subroutines (Functions)
 * This is where the main program logic lives.
 */

/* yywrap is called by Lex when it reaches the end of the input file. 
 * Returning 1 tells Lex we are done and there is no more input. 
 */
int yywrap() {
    return 1;
}

int main() {
    printf("Enter a sentence to analyze (Press Ctrl+D to stop):\n");
    
    /* yylex() is the main Lex function that starts reading and matching */
    yylex(); 
    
    return 0;
}
