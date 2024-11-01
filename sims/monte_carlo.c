
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/wait.h>
#include <time.h>

#include "monte_carlo.h"

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

static void sample_distribution(uint16_t *distribution, uint16_t *samples, const float *psv, const size_t num_subsets) {
  const float seed = generate_seed();
  float cumulative_probability = 0.0f;
  for (size_t i = 0; i < num_subsets; i++) {
    cumulative_probability += psv[i] + FP_TOLERANCE;
    if (seed < cumulative_probability) {
      distribution[i]--;
      samples[i]++;
      break;
    }
  }
}

/**
 * @brief Find the maximum iterations from the maximum iteration required in temporal layer
 *
 * @return Maximum number of iterations
 */
static uint8_t get_temporal_layer_max_iterations(const struct temporal_node *nodes, size_t num_channels) {
  uint8_t max_iterations = 0;
  for (size_t i = 0; i < num_channels; i++) {
    if (nodes[i].iteration_trigger > max_iterations) {
      max_iterations = nodes[i].iteration_trigger;
    }
  }
  return max_iterations;
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

static void simulate(uint16_t cumulative_events[MC_MAX_COMPOSITION_NODES], const struct mc_params *params, const uint8_t max_iterations) {
  uint16_t distribution[MC_MAX_SUBSETS] = {0};
  bool temporal_layer_output[MC_MAX_TEMPORAL_NODES] = {0};
  bool composition_layer_output[MC_MAX_COMPOSITION_NODES] = {0};
  float probability_vector[MC_MAX_SUBSETS] = {0.0f};
  uint16_t samples[MC_MAX_SUBSETS] = {0};
  memcpy(distribution, params->cardinality_vector, sizeof(params->cardinality_vector[0]) * params->num_subsets);
  for (uint8_t iteration = 1; iteration <= max_iterations; iteration++) {
    state_estimator(probability_vector, distribution, params->num_subsets);
    sample_distribution(distribution, samples, probability_vector, params->num_subsets);
    // run temporal layer
    for (size_t i = 0; i < params->num_temporal_nodes; i++) {
      const struct temporal_node *node = &params->temporal_nodes[i];
      if (node->iteration_trigger == iteration) {
        temporal_layer_output[i] = node->activation(samples);
      }
    }
  }
  // feedforward temporal layer outputs to run composition layer
  for (size_t i = 0; i < params->num_composition_nodes; i++) {
    const struct composition_node *node = &params->composition_nodes[i];
    composition_layer_output[i] = node->activation(temporal_layer_output);
  }
  // accumulate composition layer outputs
  for (size_t i = 0; i < params->num_composition_nodes; i++) {
    if (composition_layer_output[i]) {
      cumulative_events[i]++;
    }
  }
}

void mc_run_simulation(float *result_vector, const struct mc_params *params) {
  uint16_t cumulative_events[MC_MAX_COMPOSITION_NODES] = {0};
  // calculate maximum iterations from channel iteration triggers
  const uint8_t max_iterations = get_temporal_layer_max_iterations(params->temporal_nodes, params->num_temporal_nodes);
  // initialize seed for randomizer
  srand(time(NULL));
  print_csv_header(params->num_composition_nodes);
  for (uint64_t epoch = 1; epoch < params->max_epochs; epoch++) {
    simulate(cumulative_events, params, max_iterations);
    update_stats(result_vector, cumulative_events, params->num_composition_nodes, epoch);
    report(epoch, cumulative_events, result_vector, params->num_composition_nodes);
  }
}
