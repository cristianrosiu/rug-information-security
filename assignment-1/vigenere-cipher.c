#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>


int mod(int a, int b)
{
    int r = a % b;
    return r < 0 ? r + b : r;
}


void encrypt(char *text, char *key){
    int keyCounter = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if(keyCounter >= strlen(key) || text[i] == '\n') keyCounter = 0;
        if(isalpha(text[i]))
        {
            char ch = islower(text[i]) ? 'a':'A';
            int shiftValue = key[keyCounter] - 'a';
            text[i] = mod(text[i] - ch + shiftValue, 26) + ch;
            keyCounter++;
        }
    }
    
}


void decrypt(char *text, char *key){
    int keyCounter = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if(keyCounter >= strlen(key) || text[i] == '\n') keyCounter = 0;
        if(isalpha(text[i])){
            int isUpper = isupper(text[i]);
            text[i] = tolower(text[i]);
            text[i] = mod(text[i] - key[keyCounter], 26) + 'a';
            if(isUpper) text[i] = toupper(text[i]);
            keyCounter++; 
        }
    }
    
}


char *inputString(FILE* fp, size_t size, char endChar){
//The size is extended by the input with the value of the provisional
    char *str;
    int ch;
    size_t len = 0;
    str = realloc(NULL, sizeof(char)*size);//size is start size
    if(!str)return str;
    while(EOF!=(ch=fgetc(fp)) && ch != endChar){
    
        str[len++]=ch;
        if(len==size){
            str = realloc(str, sizeof(char)*(size+=16));
            if(!str)return str;
        }
    }
    str[len++]='\0';

    return realloc(str, sizeof(char)*len);
}


int main(int argc, char *argv[]) {
    char method; 
    scanf(" %c ", &method);

    char *key = inputString(stdin,10,'\n');

    char *text = inputString(stdin, 10,'~');


    switch (method)
    {
    case 'e':
        encrypt(text, key);
        break;

    case 'd':
        decrypt(text, key);
        break;
    
    default:
        break;
    }

    printf("%s", text);
  
    return 0;
}

