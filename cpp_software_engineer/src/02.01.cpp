// Manual correction of AI-generated code: Binet derivation and supported index range.
// F(0)=0, F(1)=1; r*r=r+1 has roots phi and psi.
// F(n)=A*phi^n+B*psi^n; A+B=0 and A*(phi-psi)=1.
// Hence F(n)=(phi^n-psi^n)/sqrt(5). This satisfies both initial
// conditions and the recurrence, whose solution is unique.
// F(46)=1836311903 fits a 32-bit int; F(47)=2971215073 does not.
#include <cmath>
#include <iostream>
#include <limits>
#include <print>

int main()
{
    constexpr int maximum_index = 46;
    static_assert(std::numeric_limits<int>::digits >= 31);
    int index = 0;
    if (!(std::cin >> index) || index < 0 || index > maximum_index)
    {
        std::print("Expected an integer in [0, {}].\n", maximum_index);
        return 1;
    }
    const double root_five = std::sqrt(5.0);
    const double phi = (1.0 + root_five) / 2.0;
    const double psi = (1.0 - root_five) / 2.0;
    const double approximation = (std::pow(phi, index) - std::pow(psi, index)) / root_five;
    const int result = static_cast<int>(std::round(approximation));
    std::print("F({}) = {}\n", index, result);
}
