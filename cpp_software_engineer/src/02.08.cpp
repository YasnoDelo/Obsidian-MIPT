#include <cstddef>
#include <print>
#include <vector>

int main()
{
    constexpr unsigned long long int maximum_start = 100;
    constexpr unsigned long long int odd_multiplier = 3;
    std::vector<std::size_t> lengths(maximum_start + 1, 0);
    lengths[1] = 1;
    std::size_t maximum_length = 1;
    unsigned long long int best_start = 1;
    for (unsigned long long int start = 2; start <= maximum_start; ++start)
    {
        auto value = start;
        std::size_t steps = 0;
        while (value > maximum_start || lengths[static_cast<std::size_t>(value)] == 0)
        {
            value = value % 2 == 0 ? value / 2 : odd_multiplier * value + 1;
            ++steps;
        }
        lengths[static_cast<std::size_t>(start)] = steps + lengths[static_cast<std::size_t>(value)];
        if (lengths[static_cast<std::size_t>(start)] > maximum_length)
        {
            maximum_length = lengths[static_cast<std::size_t>(start)];
            best_start = start;
        }
    }
    // Manual correction of AI-generated code : length counts both the initial value and final 1.
    std::print("start = {}\nlength (elements, including start and 1) = {}\n", best_start, maximum_length);
}
