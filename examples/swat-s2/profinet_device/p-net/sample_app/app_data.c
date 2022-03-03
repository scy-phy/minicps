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

#include "app_data.h"
#include "app_utils.h"
#include "app_gsdml.h"
#include "app_log.h"
#include "sampleapp_common.h"
#include "osal.h"
#include "pnal.h"
#include <pnet_api.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sqlite3.h>

#define APP_DATA_DEFAULT_OUTPUT_DATA 0

/* Parameters data
 * Todo: Data is always in pnio data format. Add conversion to uint32_t.
 */
// uint32_t app_param_1 = 0;
// uint32_t app_param_2 = 0;

/* Process data */
uint8_t inputdata_1[APP_GSDML_INPUT_DATA_SIZE_1] = {0};
uint8_t outputdata_1[APP_GSDML_OUTPUT_DATA_SIZE_1] = {0};
/* Process data */
uint8_t inputdata_4[APP_GSDML_INPUT_DATA_SIZE_4] = {0};
uint8_t outputdata_4[APP_GSDML_OUTPUT_DATA_SIZE_4] = {0};
/* Process data */
uint8_t inputdata_8[APP_GSDML_INPUT_DATA_SIZE_8] = {0};
uint8_t outputdata_8[APP_GSDML_OUTPUT_DATA_SIZE_8] = {0};

uint8_t counter = 0;

// /**
//  * Set LED state.
//  *
//  * Compares new state with previous state, to minimize system calls.
//  *
//  * Uses the hardware specific app_set_led() function.
//  *
//  * @param led_state        In:    New LED state
//  */
// static void app_handle_data_led_state (bool led_state)
// {
//    // static bool previous_led_state = false;

//    // if (led_state != previous_led_state)
//    // {
//    //    app_set_led (APP_DATA_LED_ID, led_state);
//    // }
//    // previous_led_state = led_state;
// }

uint8_t * app_data_get_input_data (
   uint32_t submodule_id,
   uint16_t * size,
   uint8_t * iops,
   uint8_t counter)
{
   // printf ("------ app_data_get_input_data ------\n");
   // printf ("submodule_id %u", submodule_id);
   // if (size == NULL || iops == NULL)
   // {
   //    return NULL;
   // }

   if (submodule_id == APP_GSDML_MOD_ID_1_IN_OUT)
   {
      *size = APP_GSDML_INPUT_DATA_SIZE_1;
      *iops = PNET_IOXS_GOOD;

      return inputdata_1;
   }
   else if (submodule_id == APP_GSDML_MOD_ID_2_IN_OUT)
   {
      *size = APP_GSDML_INPUT_DATA_SIZE_4;
      *iops = PNET_IOXS_GOOD;
      // printf ("Input n-data received!\n");
      // printf ("Count = %u!\n", counter);

      inputdata_4[0] = counter;

      return inputdata_4;
   }
   else if (submodule_id == APP_GSDML_MOD_ID_3_IN_OUT)
   {
      *size = APP_GSDML_INPUT_DATA_SIZE_8;
      *iops = PNET_IOXS_GOOD;
      // printf ("Input n-data received!\n");
      // printf ("Count = %u!\n", counter);

      inputdata_8[0] = counter;

      return inputdata_8;
   }
   /* Automated RT Tester scenario 2 - unsupported (sub)module */
   *iops = PNET_IOXS_BAD;
   return NULL;
   /* Prepare input data
    * Lowest 7 bits: Counter    Most significant bit: Button
    */
   // inputdata[0] = counter;
   // if (button_pressed)
   // {
   //    inputdata[0] |= 0x80;
   // }
   // else
   // {
   //    inputdata[0] &= 0x7F;
   // }
   // return NULL;
}

