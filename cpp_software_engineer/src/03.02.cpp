#include <algorithm>
#include <cassert>
#include <cmath>
#include <limits>
#include <numbers>
#include <print>
#include <stdexcept>

void validate_length(double value)
{
    constexpr double maximum_length = 1e100;
    if (!std::isfinite(value) || value <= 0.0 || value > maximum_length)
    {
        throw std::invalid_argument("Length must be finite, positive and at most 1e100");
    }
}

bool close(double actual, double expected)
{
    constexpr double tolerance = 1e-12;
    return std::abs(actual - expected) <= tolerance * std::max(1.0, std::abs(expected));
}

class Circle
{
private:
    double radius_ = 0.0;

public:
    explicit Circle(double radius) : radius_(radius)
    {
        validate_length(radius_);
    }

    double perimeter() const
    {
        return 2.0 * std::numbers::pi * radius_;
    }

    double area() const
    {
        return std::numbers::pi * radius_ * radius_;
    }
};

class Triangle
{
private:
    double first_ = 0.0;
    double second_ = 0.0;
    double third_ = 0.0;

public:
    Triangle(double first, double second, double third) : first_(first), second_(second), third_(third)
    {
        validate_length(first_);
        validate_length(second_);
        validate_length(third_);
        if (first_ < second_)
        {
            std::swap(first_, second_);
        }
        if (second_ < third_)
        {
            std::swap(second_, third_);
        }
        if (first_ < second_)
        {
            std::swap(first_, second_);
        }
        if (third_ <= first_ - second_)
        {
            throw std::invalid_argument("Triangle inequality failed");
        }
    }

    double perimeter() const
    {
        return first_ + second_ + third_;
    }

    double area() const
    {
        const double first_factor = first_ + (second_ + third_);
        const double second_factor = third_ - (first_ - second_);
        const double third_factor = third_ + (first_ - second_);
        const double fourth_factor = first_ + (second_ - third_);
        return (std::sqrt(first_factor) * std::sqrt(second_factor))
             * (std::sqrt(third_factor) * std::sqrt(fourth_factor)) / 4.0;
    }
};

class Square
{
private:
    double side_ = 0.0;

public:
    explicit Square(double side) : side_(side)
    {
        validate_length(side_);
    }

    double perimeter() const
    {
        return 4.0 * side_;
    }

    double area() const
    {
        return side_ * side_;
    }
};

// Manual correction of AI-generated code : check every constructor argument and invalid triangle shapes.
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
    for (double invalid : {0.0, -1.0, 1e101, std::numeric_limits<double>::infinity(),
                           std::numeric_limits<double>::quiet_NaN()})
    {
        expect_invalid([=] { static_cast<void>(Circle(invalid)); });
        expect_invalid([=] { static_cast<void>(Square(invalid)); });
        expect_invalid([=] { static_cast<void>(Triangle(invalid, 2.0, 2.0)); });
        expect_invalid([=] { static_cast<void>(Triangle(2.0, invalid, 2.0)); });
        expect_invalid([=] { static_cast<void>(Triangle(2.0, 2.0, invalid)); });
    }
    expect_invalid([] { static_cast<void>(Triangle(1.0, 2.0, 4.0)); });
    expect_invalid([] { static_cast<void>(Triangle(3.0, 1.0, 2.0)); });

    const Circle circle(2.0);
    assert(close(circle.perimeter(), 4.0 * std::numbers::pi));
    assert(close(circle.area(), 4.0 * std::numbers::pi));
    const Triangle triangle(3.0, 4.0, 5.0);
    assert(close(triangle.perimeter(), 12.0));
    assert(close(triangle.area(), 6.0));
    assert(close(Triangle(5.0, 3.0, 4.0).area(), 6.0));
    const Square square(3.0);
    assert(close(square.perimeter(), 12.0));
    assert(close(square.area(), 9.0));
    for (double invalid : {0.0, -1.0, std::numeric_limits<double>::infinity(),
                           std::numeric_limits<double>::quiet_NaN()})
    {
        bool rejected = false;
        try
        {
            static_cast<void>(Circle(invalid));
        }
        catch (const std::invalid_argument&)
        {
            rejected = true;
        }
        assert(rejected);
    }
    bool rejected = false;
    try
    {
        static_cast<void>(Triangle(1.0, 2.0, 3.0));
    }
    catch (const std::invalid_argument&)
    {
        rejected = true;
    }
    assert(rejected);
}

int main()
{
    test();
    const Circle circle(2.0);
    const Triangle triangle(3.0, 4.0, 5.0);
    const Square square(3.0);
    std::print("Circle: P = {}, A = {}\nTriangle: P = {}, A = {}\nSquare: P = {}, A = {}\n",
               circle.perimeter(), circle.area(), triangle.perimeter(), triangle.area(),
               square.perimeter(), square.area());
}
