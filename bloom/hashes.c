#include <stdio.h>
#include <string.h>

// "brian" -> 57242470
unsigned int RSHash(char* str, unsigned int len) {
   unsigned int a    = 378551;
   unsigned int b    = 63689;
   unsigned int hash = 0;
   unsigned int i    = 0;

   for(i = 0; i < len; str++, i++) {
      hash = hash * a + (*str);
      a    = a * b;
   }

   return hash;
}

int main(int argc, char **argv) {
    
    printf("RSHash: %d\n", RSHash(argv[1], strlen(argv[1])));

}
