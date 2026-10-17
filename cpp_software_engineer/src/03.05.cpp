#include <cassert>
#include <print>

class Entity_v1
{
public:
    virtual ~Entity_v1() = default;

    virtual int test() const
    {
        constexpr int base_result = 1;
        return base_result;
    }
};

class Entity_v2
{
public:
    virtual ~Entity_v2() = default;

    virtual int test() const
    {
        constexpr int base_result = 2;
        return base_result;
    }
};

class Adapter_v1 : public Entity_v1
{
public:
    int test() const final
    {
        return test_v1();
    }

    virtual int test_v1() const = 0;
};

class Adapter_v2 : public Entity_v2
{
public:
    int test() const final
    {
        return test_v2();
    }

    virtual int test_v2() const = 0;
};

class Client : public Adapter_v1, public Adapter_v2
{
public:
    int test_v1() const override
    {
        constexpr int first_result = 10;
        return first_result;
    }

    int test_v2() const override
    {
        constexpr int second_result = 20;
        return second_result;
    }
};

void test()
{
    const Entity_v1 original_first;
    const Entity_v2 original_second;
    assert(original_first.test() == 1);
    assert(original_second.test() == 2);
    const Client client;
    const Entity_v1& first = client;
    const Entity_v2& second = client;
    assert(first.test() == 10);
    assert(second.test() == 20);
    assert(client.test_v1() == first.test());
    assert(client.test_v2() == second.test());
}

int main()
{
    test();
    const Client client;
    const Entity_v1& first = client;
    const Entity_v2& second = client;
    std::print("Entity_v1::test -> {}\nEntity_v2::test -> {}\n", first.test(), second.test());
}
