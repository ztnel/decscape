
#include "monte_carlo.h"
#include <stdio.h>

int main(void) {
  mc_init();
  float result_vector[10];
  for (uint8_t i = 10; i < 20; i++) {
    result_vector[i - 10] = monte_carlo_run(i, 60, 5000);
  }
  FILE *fp;
  fp = fopen("results.csv", "w");
  printf("Results: \n");
  for (uint8_t i = 0; i < 10; i++) {
    printf("Successes: %u P(success): %.2f\n", 10 + i, result_vector[i]);
    fprintf(fp, "%u,%.2f\n", 10 + i, result_vector[i]);
  }
  fclose(fp);
}
