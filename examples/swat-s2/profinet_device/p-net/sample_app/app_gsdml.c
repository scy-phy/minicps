/*********************************************************************
 *        _       _         _
 *  _ __ | |_  _ | |  __ _ | |__   ___
 * | '__|| __|(_)| | / _` || '_ \ / __|
 * | |   | |_  _ | || (_| || |_) |\__ \
 * |_|    \__|(_)|_| \__,_||_.__/ |___/
 *
 * www.rt-labs.com
 * Copyright 2021 rt-labs AB, Sweden.
 *
 * This software is dual-licensed under GPLv3 and a commercial
 * license. See the file LICENSE.md distributed with this software for
 * full license information.
 ********************************************************************/

#include "sampleapp_common.h"
#include "app_utils.h"
#include "app_gsdml.h"
#include "app_log.h"
#include "osal.h"
#include "pnal.h"
#include <pnet_api.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const app_gsdml_module_t dap_1 = {
   .id = PNET_MOD_DAP_IDENT,
   .name = "DAP 1",
   .submodules = {
      PNET_SUBMOD_DAP_IDENT,
      PNET_SUBMOD_DAP_INTERFACE_1_IDENT,
      PNET_SUBMOD_DAP_INTERFACE_1_PORT_1_IDENT}};

static const app_gsdml_module_t module_digital_in_out_1 = {
   .id = APP_GSDML_MOD_ID_1_IN_OUT,
   .name = "8 digital in- and outputs",
   .submodules = {APP_GSDML_MOD_ID_1_IN_OUT, 0}};

static const app_gsdml_module_t module_digital_in_out_4 = {
   .id = APP_GSDML_MOD_ID_2_IN_OUT,
   .name = "32 digital in- and outputs",
   .submodules = {APP_GSDML_MOD_ID_2_IN_OUT, 0}};

static const app_gsdml_module_t module_digital_in_out_8 = {
   .id = APP_GSDML_MOD_ID_3_IN_OUT,
   .name = "64 digital in- and outputs",
   .submodules = {APP_GSDML_MOD_ID_3_IN_OUT, 0}};

static const app_gsdml_submodule_t dap_indentity_1 = {
   .name = "DAP Identity 1",
   .api = APP_GSDML_API,
   .id = PNET_SUBMOD_DAP_IDENT,
   .data_dir = PNET_DIR_NO_IO,
   .insize = 0,
   .outsize = 0,
   .parameters = {0}};

static const app_gsdml_submodule_t dap_interface_1 = {
   .name = "Interface1",
   .api = APP_GSDML_API,
   .id = 0x00000002,
   .data_dir = PNET_DIR_NO_IO,
   .insize = 0,
   .outsize = 0,
   .parameters = {0}};

static const app_gsdml_submodule_t dap_port_1 = {
   .name = "Port1",
   .api = APP_GSDML_API,
   .id = 0x00000003,
   .data_dir = PNET_DIR_NO_IO,
   .insize = 0,
   .outsize = 0,
   .parameters = {0}};

// static const app_gsdml_submodule_t dap_port_2 = {
//    .name = "DAP Port 2",
//    .api = APP_GSDML_API,
//    .id = PNET_SUBMOD_DAP_INTERFACE_1_PORT_2_IDENT,
//    .data_dir = PNET_DIR_NO_IO,
//    .insize = 0,
//    .outsize = 0,
//    .parameters = {0}};

// static const app_gsdml_submodule_t dap_port_3 = {
//    .name = "DAP Port 3",
//    .api = APP_GSDML_API,
//    .id = PNET_SUBMOD_DAP_INTERFACE_1_PORT_3_IDENT,
//    .data_dir = PNET_DIR_NO_IO,
//    .insize = 0,
//    .outsize = 0,
//    .parameters = {0}};

// static const app_gsdml_submodule_t dap_port_4 = {
//    .name = "DAP Port 4",
//    .api = APP_GSDML_API,
//    .id = PNET_SUBMOD_DAP_INTERFACE_1_PORT_4_IDENT,
//    .data_dir = PNET_DIR_NO_IO,
//    .insize = 0,
//    .outsize = 0,
//    .parameters = {0}};

static const app_gsdml_submodule_t submod_digital_inout_1 = {
   .id = APP_GSDML_MOD_ID_1_IN_OUT,
   .name = "Digital Input/Output 1 Byte",
   .api = APP_GSDML_API,
   .data_dir = PNET_DIR_IO,
   .insize = APP_GSDML_INPUT_DATA_SIZE_1,
   .outsize = APP_GSDML_OUTPUT_DATA_SIZE_1,
   .parameters = {0}};

static const app_gsdml_submodule_t submod_digital_inout_4 = {
   .id = APP_GSDML_MOD_ID_2_IN_OUT,
   .name = "Digital Input/Output 4 Byte",
   .api = APP_GSDML_API,
   .data_dir = PNET_DIR_IO,
   .insize = APP_GSDML_INPUT_DATA_SIZE_4,
   .outsize = APP_GSDML_OUTPUT_DATA_SIZE_4,
   .parameters = {0}};

static const app_gsdml_submodule_t submod_digital_inout_8 = {
   .id = APP_GSDML_MOD_ID_3_IN_OUT,
   .name = "Digital Input/Output 8 Byte",
   .api = APP_GSDML_API,
   .data_dir = PNET_DIR_IO,
   .insize = APP_GSDML_INPUT_DATA_SIZE_8,
   .outsize = APP_GSDML_OUTPUT_DATA_SIZE_8,
   .parameters = {0}};

/* List of supported modules */
static const app_gsdml_module_t * app_gsdml_modules[] = {
   &dap_1,
   &module_digital_in_out_1,
   &module_digital_in_out_4,
   &module_digital_in_out_8};

/* List of supported submodules */
static const app_gsdml_submodule_t * app_gsdml_submodules[] = {
   &dap_indentity_1,
   &dap_interface_1,
   &dap_port_1,

   &submod_digital_inout_1,
   &submod_digital_inout_4,
   &submod_digital_inout_8,
};

const app_gsdml_module_t * app_gsdml_get_module_cfg (uint32_t id)
{
   uint32_t i;
   for (i = 0; i < NELEMENTS (app_gsdml_modules); i++)
   {
      if (app_gsdml_modules[i]->id == id)
      {
         return app_gsdml_modules[i];
      }
   }
   return NULL;
}

const app_gsdml_submodule_t * app_gsdml_get_submodule_cfg (uint32_t id)
{
   uint32_t i;
   for (i = 0; i < NELEMENTS (app_gsdml_submodules); i++)
   {
      if (app_gsdml_submodules[i]->id == id)
      {
         printf (
            "app_gsdml_get_submodule_cfg %u %s\n",
            id,
            app_gsdml_submodules[i]->name);
         return app_gsdml_submodules[i];
      }
   }
   return NULL;
}