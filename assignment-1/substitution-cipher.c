#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

/* Function to read the input till the end of file */
char *inputString(FILE* fp, size_t size, char endChar){
    char *str;
    int ch;
    size_t len = 0;
    str = realloc(NULL, sizeof(char)*size); // size is start size
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

/* Function to compute the modulus of a number */
int mod(int a, int b){
    int r = a % b;
    return r < 0 ? r + b : r;
}

/* Function to encrypt a text using a map */
void map(char *text, char mapping[]){
    for(int i = 0; i < strlen(text) + 1; i++){
        if(isalpha(text[i]) && isupper(text[i])){
            text[i] = mapping[(text[i] - 'A') % 26];
            text[i] = toupper(text[i]);
        }else if(isalpha(text[i])){
            text[i] = mapping[(text[i] - 'a') % 26];
            text[i] = tolower(text[i]);
        }
    }
}

/* Function to decrypt a text using a map */
void decryptionMap(char *text, char mapping[]){
    for(int i = 0; i < strlen(text) + 1; i++){
        if(isalpha(text[i]) && isupper(text[i])){
            for (int j = 0; j < strlen(mapping) + 1; j++){
                if(text[i] == toupper(mapping[j])){
                    text[i] = j + 'A';
                    break;
                }
            }
        }else if(isalpha(text[i])){
            for (int j = 0; j < strlen(mapping) + 1; j++){
                if(text[i] == tolower(mapping[j])){
                    text[i] = j + 'a';
                    break;
                }
            }
        }
    }
}

/* Function to encrypt/decrypt a text with a shift value */
void shift(char *text, int shiftValue){
    for(int i = 0; i < strlen(text) + 1; i++){
        if(isalpha(text[i]) && isupper(text[i])){
            text[i] = mod((text[i] - 'A' + shiftValue),26) + 'A';
        }else if(isalpha(text[i])){
            text[i] = mod((text[i] - 'a' + shiftValue),26) + 'a';
        }
    }
}

/* Function to handle the input of encrypting or decrypting the text */
void handleInput(char *rules, char *text){
    // we do all the encryption/decryption on the alphabet, therefore having to map the resulted alphabet only once
    // on the given text
    char alphabet[26] = "abcdefghijklmnopqrstuvwxyz";
    char *token;
    const char s[2] = " ";

    token = strtok(rules, s);
    while(token != NULL){
        if(token[0] == 'e'){
            token = strtok(NULL, s);
            if(isdigit(token[0]) || token[0] == '-'){
                shift(alphabet, atoi(token));
            }else if (isalpha(token[0])){
                map(alphabet, token);
            }
        }else{
            token = strtok(NULL, s);
            if(isdigit(token[0]) || token[0] == '-'){
                shift(alphabet, -atoi(token));
            }else{
                decryptionMap(alphabet, token);
            }
        }
        token = strtok(NULL, s);
    }
    map(text, alphabet);
    printf("%s", text);
}

int main(int argc, const char * argv[]) {
    char *input;
    int inputLength;

    char *text;
    int textLength;

    input = inputString(stdin, 10, '\n');

    text = inputString(stdin, 10, '~');

    handleInput(input, text);

    free(input);
    free(text);

    return 0;
}