#include <cmath>
#include <cstddef>
#include <iostream>
#include <numeric>
#include <print>
#include <stdexcept>
#include <utility>

struct Statistics
{
    double minimum = 0.0;
    double maximum = 0.0;
    double median = 0.0;
    double mean = 0.0;
    double deviation = 0.0;
};

Statistics summarize(double* values, std::size_t size)
{
    if (size == 0)
    {
        throw std::invalid_argument("Empty collection");
    }
    for (std::size_t end = size; end > 1; --end)
    {
        bool changed = false;
        for (std::size_t index = 1; index < end; ++index)
        {
            if (values[index - 1] > values[index])
            {
                std::swap(values[index - 1], values[index]);
                changed = true;
            }
        }
        if (!changed)
        {
            break;
        }
    }
    // Manual correction of AI-generated code : Neumaier summation preserves small cancellation residuals.
    // Input is bounded by 1e100; allocated element counts bound the sum.
    double sum = 0.0;
    double correction = 0.0;
    for (std::size_t index = 0; index < size; ++index)
    {
        const double value = values[index];
        const double next = sum + value;
        correction += std::abs(sum) >= std::abs(value)
            ? (sum - next) + value : (value - next) + sum;
        sum = next;
    }
    const double mean = (sum + correction) / static_cast<double>(size);
    // Population variance: sum((x-mean)^2)/N, not the N-1 estimate.
    double variance = 0.0;
    for (std::size_t index = 0; index < size; ++index)
    {
        const double difference = values[index] - mean;
        variance += (difference * difference - variance) / static_cast<double>(index + 1);
    }
    const std::size_t middle = size / 2;
    const double median = size % 2 == 0 ? std::midpoint(values[middle - 1], values[middle]) : values[middle];
    return {values[0], values[size - 1], median, mean, std::sqrt(variance)};
}

void show(const Statistics& result)
{
    std::print("min = {:.17g}\nmax = {:.17g}\nmedian = {:.17g}\nmean = {:.17g}\nstddev = {:.17g}\n",
               result.minimum, result.maximum, result.median, result.mean, result.deviation);
}

int main()
{
    constexpr std::size_t maximum_size = 10000;
    constexpr double value_limit = 1e100;
    double values[maximum_size] = {};
    int count = 0;
    if (!(std::cin >> count) || count <= 0 || count > static_cast<int>(maximum_size))
    {
        std::print("Expected collection size in [1, {}].\n", maximum_size);
        return 1;
    }
    const auto size = static_cast<std::size_t>(count);
    for (std::size_t index = 0; index < size; ++index)
    {
        if (!(std::cin >> values[index]) || !std::isfinite(values[index]) || std::abs(values[index]) > value_limit)
        {
            std::print("Expected finite values with absolute values <= {}.\n", value_limit);
            return 1;
        }
    }
    show(summarize(values, size));
}
