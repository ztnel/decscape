
#include "monte_carlo.h"
#include <stdbool.h>

enum subsets {
  LAND = 0,
  ENGINE,
  INTERACTION,
  CANTRIP,
  ARTIFACT,
  RITUAL,
  OTHER,
  NUM_SUBSETS
};

enum channels {
  CH1 = 0,
  CH2,
  CH3,
  CH4,
  CH5,
  CH6,
  CH7,
  NUM_CHANNELS
};

static bool temporal_event_1(const uint16_t samples[NUM_SUBSETS]) {
  return samples[LAND] >= 1;
}

static bool temporal_event_2(const uint16_t samples[NUM_SUBSETS]) {
  return samples[ARTIFACT] >= 1;
}

static bool composition_event_1(const bool inputs[NUM_CHANNELS]) {
  return inputs[CH1] || inputs[CH2];
}

static void test_for_land_ratios() {
  struct mc_params params = {
      // convergence parameters
      .max_epochs = 10000,
      .target_margin = 0.01,
      // population parameters
      .cardinality_vector = {
          [LAND] = 15,
          [ENGINE] = 7,
          [INTERACTION] = 7,
          [CANTRIP] = 7,
          [ARTIFACT] = 13,
          [RITUAL] = 7,
          [OTHER] = 4},
      .num_subsets = NUM_SUBSETS,
      // channel registration (probe points)
      .temporal_nodes = {
          {.iteration_trigger = 7, .activation = temporal_event_1},
          {.iteration_trigger = 7, .activation = temporal_event_2},
      },
      .num_temporal_nodes = 2,
      .composition_nodes = {{.activation = composition_event_1}},
      .num_composition_nodes = 1};
  float result_vector[NUM_CHANNELS];
  mc_run_simulation((float *)&result_vector, &params);
}

int main(void) {
  test_for_land_ratios();
}
