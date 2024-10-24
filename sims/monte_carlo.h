
#pragma once


#include <stdint.h>

void monte_carlo_init(void);
float monte_carlo_run(uint8_t successes, uint8_t n_successes, const uint32_t epochs);

