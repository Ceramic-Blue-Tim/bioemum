//  source code from (https://harmoninstruments.com/posts/uio.html)

#ifndef __UIO_H__
#define __UIO_H__

#include <cstdint>
#include <cstddef>

class UIO {
    private:
        int _fd;

    public:
        explicit UIO(const char *fn);
        ~UIO();
        void unmask_interrupt();
        void wait_interrupt(int timeout_ms);
        friend class UIO_mmap;
};

class UIO_mmap {
private:
    size_t _size;
    void *_ptr;

public:
    UIO_mmap(const UIO &u, int index, size_t size);
    ~UIO_mmap();
    size_t size() const { return _size; }
    void *get_ptr() const { return _ptr; }
};
#endif