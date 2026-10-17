#include <cmath>
#include <cstddef>
#include <exception>
#include <iostream>
#include <numeric>
#include <print>
#include <stdexcept>
#include <utility>
#include <cassert>
#include <limits>
#include <memory>

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

void append(std::unique_ptr<double[]>& values, std::size_t& size, std::size_t& capacity, double value)
{
    constexpr std::size_t initial_capacity = 1;
    constexpr std::size_t growth_factor = 2;
    if (size == capacity)
    {
        if (capacity > std::numeric_limits<std::size_t>::max() / sizeof(double) / growth_factor)
        {
            throw std::length_error("Collection is too large");
        }
        const std::size_t next_capacity = capacity == 0 ? initial_capacity : capacity * growth_factor;
        std::unique_ptr<double[]> next(new double[next_capacity]{});
        for (std::size_t index = 0; index < size; ++index)
        {
            next[index] = values[index];
        }
        values.swap(next);
        capacity = next_capacity;
    }
    values[size++] = value;
}

void test()
{
    std::unique_ptr<double[]> values;
    std::size_t size = 0;
    std::size_t capacity = 0;
    bool rejected = false;
    try
    {
        static_cast<void>(summarize(values.get(), size));
    }
    catch (const std::invalid_argument&)
    {
        rejected = true;
    }
    assert(rejected);
    append(values, size, capacity, 4.0);
    assert(size == 1 && capacity == 1);
    auto result = summarize(values.get(), size);
    assert(result.minimum == 4.0 && result.maximum == 4.0 && result.median == 4.0);
    assert(result.mean == 4.0 && result.deviation == 0.0);
    append(values, size, capacity, -2.0);
    append(values, size, capacity, 2.0);
    assert(size == 3 && capacity == 4);
    result = summarize(values.get(), size);
    constexpr double tolerance = 1e-12;
    assert(result.minimum == -2.0 && result.maximum == 4.0 && result.median == 2.0);
    assert(std::abs(result.mean - 4.0 / 3.0) < tolerance);
    assert(std::abs(result.deviation - std::sqrt(56.0 / 9.0)) < tolerance);
    append(values, size, capacity, 0.0);
    result = summarize(values.get(), size);
    assert(result.median == 1.0 && result.mean == 1.0);
    assert(std::abs(result.deviation - std::sqrt(5.0)) < tolerance);
    append(values, size, capacity, 0.0);
    assert(size == 5 && capacity == 8);
    assert(values[0] == -2.0 && values[3] == 4.0 && values[4] == 0.0);
    // Manual correction of AI-generated code : regression for severe cancellation.
    double cancellation[] = {-1e100, 1.0, 1e100};
    assert(std::abs(summarize(cancellation, 3).mean - 1.0 / 3.0) < tolerance);
}

int main()
{
    try
    {
        test();
        std::print("Enter numbers until EOF (Ctrl+D on an empty line on Linux).\n");
        constexpr double value_limit = 1e100;
        std::unique_ptr<double[]> values;
        std::size_t size = 0;
        std::size_t capacity = 0;
        double value = 0.0;
        while (true)
        {
            std::cin >> std::ws;
            if (std::cin.eof())
            {
                break;
            }
            if (!(std::cin >> value))
            {
                throw std::invalid_argument("Invalid numeric input");
            }
            if (!std::isfinite(value) || std::abs(value) > value_limit)
            {
                throw std::invalid_argument("Value is outside the supported range");
            }
            append(values, size, capacity, value);
        }
        if (!std::cin.eof() || std::cin.bad())
        {
            throw std::invalid_argument("Invalid input");
        }
        show(summarize(values.get(), size));
    }
    catch (const std::exception& error)
    {
        std::print("Error: {}\n", error.what());
        return 1;
    }
}