int app_data_set_output_data (
   uint32_t submodule_id,
   uint8_t * data,
   uint16_t size,
   uint8_t counter)
{
   // printf ("------ app_data_set_output_data ------\n");
   // printf ("submodule_id %u\n", submodule_id);
   // printf ("size %u\n", size);
   // printf ("data %u\n", *data);
   if (data != NULL)
   {

      if (
         submodule_id == APP_GSDML_MOD_ID_1_IN_OUT &&
         size == APP_GSDML_OUTPUT_DATA_SIZE_1)
      {
         memcpy (outputdata_1, data, size);

         // printf ("outputdata_1[0] = %u\n\n", outputdata_1[0]);
         return 0;
      }
      else if (
         submodule_id == APP_GSDML_MOD_ID_2_IN_OUT &&
         size == APP_GSDML_OUTPUT_DATA_SIZE_4)
      {
         memcpy (outputdata_4, data, size);
         // led_state = (outputdata_n[0] & 0x80) > 0;
         // printf ("outputdata_4[0] = %u\n\n", outputdata_4[0]);
         // printf ("outputdata_4[3] = %u\n\n", outputdata_4[3]);

         // app_handle_data_led_state (false);
         return 0;
      }
      else if (
         submodule_id == APP_GSDML_MOD_ID_3_IN_OUT &&
         size == APP_GSDML_OUTPUT_DATA_SIZE_8)
      {
         memcpy (outputdata_8, data, size);
         // led_state = (outputdata_n[0] & 0x80) > 0;
         // printf ("new outputdata_8[0] = %u\n\n", outputdata_8[0]);
         printf ("OUTPUTDATA: %u %u %u %u %u %u %u %u \n", 
            outputdata_8[0], outputdata_8[1], outputdata_8[2], outputdata_8[3], 
            outputdata_8[4], outputdata_8[5], outputdata_8[6], outputdata_8[7]);

         // app_handle_data_led_state (false);
         return 0;
      }
   }
   return -1;
}

int app_data_set_default_outputs (void)
{
   outputdata_1[0] = APP_DATA_DEFAULT_OUTPUT_DATA;
   outputdata_4[0] = APP_DATA_DEFAULT_OUTPUT_DATA;
   outputdata_8[0] = APP_DATA_DEFAULT_OUTPUT_DATA;

   // app_handle_data_led_state (false);
   return 0;
}

int app_data_update_database (
   char * database_path,
   char * database_name,
   uint8_t pid)
{
   printf ("DATABASE SHIT: %s%s%u\n", database_path, database_name, pid);

   union
   {
      char array[8];
      double num;
   } array_double;

   union
   {
      char array[4];
      float num;
   } array_float;

   union
   {
      char array[4];
      int num;
   } array_int;

   for (int i = 0; i < 8; i++)
   {
      array_double.array[i] = (char)outputdata_8[i];
   }

   printf("%f", array_double.num); 

   for (int i = 0; i < 4; i++)
   {
      array_float.array[i] = (char)outputdata_4[i];
   }
   array_int.num = outputdata_1[0];

   sqlite3 * db;
   if (sqlite3_open (database_path, &db))
   {
      printf ("Could not open the.db\n");
      exit (-1);
   }

   double values[3] = {
      (double)array_int.num,
      (double)array_float.num,
      array_double.num};

   char * output_names[] = {"DI8", "DI32", "DI64"};
   char * input_names[] = {"DO8", "DO32", "DO64"};


   app_update_sql_values (db, pid, output_names, 3, values);

   app_get_sql_values (db, pid, input_names, 3);

   sqlite3_close (db);

   return 0;
}

void app_get_sql_values (
   sqlite3 * db,
   int pid,
   char * name[],
   int amount_names)
{
   sqlite3_stmt * stmt;

   double results[3] = {0, 0, 0}; 

   for (int j = 0; j < amount_names; j++)
   {
      printf ("Execute SQL Statement with name: %s\n", name[j]);
      if (sqlite3_prepare_v2 (
             db,
             "select * from profinet_device where name = ? and pid = ?",
             -1,
             &stmt,
             NULL))
      {
         printf ("Error executing sql statement\n");
         sqlite3_close (db);
      }
      sqlite3_bind_text (stmt, 1, name[j], -1, NULL);
      sqlite3_bind_int (stmt, 2, pid);

      while (sqlite3_step (stmt) != SQLITE_DONE)
      {
         results[j] = sqlite3_column_double (stmt, 2);
      }
      sqlite3_finalize (stmt);
   }

   union
   {
      char array[8];
      double num;
   } arrayDouble;

   union
   {
      char array[4];
      float num;
   } arrayFloat;

   arrayDouble.num = results[2]; 
   arrayFloat.num = results[1];


   for (int i = 0; i < 8; i++)
   {
      inputdata_8[i] = (uint8_t)arrayDouble.array[i];
   }

   for (int i = 0; i < 4; i++)
   {
      inputdata_4[i] = (uint8_t)arrayFloat.array[i];
   }
   inputdata_1[0] = results[0];

   return;
}

