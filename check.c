#include <stdio.h>
#include <stdlib.h>

void try()
{
fork();
printf("Example\n");
fork();
return;
}

 int main()
{
try(); fork();
printf("Example\n");
exit(0);
}