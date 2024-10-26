
#pragma once

#include <math.h>
#include <stdbool.h>
#include <stddef.h>

/**
 * @brief Calculate standard deviation of floating point samples
 *
 * @param[in] samples Input samples
 * @param[in] size Sample size
 * @param[in] sample_std Flag to indicate sample standard deviation calculation (vs. population)
 * @return Standard deviation
 */
float stats_fstd(const float *samples, const size_t size, const bool sample_std);

/**
 * @brief Calculate sample mean
 *
 * @param[in] samples Input samples
 * @param[in] size Sample size
 * @return sample mean
 */
float stats_fmean(const float *samples, const size_t size);

/**
 * @brief Calculate relative standard error (RSE) of sample
 *
 * @param[in] mean Sample mean
 * @param[in] std Sample standard deviation
 * @return Relative standard error
 */
float stats_rse(const float mean, const float std);

