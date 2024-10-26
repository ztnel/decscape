
#pragma once

#include <stdint.h>

#define MC_MAX_EVENTS 20
#define MC_MAX_EPOCHS 5000

typedef void (*agent_cb_t)(uint64_t status, uint8_t successes, uint8_t sample_size);

struct mc_params {
  uint64_t max_epochs;
  float target_margin;
  uint64_t conv_check_interval;
};

struct mc_ctx {
  uint64_t epochs;
  uint64_t event_accumulator_vector[MC_MAX_EVENTS];
  float p_success_vector[MC_MAX_EVENTS];
};

void mc_init(void);
float mc_run(uint8_t successes, uint8_t n_successes, const uint32_t epochs);
