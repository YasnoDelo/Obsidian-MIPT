#include <cassert>
#include <cstdio>
#include <memory>
#include <print>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <vector>

class Noncopyable
{
protected:
    Noncopyable() = default;
    ~Noncopyable() = default;
    Noncopyable(const Noncopyable&) = delete;
    Noncopyable& operator=(const Noncopyable&) = delete;
};

class List : private Noncopyable
{
private:
    struct Node
    {
        int value = 0;
        Node* next = nullptr;
    };

    Node* first_ = nullptr;
    Node* last_ = nullptr;

public:
    ~List()
    {
        while (!empty())
        {
            pop_front();
        }
    }

    bool empty() const noexcept
    {
        return first_ == nullptr;
    }

    void show(std::FILE* output = stdout) const
    {
        for (const Node* node = first_; node != nullptr; node = node->next)
        {
            std::print(output, "{}{}", node == first_ ? "" : " ", node->value);
        }
        std::print(output, "\n");
    }

    void push_front(int value)
    {
        first_ = new Node{value, first_};
        if (last_ == nullptr)
        {
            last_ = first_;
        }
    }

    void push_back(int value)
    {
        Node* node = new Node{value, nullptr};
        if (last_ != nullptr)
        {
            last_->next = node;
        }
        else
        {
            first_ = node;
        }
        last_ = node;
    }

    void pop_front() noexcept
    {
        if (empty())
        {
            return;
        }
        Node* removed = first_;
        first_ = first_->next;
        delete removed;
        if (first_ == nullptr)
        {
            last_ = nullptr;
        }
    }

    void pop_back() noexcept
    {
        if (first_ == last_)
        {
            pop_front();
            return;
        }
        Node* previous = first_;
        while (previous->next != last_)
        {
            previous = previous->next;
        }
        delete last_;
        last_ = previous;
        last_->next = nullptr;
    }

    int get() const
    {
        if (empty())
        {
            throw std::out_of_range("Empty list has no middle element");
        }
        const Node* slow = first_;
        const Node* fast = first_;
        while (fast != nullptr && fast->next != nullptr)
        {
            slow = slow->next;
            fast = fast->next->next;
        }
        return slow->value;
    }
};

std::string capture(const List& list)
{
    const auto close_file = [](std::FILE* file) { std::fclose(file); };
    std::unique_ptr<std::FILE, decltype(close_file)> file(std::tmpfile(), close_file);
    if (!file)
    {
        throw std::runtime_error("Cannot create output capture");
    }
    list.show(file.get());
    std::rewind(file.get());
    std::string result;
    int symbol = 0;
    while ((symbol = std::fgetc(file.get())) != EOF)
    {
        result.push_back(static_cast<char>(symbol));
    }
    if (std::ferror(file.get()))
    {
        throw std::runtime_error("Cannot read output capture");
    }
    return result;
}

void test()
{
    static_assert(std::is_default_constructible_v<List>);
    static_assert(!std::is_copy_constructible_v<List>);
    static_assert(!std::is_copy_assignable_v<List>);
    static_assert(!std::is_move_constructible_v<List>);
    List list;
    assert(list.empty());
    assert(capture(list) == "\n");
    list.pop_front();
    list.pop_back();
    bool rejected = false;
    try
    {
        static_cast<void>(list.get());
    }
    catch (const std::out_of_range&)
    {
        rejected = true;
    }
    assert(rejected);
    list.push_front(2);
    assert(!list.empty() && list.get() == 2);
    list.pop_back();
    assert(list.empty());
    list.push_back(2);
    list.push_front(1);
    assert(list.get() == 2);
    list.push_back(3);
    assert(list.get() == 2);
    assert(capture(list) == "1 2 3\n");
    list.pop_back();
    assert(capture(list) == "1 2\n");
    list.pop_front();
    assert(list.get() == 2);
    list.pop_front();
    assert(list.empty());
    std::vector<int> reference;
    constexpr int iteration_count = 120;
    for (int value = 0; value < iteration_count; ++value)
    {
        if (value % 2 == 0)
        {
            list.push_front(value);
            reference.insert(reference.begin(), value);
        }
        else
        {
            list.push_back(value);
            reference.push_back(value);
        }
        assert(list.get() == reference[reference.size() / 2]);
    }
    while (!reference.empty())
    {
        if (reference.size() % 2 == 0)
        {
            list.pop_back();
            reference.pop_back();
        }
        else
        {
            list.pop_front();
            reference.erase(reference.begin());
        }
        assert(list.empty() == reference.empty());
        if (!reference.empty())
        {
            assert(list.get() == reference[reference.size() / 2]);
        }
    }
    {
        List destruction_case;
        for (int value = 0; value < iteration_count; ++value)
        {
            destruction_case.push_back(value);
        }
    }
}

int main()
{
    test();
    List list;
    for (int value : {1, 2, 3, 4, 5})
    {
        list.push_back(value);
    }
    list.show();
    std::print("Middle: {}\n", list.get());
}
