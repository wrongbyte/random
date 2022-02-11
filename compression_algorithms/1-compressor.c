// We start with 512 buckets in the dictionary because we are using 9 bits instead of 8 bits (1 byte)
// So we are going to write a similar code to the previous one but using 512 as the default size for the dict (2^9)
#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <string.h>


void compress (const char *buf, int buflen) {
    char **dictionary; //pointers to strings (that are themselves pointers)
    int dictionary_index;
    int code;
    int code_length = 9; // bits per character, may grow depending on if the dict is full or not
    char *inp = buf;

    // 1 << x é o mesmo de 2^x
    dictionary = (char**)malloc(sizeof(char*) * (1 << code_length));

    /*      POR QUÊ USAR MEMSET AQUI?
        Cada "dictionary" é um pointer para uma string. Reservamos, com malloc, um espaço na memória para 512 entries.
        Contudo, esse espaço vai ser inicialmente preenchido por garbage values, porque não atribuímos valores. Então, para "limpar" esses garbage values, usaremos memset usando 0x0, o que vai substituir os garbage values por null pointers.
        O motivo disso é explicitado na linha 36.
    */
    memset(dictionary, 0x0, sizeof(char*) * (1 << code_length));

    // inicialização do dicionário inicial com os chars individuais
    // Lembra dos códigos ASCII? O compilador vai interpretar (caso o datatype seja char) o número como o caractere correspondente da tabela.
    for (dictionary_index = 0; dictionary_index < 256; dictionary_index++) {
        dictionary[dictionary_index] = (char*)malloc(2); // char + '/0'
        // aqui estamos montando o dicionário, veja que estamos basicamente inserindo dictionary_index em dictionary[dictionary_index]
        sprintf(dictionary[dictionary_index], "%c", dictionary_index);
    }

    // search while there's still data
    while(buflen--) {
        // começamos de trás para frente nos índices pq nos índices mais recentes teremos as maiores substrings
        for (int i = dictionary_index - 1; i; i--) {
            // Veja que na linha abaixo podemos ver claramente o porquê do memset. Sem usar memset, a condição abaixo seria sempre verdadeira, já que um bucket não preenchido conteria um garbage value, que por sua vez seria diferente de NULL. Isso pq temos já 512 buckets, e os últimos ainda não foram preenchidos.
            if (dictionary[i] != NULL) {
                if (!strncmp(dictionary[i], inp, strlen(dictionary[i]))) { // ou seja, falso = 0 = strings iguais = substring já existe no dicionário
                    code = i; // já que vamos printar no output somente o índice da substring correspondente
                    break;
                }
            }
        }

        /* VAMOS ADICIONAR POSTERIORMENTE AQUI A LÓGICA PARA PRINTAR OS CÓDIGOS CONFORME VÃO SENDO ENCONTRADOS */
        // printar p/ stdout + mover o pointer à frente
        // write_bits( code, out, code_length );
        // inp += strlen( dictionary[ code ] );

        // pq + 2? pq temos + o caractere atual + '\0'
        dictionary[dictionary_index] = malloc(strlen(dictionary[code]) + 2);
        // %s %c pq temos a substring já existente + o novo char adicionado
        sprintf(dictionary[dictionary_index], "%s%c", dictionary[code], *inp); // aparentemente inp é o char atual sendo lido
        dictionary_index++;
        
        // Expand the dictionary if necessary
        if (dictionary_index == (1 << code_length)) {
            code_length++;
            dictionary = realloc(dictionary, sizeof(unsigned char**) * (1 << code_length));
        }
    }
}
