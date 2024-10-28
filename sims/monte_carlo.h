// monte carlo simulation engine for random select no replacement

#pragma once

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#define MC_MAX_EVENT_CHANNELS 20
#define MC_MAX_EPOCHS 5000
#define MC_MAX_SUBSETS 10

typedef bool (*event_test_cb_t)(const uint16_t *csv, const bool *iev);

struct mc_event_channel {
  uint8_t iteration_trigger;
  event_test_cb_t event_test_cb;
};

struct mc_params {
  uint64_t max_epochs;
  float target_margin;
  uint16_t cardinality_vector[MC_MAX_SUBSETS];
  size_t num_subsets;
  struct mc_event_channel channels[MC_MAX_EVENT_CHANNELS];
  size_t num_channels;
};

void mc_run_simulation(float *result_vector, const struct mc_params *params);
