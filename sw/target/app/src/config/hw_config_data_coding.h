#ifndef __HW_CONFIG_DATA_CODING_H__
#define __HW_CONFIG_DATA_CODING_H__
    #if defined(HW_FPGA_ARCH_ZYNQMP)
        #include "hw_config_data_coding_zynqmp.h"
    #elif defined(HW_FPGA_ARCH_VERSAL)
        #include "hw_config_data_coding_versal.h"
    #else

    #endif
#endif
