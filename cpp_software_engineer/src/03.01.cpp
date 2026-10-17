#include <algorithm>
#include <cassert>
#include <cstdint>
#include <limits>
#include <optional>
#include <print>
#include <stdexcept>
#include <vector>

struct Rectangle
{
    int left = 0;
    int top = 0;
    int right = 0;
    int bottom = 0;
};

void validate(const Rectangle& rectangle)
{
    if (rectangle.left > rectangle.right || rectangle.top > rectangle.bottom)
    {
        throw std::invalid_argument("Reversed rectangle coordinates");
    }
}

std::uint64_t area(const Rectangle& rectangle)
{
    validate(rectangle);
    static_assert(std::numeric_limits<int>::digits <= 31);
    const auto width = static_cast<std::uint64_t>(static_cast<std::int64_t>(rectangle.right) - rectangle.left);
    const auto height = static_cast<std::uint64_t>(static_cast<std::int64_t>(rectangle.bottom) - rectangle.top);
    return width * height;
}

std::uint64_t intersection_area(const std::vector<Rectangle>& rectangles)
{
    if (rectangles.empty())
    {
        return 0;
    }
    Rectangle intersection = rectangles.front();
    for (const auto& rectangle : rectangles)
    {
        validate(rectangle);
        intersection.left = std::max(intersection.left, rectangle.left);
        intersection.top = std::max(intersection.top, rectangle.top);
        intersection.right = std::min(intersection.right, rectangle.right);
        intersection.bottom = std::min(intersection.bottom, rectangle.bottom);
    }
    if (intersection.left >= intersection.right || intersection.top >= intersection.bottom)
    {
        return 0;
    }
    return area(intersection);
}

std::optional<Rectangle> bounding_rectangle(const std::vector<Rectangle>& rectangles)
{
    if (rectangles.empty())
    {
        return std::nullopt;
    }
    Rectangle bounds = rectangles.front();
    for (const auto& rectangle : rectangles)
    {
        validate(rectangle);
        bounds.left = std::min(bounds.left, rectangle.left);
        bounds.top = std::min(bounds.top, rectangle.top);
        bounds.right = std::max(bounds.right, rectangle.right);
        bounds.bottom = std::max(bounds.bottom, rectangle.bottom);
    }
    return bounds;
}

void test()
{
    assert(intersection_area({}) == 0);
    assert(!bounding_rectangle({}));
    assert(intersection_area({{0, 0, 4, 4}}) == 16);
    assert(intersection_area({{0, 0, 4, 4}, {2, 2, 6, 6}, {3, 1, 5, 5}}) == 2);
    assert(intersection_area({{0, 0, 1, 1}, {2, 2, 3, 3}}) == 0);
    assert(intersection_area({{0, 0, 2, 2}, {2, 0, 3, 2}}) == 0);
    assert(intersection_area({{1, 1, 1, 1}}) == 0);
    const auto bounds = bounding_rectangle({{-3, -2, 0, 1}, {2, 3, 4, 5}});
    assert(bounds && bounds->left == -3 && bounds->top == -2 && bounds->right == 4 && bounds->bottom == 5);
    const auto point = bounding_rectangle({{1, 2, 1, 2}});
    assert(point && point->left == 1 && point->right == 1 && point->top == 2 && point->bottom == 2);
    constexpr int minimum = std::numeric_limits<int>::min();
    constexpr int maximum = std::numeric_limits<int>::max();
    const auto extent = static_cast<std::uint64_t>(static_cast<std::int64_t>(maximum) - minimum);
    assert(area({minimum, minimum, maximum, maximum}) == extent * extent);
    bool rejected = false;
    try
    {
        static_cast<void>(intersection_area({{1, 0, 0, 1}}));
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
    const std::vector<Rectangle> rectangles{{0, 0, 4, 4}, {2, 2, 6, 6}};
    const auto bounds = bounding_rectangle(rectangles);
    std::print("Intersection area: {}\nBounds: ({}, {}) - ({}, {})\n", intersection_area(rectangles),
               bounds->left, bounds->top, bounds->right, bounds->bottom);
}
