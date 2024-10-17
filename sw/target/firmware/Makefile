# Path to board specific firmwares to build.
BOARDS := boards/

# Define specific Makefiles for each architecture
MAKEFILE_VERSAL := Makefile.versal
MAKEFILE_ZYNQMP := Makefile.zynqmp

# Set the default target if ARCH is not specified
ARCH ?= all

default: all

all: build

build:
ifeq ($(ARCH), zynqmp)
	make -C $(BOARDS) -f $(MAKEFILE_ZYNQMP)
else ifeq ($(ARCH), versal)
	make -C $(BOARDS) -f $(MAKEFILE_VERSAL)
else
	@echo "Invalid architecture specified. Use 'zynqmp' or 'versal'."
	exit 1
endif

clean:
ifeq ($(ARCH), zynqmp)
	make -C $(BOARDS) -f $(MAKEFILE_ZYNQMP) clean
else ifeq ($(ARCH), versal)
	make -C $(BOARDS) -f $(MAKEFILE_VERSAL) clean
else
	@echo "Invalid architecture specified. Use 'zynqmp' or 'versal'."
	exit 1
endif

install:
ifeq ($(ARCH), zynqmp)
	make -C $(BOARDS) -f $(MAKEFILE_ZYNQMP) install DESTDIR=$(DESTDIR)
else ifeq ($(ARCH), versal)
	make -C $(BOARDS) -f $(MAKEFILE_VERSAL) install DESTDIR=$(DESTDIR)
else
	@echo "Invalid architecture specified. Use 'zynqmp' or 'versal'."
	exit 1
endif

.PHONY: default all build clean install