void app_update_sql_values (
   sqlite3 * db,
   int pid,
   char * name[],
   int amount_names,
   double values[])
{
   sqlite3_stmt * stmt;

   for (int j = 0; j < amount_names; j++)
   {
      printf ("Execute SQL Statement with name: %s\n", name[j]);
      if (sqlite3_prepare_v2 (
             db,
             "update profinet_device set value = ? where name = ? and pid = ?",
             -1,
             &stmt,
             NULL))
      {
         printf ("Error executing sql statement\n");
         sqlite3_close (db);
      }
      sqlite3_bind_text (stmt, 2, name[j], -1, NULL);
      sqlite3_bind_double (stmt, 1, values[j]);
      sqlite3_bind_int (stmt, 3, pid);

      if (sqlite3_step (stmt) != SQLITE_DONE)
      {
         printf ("Error executing sql statement\n");
      }
      sqlite3_finalize (stmt);
   }

   return;
}

// int app_data_write_parameter (
//    uint32_t submodule_id,
//    uint32_t index,
//    const uint8_t * data,
//    uint16_t length)
// {
//    const app_gsdml_param_t * par_cfg;

//    par_cfg = app_gsdml_get_parameter_cfg (submodule_id, index);
//    if (par_cfg == NULL)
//    {
//       APP_LOG_WARNING (
//          "PLC write request unsupported submodule/parameter. "
//          "Submodule id: %u Index: %u\n",
//          (unsigned)submodule_id,
//          (unsigned)index);
//       return -1;
//    }

//    if (length != par_cfg->length)
//    {
//       APP_LOG_WARNING (
//          "PLC write request unsupported length. "
//          "Index: %u Length: %u Expected length: %u\n",
//          (unsigned)index,
//          (unsigned)length,
//          par_cfg->length);
//       return -1;
//    }

//    if (index == APP_GSDM_PARAMETER_1_IDX)
//    {
//       memcpy (&app_param_1, data, sizeof (length));
//    }
//    else if (index == APP_GSDM_PARAMETER_2_IDX)
//    {
//       memcpy (&app_param_2, data, sizeof (length));
//    }
//    APP_LOG_DEBUG ("  Writing %s\n", par_cfg->name);
//    app_log_print_bytes (APP_LOG_LEVEL_DEBUG, data, length);

//    return 0;
// }

// int app_data_read_parameter (
//    uint32_t submodule_id,
//    uint32_t index,
//    uint8_t ** data,
//    uint16_t * length)
// {
//    const app_gsdml_param_t * par_cfg;

//    par_cfg = app_gsdml_get_parameter_cfg (submodule_id, index);
//    if (par_cfg == NULL)
//    {
//       APP_LOG_WARNING (
//          "PLC read request unsupported submodule/parameter. "
//          "Submodule id: %u Index: %u\n",
//          (unsigned)submodule_id,
//          (unsigned)index);
//       return -1;
//    }

//    if (*length < par_cfg->length)
//    {
//       APP_LOG_WARNING (
//          "PLC read request unsupported length. "
//          "Index: %u Length: %u Expected length: %u\n",
//          (unsigned)index,
//          (unsigned)*length,
//          par_cfg->length);
//       return -1;
//    }

//    APP_LOG_DEBUG ("  Reading %s\n", par_cfg->name);
//    if (index == APP_GSDM_PARAMETER_1_IDX)
//    {
//       *data = (uint8_t *)&app_param_1;
//       *length = sizeof (app_param_1);
//    }
//    else if (index == APP_GSDM_PARAMETER_2_IDX)
//    {
//       *data = (uint8_t *)&app_param_2;
//       *length = sizeof (app_param_2);
//    }

//    app_log_print_bytes (APP_LOG_LEVEL_DEBUG, *data, *length);

//    return 0;
// }
