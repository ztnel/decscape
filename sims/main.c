
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

static bool event_test_1(const uint16_t csv[NUM_SUBSETS], const bool iev[NUM_CHANNELS]) {
  return csv[LAND] >= 1;
}

static bool event_test_2(const uint16_t csv[NUM_SUBSETS], const bool iev[NUM_CHANNELS]) {
  return csv[ENGINE] == 1;
}

static bool event_test_3(const uint16_t csv[NUM_SUBSETS], const bool iev[NUM_CHANNELS]) {
  return csv[RITUAL] == 1;
}

static bool event_test_4(const uint16_t csv[NUM_SUBSETS], const bool iev[NUM_CHANNELS]) {
  return csv[INTERACTION] == 1;
}

static bool event_test_5(const uint16_t csv[NUM_SUBSETS], const bool iev[NUM_CHANNELS]) {
  return csv[ARTIFACT] == 1;
}

static bool event_test_6(const uint16_t csv[NUM_SUBSETS], const bool iev[NUM_CHANNELS]) {
  return csv[CANTRIP] == 1;
}

static bool event_test_joint(const uint16_t csv[NUM_SUBSETS], const bool iev[NUM_CHANNELS]) {
  return iev[CH1] & iev[CH2] & iev[CH3] & iev[CH4] & iev[CH5] & iev[CH6];
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
      [OTHER] = 4
    },
    .num_subsets = NUM_SUBSETS,
    // channel registration (probe points)
    .channels = {
      [CH1] = {
        .iteration_trigger = 7,
        .event_test_cb = event_test_1
      },
      // order matters!
      [CH2] = {
        .iteration_trigger = 7,
        .event_test_cb = event_test_2
      },
      [CH3] = {
        .iteration_trigger = 7,
        .event_test_cb = event_test_3
      },
      [CH4] = {
        .iteration_trigger = 7,
        .event_test_cb = event_test_4
      },
      [CH5] = {
        .iteration_trigger = 7,
        .event_test_cb = event_test_5
      },
      [CH6] = {
        .iteration_trigger = 7,
        .event_test_cb = event_test_6
      },
      [CH7] = {
        .iteration_trigger = 7,
        .event_test_cb = event_test_joint
      }
    },
    .num_channels = NUM_CHANNELS
  };
  float result_vector[NUM_CHANNELS];
  mc_run_simulation((float *)&result_vector, &params);
}

int main(void) {
  test_for_land_ratios();
}
