#include <print>

int main()
{
    constexpr int radix = 10;
    for (int hundreds = 1; hundreds < radix; ++hundreds)
    {
        for (int tens = 0; tens < radix; ++tens)
        {
            for (int units = 0; units < radix; ++units)
            {
                const int number = hundreds * radix * radix + tens * radix + units;
                const int cube_sum = hundreds * hundreds * hundreds + tens * tens * tens + units * units * units;
                if (number == cube_sum)
                {
                    std::print("{}\n", number);
                }
            }
        }
    }
}
