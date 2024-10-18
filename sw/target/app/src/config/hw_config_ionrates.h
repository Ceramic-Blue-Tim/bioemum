#ifndef __HW_CONFIG_IONRATES_H__
#define __HW_CONFIG_IONRATES_H__
    #if defined(HW_FPGA_ARCH_ZYNQMP)
        #include "hw_config_ionrates_zynqmp.h"
    #elif defined(HW_FPGA_ARCH_VERSAL)
        #include "hw_config_ionrates_versal.h"
    #else

    #endif
#endif
