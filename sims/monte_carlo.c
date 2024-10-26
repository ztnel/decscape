
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#include "monte_carlo.h"
#include "stats.h"

#define TURNS (uint8_t)4
#define SAMPLES (uint8_t)7 + (TURNS - 1)
#define P_MAX (float)1.0f

#define STATUS_S1 (1 << 0)
#define STATUS_S2 (1 << 1)

static float generate_seed() {
  return (float)rand() / RAND_MAX;
}

static void update_stats() {

}

static void simulate(uint8_t *status, const uint8_t successes, uint8_t sample_size) {
  float success_ratio = (float)successes / sample_size;
  uint8_t hits = 0;
  for (uint8_t j = 0; j < SAMPLES; j++) {
    float seed = generate_seed();
    if (seed <= success_ratio) {
      hits++;
    }
    if (j == 6) {
      if (hits > 0) {
        *status |= STATUS_S1;
      }
    } else if (j == (SAMPLES - 1)) {
      if (hits <= 4) {
        *status |= STATUS_S2;
      }
    }
#ifdef DEBUG
    printf("%i: hits: %u seed: %.2f, status: %u, success_ratio: (%u/%u) %.2f\n", j, hits, seed, *status, successes, sample_size, success_ratio);
#endif
    sample_size--;
    success_ratio = (float)(successes - hits) / sample_size;
  }
}

void mc_init(void) {
  srand(time(NULL));
}

float mc_run(uint8_t successes, const uint8_t sample_size, const uint32_t epochs) {
  float p_success_1 = 0.0f;
  float p_success_2 = 0.0f;
  float p_s1_s2 = 0.0f;
  uint16_t acc_success_1 = 0;
  uint16_t acc_success_2 = 0;
  printf("EPOCH,ACC(S1),ACC(S2),P(S1),P(S2)\n");
  float result_vector[MC_MAX_EPOCHS][MC_MAX_EVENTS] = {0.0f};
  for (uint32_t i = 1; i < epochs; i++) {
    uint8_t status = 0;
    simulate(&status, successes, sample_size);
    if (status & STATUS_S1) {
      acc_success_1++;
    }
    if (status & STATUS_S2) {
      acc_success_2++;
    }
    p_success_1 = fminf((float)acc_success_1 / i, P_MAX);
    p_success_2 = fminf((float)acc_success_2 / i, P_MAX);
    p_s1_s2 = p_success_1 * p_success_2;
    if (stats_rse(mean, fstd) < target_margin) {
      break;
    }
    // export results
    printf("%u,%u,%u,%.2f,%.2f,%.2f\n", i, acc_success_1, acc_success_2, p_success_1, p_success_2, p_s1_s2);
  }
  printf("\n");
  return p_s1_s2;
}
