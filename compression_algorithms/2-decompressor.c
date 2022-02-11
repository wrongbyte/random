#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <string.h>

void decompress () {
    int prev = -1; // ??????????
    int code;
    int code_length = 9;
    unsigned char** dictionary;
    int dictionary_index;
    // Once the dictionary overflows, code_length increases
    dictionary = (unsigned char **)malloc(sizeof(unsigned char *) * (1 << code_length));
    memset(dictionary, sizeof(unsigned char*) * (1 << code_length), 0x0); //?????????????????

    //Initialize the first 256 entries
    for (dictionary_index = 0; dictionary_index < 256; dictionary_index++) {
        dictionary[dictionary_index] = (char**)malloc(2); // primeiro fazemos a alocação da memória
        sprintf(dictionary[dictionary_index], "%c", dictionary_index);
    }

    // !!!!!!!!!!!!!! temos que implementar read-next-code
    while ((code = read_next_code( code_length )) != -1) {
        if (prev > -1) {
            // HIPOTESE: se a entrada já existir no dicionário, concatenamos com o(s) caracter(es) atuais e inserimos isso no dicionário
            // possivelmente -1 se refere à isso, se for maior q -1 significa q a entrada já existe idk
            if (code == dictionary_index) {
                dictionary[dictionary_index] = (unsigned char*)malloc( strlen(dictionary[prev]) + 2 );
                sprintf(dictionary[dictionary_index], "%s%c", dictionary[prev], dictionary[code][0]); // PQ dictionary[code][0] ??? PQ ESTAMOS ADICIONANDO O PRIMEIRO CARACTERE DA SUBSTRING!
            } else {
                dictionary[dictionary_index] = (unsigned char*)malloc(strlen(dictionary[prev]) + 2);
                sprintf(dictionary[dictionary_index], "%s%c", dictionary[prev], dictionary[code][0]);
                dictionary_index++; //só partimos para o próximo bucket quando adicionamos uma nova entry
            }            
        }

        //Expand the dict if necessary
        if (dictionary_index == (1 << code_length)) {
            unsigned char **new_dictionary;
            code_length++;
            // we create a new dictionary and REassign the current dictionary to it (by using realloc)
            // The realloc function allocates a block of memory (which be can make it larger or smaller in size than the original) and copies the contents of the old block to the new block of memory, if necessary.
            dictionary = (unsigned char**)realloc(dictionary, sizeof(unsigned char**) * (1 << code_length));
        }
    }
    prev = code;
}

static void write_bits(int code, int out, int code_length) {
    static unsigned char buf = 0x0;
    static int bufpos = 0;

    int mask_pos = 0;

    while (code_length--) {
        // what the real fuck below ?
        buf |= ( (code & (code & (1 << mask_pos)) ? 1 : 0)) << bufpos;
        mask_pos++;
        if (bufpos++ == 7) {
            write(out, &buf, 1);
            buf = 0x0;
            bufpos = 0;
        }
    }
}