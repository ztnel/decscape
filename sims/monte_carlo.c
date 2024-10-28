
#include <math.h>
#include <stdint.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <time.h>

#include "monte_carlo.h"
#include "stats.h"

#define P_MAX (float)1.0f
#define FP_TOLERANCE 1e-6f // rounding errors

static float generate_seed(void) {
  float r = 0.0f; 
  while (r == 0.0f) {
    r = (float)rand() / (float)RAND_MAX;
  }
  return r;
}

static void state_estimator(float *psv, const uint16_t *cv, const size_t num_subsets) {
  uint64_t population_size = 0;
  for (size_t i = 0; i < num_subsets; i++) {
    population_size += cv[i];
  }
  for (size_t i = 0; i < num_subsets; i++) {
    psv[i] = (float)cv[i] / population_size;
  }
}

static void randomizer(uint16_t *cv, uint16_t *csv, const float *psv, const size_t num_subsets) {
  const float seed = generate_seed();
  float cumulative_probability = 0.0f;
  for (size_t i = 0; i < num_subsets; i++) {
    cumulative_probability += psv[i] + FP_TOLERANCE; 
    if (seed < cumulative_probability) {
      cv[i]--;
      csv[i]++;
      break;
    }
  }
}

/**
 * @brief Find the maximum iterations required based on channel iteration triggers
 * 
 * @return Maximum number of iterations
 */
static uint8_t get_max_iterations(const struct mc_event_channel *channels, size_t num_channels) {
  uint8_t max_iterations = 0;
  for (size_t i = 0; i < num_channels; i++) {
    if (channels[i].iteration_trigger > max_iterations) {
      max_iterations = channels[i].iteration_trigger;
    }
  }
  return max_iterations;
}

static void run_traces(bool *iev, const uint16_t *csv, const struct mc_params *params, const uint8_t iteration) {
  for (size_t i = 0; i < params->num_channels; i++) {
    const struct mc_event_channel *channel = &params->channels[i];
    if (channel->iteration_trigger == iteration) {
      // iev can only be updated once per simulation epoch
      iev[i] = channel->event_test_cb(csv, iev);
    }
  }
}
static void update_stats(float *result_vector, const uint16_t *csv, const size_t num_channels, const uint64_t epoch) {
  for (size_t i = 0; i < num_channels; i++) {
    result_vector[i] = fminf((float)csv[i] / (float)epoch, P_MAX);
  }
}

static void print_csv_header(const size_t num_channels) {
  printf("EPOCH,");
  for (size_t i = 0; i < num_channels; i++) {
    printf("ACC(E%zu),", i);
  }
  for (size_t i = 0; i < num_channels; i++) {
    printf("P(E%zu),", i);
  }
  printf("\n");
}

static void report(const uint64_t epoch, const uint16_t *csv, const float *psv, const size_t num_channels) {
  printf("%llu,", epoch);
  for (size_t i = 0; i < num_channels; i++) {
    printf("%u,", csv[i]);
  }
  for (size_t i = 0; i < num_channels; i++) {
    printf("%.4f,", psv[i]);
  }
  printf("\n");
}

static void simulate(uint16_t *cesv, const struct mc_params *params, const uint8_t max_iterations) {
  bool iev[MC_MAX_EVENT_CHANNELS] = {0};
  float psv[MC_MAX_SUBSETS] = {0.0f};
  uint16_t cv[MC_MAX_SUBSETS] = {0};
  uint16_t csv[MC_MAX_SUBSETS] = {0};
  memcpy(cv, params->cardinality_vector, sizeof(params->cardinality_vector[0]) * params->num_subsets);
  for (uint8_t iteration = 1; iteration <= max_iterations; iteration++) {
    // update psv
    state_estimator(psv, cv, params->num_subsets);
    // update cv and csv
    randomizer(cv, csv, psv, params->num_subsets);
    run_traces(iev, csv, params, iteration);
#ifdef DEBUG
    printf("%u,", iteration);
    for (size_t i = 0; i < params->num_subsets; i++) {
      printf("%u,", cv[i]);
    }
    for (size_t i = 0; i < params->num_subsets; i++) {
      printf("%u,", csv[i]);
    }
    for (size_t i = 0; i < params->num_subsets; i++) {
      printf("%.2f,", psv[i]);
    }
    for (size_t i = 0; i < params->num_channels; i++) {
      printf("%u,", (uint8_t)iev[i]);
    }
    printf("\n");
#endif
  }
  // accumulate csv successes
  for (size_t i = 0; i < params->num_channels; i++) {
    if (iev[i]) {
      cesv[i]++;
    }
  }
}

void mc_run_simulation(float *result_vector, const struct mc_params *params) {
  uint16_t csv[MC_MAX_EVENT_CHANNELS] = {0};
  // calculate maximum iterations from channel iteration triggers
  const uint8_t max_iterations = get_max_iterations(params->channels, params->num_channels);
  // initialize seed for randomizer
  srand(time(NULL));
  print_csv_header(params->num_channels);
  for (uint64_t epoch = 1; epoch < params->max_epochs; epoch++) {
    simulate(csv, params, max_iterations);
    update_stats(result_vector, csv, params->num_channels, epoch);
    report(epoch, csv, result_vector, params->num_channels);
  }
}

