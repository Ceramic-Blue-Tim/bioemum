# Path to board specific firmwares to build.
BOARDS := boards/

# Set the default target if ARCH is not specified
ARCH ?= all
MSG_ERR_ARCH := "Invalid architecture specified. Use 'zynqmp' or 'versal'."

default: all

all: build

build:
ifeq ($(ARCH), zynqmp)
	make ARCH=$(ARCH) -C $(BOARDS)
else ifeq ($(ARCH), versal)
	make ARCH=$(ARCH) -C $(BOARDS)
else
	@echo $(MSG_ERR_ARCH)
	exit 1
endif

clean:
ifeq ($(ARCH), zynqmp)
	make ARCH=$(ARCH) -C $(BOARDS) clean
else ifeq ($(ARCH), versal)
	make ARCH=$(ARCH) -C $(BOARDS) clean
else
	@echo $(MSG_ERR_ARCH)
	exit 1
endif

install:
ifeq ($(ARCH), zynqmp)
	make ARCH=$(ARCH) -C $(BOARDS) install DESTDIR=$(DESTDIR)
else ifeq ($(ARCH), versal)
	make ARCH=$(ARCH) -C $(BOARDS) install DESTDIR=$(DESTDIR)
else
	@echo $(MSG_ERR_ARCH)
	exit 1
endif

.PHONY: default all build clean install