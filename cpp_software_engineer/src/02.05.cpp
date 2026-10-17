#include <cmath>
#include <cstddef>
#include <iostream>
#include <print>

int main()
{
    double epsilon = 0.0;
    if (!(std::cin >> epsilon) || !std::isfinite(epsilon) || epsilon <= 0.0)
    {
        std::print("Expected a finite positive epsilon.\n");
        return 1;
    }
    // Manual correction of AI-generated code: validate the supported threshold before summation.
    // After maximum_terms terms, the first omitted Leibniz term is 4/(2*maximum_terms+1).
    constexpr std::size_t maximum_terms = 10000000;
    constexpr double minimum_threshold = 4.0 / (2.0 * maximum_terms + 1.0);
    if (epsilon <= minimum_threshold)
    {
        std::print("Leibniz summation supports epsilon > {:.17g} (at most {} terms).\n",
                   minimum_threshold, maximum_terms);
        return 1;
    }
    double pi = 0.0;
    double compensation = 0.0;
    double denominator = 1.0;
    double sign = 1.0;
    double pi_term = 4.0;
    while (std::abs(pi_term) >= epsilon)
    {
        // Manual correction of AI-generated code: compensated summation reduces roundoff.
        const double adjusted = pi_term - compensation;
        const double next = pi + adjusted;
        compensation = (next - pi) - adjusted;
        pi = next;
        denominator += 2.0;
        sign = -sign;
        pi_term = sign * 4.0 / denominator;
    }
    double e = 0.0;
    double e_term = 1.0;
    double next_factor = 1.0;
    double e_tail_bound = 3.0;
    // Manual correction of AI-generated code: also bound the whole omitted Maclaurin tail.
    // At omitted index m >= 1, tail <= (1/m!)*(m+1)/m; at m=0, e < 3.
    while (e_term >= epsilon || e_tail_bound >= epsilon)
    {
        e += e_term;
        e_term /= next_factor;
        next_factor += 1.0;
        e_tail_bound = e_term * next_factor / (next_factor - 1.0);
    }
    std::print("pi = {:.17g}\ne = {:.17g}\n", pi, e);
    std::print("Truncation-error bounds (exact arithmetic; roundoff excluded): "
               "pi error <= {:.17g}, e error <= {:.17g}.\n",
               std::abs(pi_term), e_tail_bound);
}
