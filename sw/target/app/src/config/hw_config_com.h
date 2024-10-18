#ifndef __HW_CONFIG_COM_H__
#define __HW_CONFIG_COM_H__
    #if defined(HW_FPGA_ARCH_ZYNQMP)
        #include "hw_config_com_zynqmp.h"
    #elif defined(HW_FPGA_ARCH_VERSAL)
        #include "hw_config_com_versal.h"
    #else

    #endif
#endif
