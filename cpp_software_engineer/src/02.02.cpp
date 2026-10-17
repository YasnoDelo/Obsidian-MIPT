#include <algorithm>
#include <cmath>
#include <iostream>
#include <limits>
#include <print>

int main()
{
    constexpr long double epsilon = 1e-12L;
    double input_a = 0.0;
    double input_b = 0.0;
    double input_c = 0.0;
    if (!(std::cin >> input_a >> input_b >> input_c)
        || !std::isfinite(input_a) || !std::isfinite(input_b) || !std::isfinite(input_c))
    {
        std::print("Expected finite double coefficients.\n");
        return 1;
    }
    // Manual correction of AI-generated code: do not discard a nonzero leading coefficient.
    // Wider intermediates prevent overflow/underflow in products of finite double inputs.
    // This implementation requires an extended-range long double (e.g. GCC on x86-64 Linux).
    static_assert(std::numeric_limits<long double>::max_exponent
                  > 2 * std::numeric_limits<double>::max_exponent + 4);
    static_assert(std::numeric_limits<long double>::min_exponent
                  < 2 * (std::numeric_limits<double>::min_exponent
                         - std::numeric_limits<double>::digits) - 4);
    const long double a = input_a;
    const long double b = input_b;
    const long double c = input_c;
    if (a == 0.0L)
    {
        if (b == 0.0L)
        {
            std::print("{}\n", c == 0.0L ? "Infinitely many roots" : "No real roots");
        }
        else
        {
            std::print("Root: {:.17g}\n", -c / b);
        }
        return 0;
    }
    const long double square_b = b * b;
    const long double four_ac = 4.0L * a * c;
    const long double discriminant = std::fma(-4.0L * a, c, square_b);
    const long double discriminant_scale = std::abs(square_b) + std::abs(four_ac);
    // Epsilon classifies only near-zero discriminants, relative to the terms forming D.
    // A nonzero D within tolerance gives an explicitly labelled approximate double root.
    if (std::abs(discriminant) <= epsilon * discriminant_scale)
    {
        std::print("Root (discriminant treated as zero within relative tolerance): {:.17g}\n",
                   -b / (2.0L * a));
    }
    else if (discriminant < 0.0L)
    {
        std::print("No real roots\n");
    }
    else
    {
        const long double q = -0.5L * (b + std::copysign(std::sqrt(discriminant), b));
        const long double first = q / a;
        const long double second = c / q;
        std::print("Roots: {:.17g} {:.17g}\n", std::min(first, second), std::max(first, second));
    }
}
