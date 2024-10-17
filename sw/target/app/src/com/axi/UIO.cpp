//  source code from (https://harmoninstruments.com/posts/uio.html)

#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <cstdlib>
#include <cstdint>
#include <poll.h>
#include <errno.h>
#include <stdexcept>
#include "UIO.h"

UIO::UIO(const char *fn) {
        _fd = open(fn, O_RDWR);
        if (_fd < 0)
               throw std::runtime_error("failed to open UIO device");
}

UIO::~UIO() { close(_fd); }

void UIO::unmask_interrupt() {
        uint32_t unmask = 1;
        ssize_t rv = write(_fd, &unmask, sizeof(unmask));
        if (rv != (ssize_t)sizeof(unmask)) {
                perror("UIO::unmask_interrupt()");
        }
}

void UIO::wait_interrupt(int timeout_ms) {
        // wait for the interrupt
        struct pollfd pfd = {.fd = _fd, .events = POLLIN};
        int rv = poll(&pfd, 1, timeout_ms);
        // clear the interrupt
        if (rv >= 1) {
               uint32_t info;
               read(_fd, &info, sizeof(info));
        } else if (rv == 0) {
               // this indicates a timeout, will be caught by device busy flag
        } else {
               perror("UIO::wait_interrupt()");
        }
}

UIO_mmap::UIO_mmap(const UIO &u, int index, size_t size) : _size(size) {
        _ptr = mmap(NULL, size, PROT_READ | PROT_WRITE, MAP_SHARED,
                u._fd, index * getpagesize());
        if (_ptr == MAP_FAILED) {
                perror("UIO_mmap");
                std::runtime_error("UIO_mmap construction failed");
        }
}

UIO_mmap::~UIO_mmap() { munmap(_ptr, _size); }