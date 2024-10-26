
#include "stats.h"

float stats_fstd(const float samples[], const size_t size, const bool sample_std) {
  if (size < 1 || size <= 1 && sample_std) {
    return NAN;
  }
  // calculate variance using Welford's online algorithm
  double mean = 0.0;
  double m2 = 0.0;
  for (size_t i = 0; i < size; i++) {
    float delta = samples[i] - mean;
    mean += samples[i] / (i + 1);
    m2 += delta * (samples[i] - mean);
  }
  return sqrtf(m2 / (sample_std ? size - 1 : size));
}

float stats_fmean(const float samples[], const size_t size) {
  if (size < 1) {
    return NAN;
  }
  double acc_sum = 0.0;
  for (size_t i = 0; i < size; i++) {
    acc_sum += samples[i] / (i + 1);
  }
  return (float)(acc_sum / size);
}

float stats_rse(const float mean, const float std) {
  if (mean < 1) {
    return NAN;
  }
  return std / mean;
}
