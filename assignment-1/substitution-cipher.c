#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

char *inputString(FILE* fp, size_t size, int *length){
//The size is extended by the input with the value of the provisional
    char *str;
    int ch;
    size_t len = 0;
    str = realloc(NULL, sizeof(char)*size);//size is start size
    if(!str)return str;
    while(EOF!=(ch=fgetc(fp))){
        str[len++]=ch;
        if(len==size){
            str = realloc(str, sizeof(char)*(size+=16));
            if(!str)return str;
        }
    }
    str[len++]='\0';
    *length = len;

    return realloc(str, sizeof(char)*len);
}

void map(char *text, char mapping[]){
    for(int i = 0; i < strlen(text) + 1; i++){
        if(isalpha(text[i]) && isupper(text[i])){
           text[i] = mapping[(text[i] - 'A') % 26] - 32;
       }else if(isalpha(text[i])){
           text[i] = mapping[(text[i] - 'a') % 26]; 
       }
    }

}
void decryptionMap(char *text, char mapping[]){
    for(int i = 0; i < strlen(text) + 1; i++)
    {
        if(isalpha(text[i]) && isupper(text[i])){
           for (int j = 0; j < strlen(mapping) + 1; j++)
           {
               if(text[i] == mapping[j]){
                   text[i] = j + 'A';
                   break;
               }
           }
       }else if(isalpha(text[i])){
           for (int j = 0; j < strlen(mapping) + 1; j++)
           {
               if(text[i] == mapping[j]){
                   text[i] = j + 'a';
                   break;
               }
           }
           
       }
    }
}

int mod(int a, int b)
{
    int r = a % b;
    return r < 0 ? r + b : r;
}

void shift(char *text, int shiftValue){
    for(int i = 0; i < strlen(text) + 1; i++){
       if(isalpha(text[i]) && isupper(text[i])){
           text[i] = mod((text[i]- 'A' + shiftValue),26) + 'A';
       }else if(isalpha(text[i])){
           text[i] = mod((text[i] - 'a' + shiftValue),26) + 'a';
       }
    }

}
void handleInput(char *rules, char *text){
    
    char *token;
    const char s[2] = " ";

    token = strtok(rules, s);
    while(token != NULL){  
        if(token[0] == 'e'){
            token = strtok(NULL, s);
            if(isdigit(token[0])){
                shift(text, atoi(token));

            }else{
                map(text, token);
            }
        }else{
            token = strtok(NULL, s);
            if(isdigit(token[0])){
                shift(text, -atoi(token));
            }else{
                decryptionMap(text, token);
            }
        }
        token = strtok(NULL, s);
    }

    printf("%s", text);
}  
int main(int argc, const char * argv[]) {
    char *input;
    int inputLength;

    char *textToken;
    const char s[2] = "\n";

    input = inputString(stdin, 10, &inputLength);

    textToken = strtok(input, s);
   
    char *rules = malloc(strlen(textToken) + 1);
    strcpy(rules, textToken);
    textToken = strtok(NULL, s);

    char *text = malloc(strlen(textToken) + 1);
    while(textToken != NULL){
        text = realloc(text,strlen(text) + strlen(textToken) + 2);
        strcat(text, textToken);
        strcat(text, "\n");
        textToken = strtok(NULL, s);
    }
    
    handleInput(rules, text);
    free(input);
    free(rules);
    free(text);

    return 0;
}