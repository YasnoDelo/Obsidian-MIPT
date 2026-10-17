#include <cassert>
#include <limits>
#include <numeric>
#include <print>
#include <stdexcept>

int gcd_recursive(int first, int second)
{
    if (first < 0 || second < 0)
    {
        throw std::invalid_argument("Negative GCD argument");
    }
    return second == 0 ? first : gcd_recursive(second, first % second);
}

int gcd_iterative(int first, int second)
{
    if (first < 0 || second < 0)
    {
        throw std::invalid_argument("Negative GCD argument");
    }
    while (second != 0)
    {
        const int remainder = first % second;
        first = second;
        second = remainder;
    }
    return first;
}

int lcm(int first, int second)
{
    if (first <= 0 || second <= 0)
    {
        throw std::invalid_argument("LCM requires positive integers");
    }
    const int quotient = first / gcd_iterative(first, second);
    if (quotient > std::numeric_limits<int>::max() / second)
    {
        throw std::overflow_error("LCM does not fit int");
    }
    return quotient * second;
}

// Manual correction of AI-generated code : cover rejected arguments and supported zero GCD inputs.
template <typename Action>
void expect_invalid(Action action)
{
    bool rejected = false;
    try { action(); }
    catch (const std::invalid_argument&) { rejected = true; }
    assert(rejected);
}

void test()
{
    assert(gcd_recursive(0, 0) == 0 && gcd_iterative(0, 0) == 0);
    assert(gcd_recursive(0, 7) == 7 && gcd_iterative(0, 7) == 7);
    assert(gcd_recursive(7, 0) == 7 && gcd_iterative(7, 0) == 7);
    for (int negative : {-1, std::numeric_limits<int>::min()})
    {
        expect_invalid([=] { gcd_recursive(negative, 1); });
        expect_invalid([=] { gcd_recursive(1, negative); });
        expect_invalid([=] { gcd_iterative(negative, 1); });
        expect_invalid([=] { gcd_iterative(1, negative); });
        expect_invalid([=] { lcm(negative, 1); });
        expect_invalid([=] { lcm(1, negative); });
    }
    expect_invalid([] { lcm(1, 0); });
    expect_invalid([] { lcm(0, 0); });
    constexpr int test_limit = 100;
    for (int first = 1; first <= test_limit; ++first)
    {
        for (int second = 1; second <= test_limit; ++second)
        {
            assert(gcd_recursive(first, second) == std::gcd(first, second));
            assert(gcd_iterative(first, second) == std::gcd(first, second));
            assert(lcm(first, second) == std::lcm(first, second));
        }
    }
    constexpr int maximum = std::numeric_limits<int>::max();
    assert(lcm(maximum, maximum) == maximum);
    assert(gcd_recursive(maximum, maximum - 1) == 1);
    assert(gcd_iterative(maximum, maximum - 1) == 1);
    bool overflow_rejected = false;
    try
    {
        static_cast<void>(lcm(maximum, maximum - 1));
    }
    catch (const std::overflow_error&)
    {
        overflow_rejected = true;
    }
    assert(overflow_rejected);
    bool zero_rejected = false;
    try
    {
        static_cast<void>(lcm(0, 1));
    }
    catch (const std::invalid_argument&)
    {
        zero_rejected = true;
    }
    assert(zero_rejected);
}

int main()
{
    test();
    constexpr int first = 48;
    constexpr int second = 18;
    std::print("gcd({}, {}) = {}\nlcm({}, {}) = {}\n", first, second,
               gcd_recursive(first, second), first, second, lcm(first, second));
}
