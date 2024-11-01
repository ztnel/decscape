// monte carlo simulation engine for random select no replacement

#pragma once

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>

#define MC_MAX_TEMPORAL_NODES 20
#define MC_MAX_COMPOSITION_NODES MC_MAX_TEMPORAL_NODES
#define MC_MAX_EPOCHS 5000
#define MC_MAX_SUBSETS 10

typedef bool (*temporal_activation_func)(const uint16_t *samples);
typedef bool (*composition_activation_func)(const bool *event_vector);

struct temporal_node {
  uint8_t iteration_trigger;
  temporal_activation_func activation;
};

struct composition_node {
  struct temporal_node inputs[MC_MAX_TEMPORAL_NODES];
  composition_activation_func activation;
};

struct mc_params {
  uint64_t max_epochs;
  float target_margin;
  uint16_t cardinality_vector[MC_MAX_SUBSETS];
  size_t num_subsets;
  struct temporal_node temporal_nodes[MC_MAX_TEMPORAL_NODES];
  size_t num_temporal_nodes;
  struct composition_node composition_nodes[MC_MAX_COMPOSITION_NODES];
  size_t num_composition_nodes;
};

void mc_run_simulation(float *result_vector, const struct mc_params *params);
