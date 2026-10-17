#include <cassert>
#include <print>

class Attorney_v1;
class Attorney_v2;
class Tester_v1;
class Tester_v2;

class Entity
{
private:
    int test_v1() const noexcept
    {
        constexpr int first_result = 10;
        return first_result;
    }

    int test_v2() const noexcept
    {
        constexpr int second_result = 20;
        return second_result;
    }

    friend class Attorney_v1;
    friend class Attorney_v2;
};

class Attorney_v1
{
private:
    static int invoke(const Entity& entity) noexcept
    {
        return entity.test_v1();
    }

    friend class Tester_v1;
};

class Attorney_v2
{
private:
    static int invoke(const Entity& entity) noexcept
    {
        return entity.test_v2();
    }

    friend class Tester_v2;
};

class Tester_v1
{
public:
    static void run(const Entity& entity)
    {
        constexpr int expected = 10;
        assert(Attorney_v1::invoke(entity) == expected);
    }
};

class Tester_v2
{
public:
    static void run(const Entity& entity)
    {
        constexpr int expected = 20;
        assert(Attorney_v2::invoke(entity) == expected);
    }
};

int main()
{
    const Entity entity;
    Tester_v1::run(entity);
    Tester_v2::run(entity);
    std::print("Both private methods passed their independent tests.\n");
}
