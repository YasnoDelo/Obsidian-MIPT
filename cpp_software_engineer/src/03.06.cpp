#include <algorithm>
#include <cassert>
#include <cmath>
#include <limits>
#include <numbers>
#include <print>
#include <stdexcept>
#include <array>
#include <memory>
#include <type_traits>
#include <vector>

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

class Shape
{
public:
    virtual ~Shape() = default;
    virtual double perimeter() const = 0;
    virtual double area() const = 0;
};

class Polygon : public Shape
{
};

class Circle final : public Shape
{
private:
    double radius_ = 0.0;

public:
    explicit Circle(double radius) : radius_(radius)
    {
        validate_length(radius_);
    }

    double perimeter() const override
    {
        return 2.0 * std::numbers::pi * radius_;
    }

    double area() const override
    {
        return std::numbers::pi * radius_ * radius_;
    }
};

class Triangle : public Polygon
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

    double perimeter() const override
    {
        return first_ + second_ + third_;
    }

    double area() const override
    {
        const double first_factor = first_ + (second_ + third_);
        const double second_factor = third_ - (first_ - second_);
        const double third_factor = third_ + (first_ - second_);
        const double fourth_factor = first_ + (second_ - third_);
        return (std::sqrt(first_factor) * std::sqrt(second_factor))
             * (std::sqrt(third_factor) * std::sqrt(fourth_factor)) / 4.0;
    }
};

class Rectangle : public Polygon
{
private:
    double width_ = 0.0;
    double height_ = 0.0;

public:
    Rectangle(double width, double height) : width_(width), height_(height)
    {
        validate_length(width_);
        validate_length(height_);
    }

    double perimeter() const override final
    {
        return 2.0 * (width_ + height_);
    }

    double area() const override final
    {
        return width_ * height_;
    }
};

class Square final : public Rectangle
{
public:
    explicit Square(double side) : Rectangle(side, side)
    {
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
        expect_invalid([=] { static_cast<void>(Rectangle(invalid, 2.0)); });
        expect_invalid([=] { static_cast<void>(Rectangle(2.0, invalid)); });
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

// Manual correction of AI-generated code : share construction between demonstration and dispatch tests.
std::vector<std::unique_ptr<Shape>> make_shapes()
{
    std::vector<std::unique_ptr<Shape>> shapes;
    shapes.push_back(std::make_unique<Circle>(2.0));
    shapes.push_back(std::make_unique<Triangle>(3.0, 4.0, 5.0));
    shapes.push_back(std::make_unique<Square>(3.0));
    return shapes;
}

void test_polymorphism()
{
    static_assert(std::is_abstract_v<Shape>);
    static_assert(std::is_abstract_v<Polygon>);
    static_assert(std::has_virtual_destructor_v<Shape>);
    static_assert(std::is_final_v<Circle>);
    static_assert(std::is_final_v<Square>);
    auto shapes = make_shapes();
    const std::array expected_areas{4.0 * std::numbers::pi, 6.0, 9.0};
    const std::array expected_perimeters{4.0 * std::numbers::pi, 12.0, 12.0};
    for (std::size_t index = 0; index < shapes.size(); ++index)
    {
        assert(close(shapes[index]->area(), expected_areas[index]));
        assert(close(shapes[index]->perimeter(), expected_perimeters[index]));
    }
    const Rectangle rectangle(2.0, 3.0);
    assert(close(rectangle.perimeter(), 10.0) && close(rectangle.area(), 6.0));
}

int main()
{
    test();
    test_polymorphism();
    auto shapes = make_shapes();
    for (const auto& shape : shapes)
    {
        std::print("P = {}, A = {}\n", shape->perimeter(), shape->area());
    }
}
