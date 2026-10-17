#include <algorithm>
#include <cassert>
#include <cstddef>
#include <limits>
#include <numeric>
#include <print>
#include <random>
#include <utility>
#include <vector>

void order(std::vector<int>& values, std::size_t left, std::size_t right)
{
    if (left == right)
    {
        return;
    }
    for (std::size_t index = left + 1; index < right; ++index)
    {
        for (std::size_t current = index; current > left && values[current - 1] > values[current]; --current)
        {
            std::swap(values[current], values[current - 1]);
        }
    }
}

int median(int first, int middle, int last)
{
    if (first > middle)
    {
        std::swap(first, middle);
    }
    if (middle > last)
    {
        std::swap(middle, last);
    }
    return std::max(first, middle);
}

std::size_t partition(std::vector<int>& values, std::size_t left, std::size_t right)
{
    const int pivot = median(values[left], values[std::midpoint(left, right - 1)], values[right - 1]);
    std::size_t lower = left;
    std::size_t upper = right - 1;
    while (true)
    {
        while (values[lower] < pivot)
        {
            ++lower;
        }
        while (values[upper] > pivot)
        {
            --upper;
        }
        if (lower >= upper)
        {
            return upper + 1;
        }
        std::swap(values[lower], values[upper]);
        ++lower;
        --upper;
    }
}

void split(std::vector<int>& values, std::size_t left, std::size_t right)
{
    constexpr std::size_t insertion_threshold = 16;
    while (right - left > insertion_threshold)
    {
        const std::size_t middle = partition(values, left, right);
        if (middle - left < right - middle)
        {
            split(values, left, middle);
            left = middle;
        }
        else
        {
            split(values, middle, right);
            right = middle;
        }
    }
    order(values, left, right);
}

void sort(std::vector<int>& values)
{
    split(values, 0, values.size());
}

void verify(std::vector<int> values)
{
    auto expected = values;
    std::ranges::sort(expected);
    sort(values);
    assert(values == expected);
}

void test()
{
    verify({});
    verify({1});
    verify({2, 1});
    verify({std::numeric_limits<int>::max(), 0, std::numeric_limits<int>::min()});
    constexpr std::size_t test_size = 1024;
    verify(std::vector<int>(test_size, 7));
    std::vector<int> ordered(test_size, 0);
    std::iota(ordered.begin(), ordered.end(), 0);
    verify(ordered);
    std::ranges::reverse(ordered);
    verify(ordered);
    constexpr unsigned seed = 2044;
    constexpr std::size_t maximum_test_size = 300;
    constexpr int value_limit = 20;
    std::mt19937 generator(seed);
    std::uniform_int_distribution<int> distribution(-value_limit, value_limit);
    for (std::size_t size = 0; size <= maximum_test_size; ++size)
    {
        std::vector<int> values(size, 0);
        for (int& value : values)
        {
            value = distribution(generator);
        }
        verify(values);
    }
}

int main()
{
    test();
    constexpr std::size_t size = 1uz << 10;
    std::vector<int> values(size, 0);
    for (std::size_t index = 0; index < size; ++index)
    {
        values[index] = static_cast<int>(size - index);
    }
    sort(values);
    assert(std::ranges::is_sorted(values));
    std::print("Sorted {} values: first = {}, last = {}\n", values.size(), values.front(), values.back());
}
