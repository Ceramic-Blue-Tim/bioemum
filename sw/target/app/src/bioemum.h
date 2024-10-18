/*
*! @title      Main application for bioemum
*! @file       bioemum.h
*! @author     Romain Beaubois
*! @date       10 Aug 2022
*! @copyright
*! SPDX-FileCopyrightText: © 2022 Romain Beaubois <refbeaubois@yahoo.com>
*! SPDX-License-Identifier: GPL-3.0-or-later
*!
*! @brief
*! 
*! @details
*! > **10 Aug 2022** : file creation (RB)
*! > **17 Oct 2024** : fpga hw arch passed at compilation from makefile (RB)
*/

#ifndef BIOEMUM_H
#define BIOEMUM_H

    /* ############################# Parameters ############################# */
    #define SW_VERSION "0.1.1"

    #if defined(HW_FPGA_ARCH_ZYNQMP)
        #define HW_FPGA_ARCH                "ZynqMP"
        #define BASEADDR_AXI_LITE_CORE0     0x0000'A000'0000 // physical address map
        #define RANGE_AXI_LITE_CORE0        0x0000'0001'0000 // range address map
    #elif defined(HW_FPGA_ARCH_VERSAL)
        #define HW_FPGA_ARCH                "Versal"
        #define BASEADDR_AXI_LITE_CORE0     0x0203'4000'0000 // physical address map
        #define RANGE_AXI_LITE_CORE0        0x0000'0001'0000 // range address map
    #else
        #define HW_FPGA_ARCH                "Undefined"
        #define BASEADDR_AXI_LITE_CORE0     0x0000'0000'0000 // physical address map
        #define RANGE_AXI_LITE_CORE0        0x0000'0001'0000 // range address map
    #endif

#endif