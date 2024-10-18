#ifndef __HW_CONFIG_HHPARAM_H__
#define __HW_CONFIG_HHPARAM_H__
    #if defined(HW_FPGA_ARCH_ZYNQMP)
        #include "hw_config_hhparam_zynqmp.h"
    #elif defined(HW_FPGA_ARCH_VERSAL)
        #include "hw_config_hhparam_versal.h"
    #else

    #endif
#endif
