/*********************************************************************
 *        _       _         _
 *  _ __ | |_  _ | |  __ _ | |__   ___
 * | '__|| __|(_)| | / _` || '_ \ / __|
 * | |   | |_  _ | || (_| || |_) |\__ \
 * |_|    \__|(_)|_| \__,_||_.__/ |___/
 *
 * www.rt-labs.com
 * Copyright 2018 rt-labs AB, Sweden.
 *
 * This software is dual-licensed under GPLv3 and a commercial
 * license. See the file LICENSE.md distributed with this software for
 * full license information.
 ********************************************************************/

#ifndef APP_DATA_H
#define APP_DATA_H

/**
 * @file
 * @brief Sample application data interface
 *
 * Functions for:
 * - Getting input data (Button 1 and counter value)
 * - Setting ouput data (LED 1)
 * - Setting default output state. This should be
 *   part of all device implementations for setting
 *   defined state when device is not connected to PLC
 * - Reading and writing parameters
 *
 * Todo:
 * Currently sample application uses a single byte
 * for both input and output data. Add float and other
 * types.
 * Currently sample application never convert parameters
 * to native uint32_t value. Fix this.
 */

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include <stdbool.h>
#include <sqlite3.h>

/**
 * Get PNIO input data using module id.
 * The main sample application keep track
 * of button and counter state so these are
 * parameters to this function.
 * @param submodule_id  In:  Submodule id
 * @param button_state  In:  State of button 1
 * @param counter       In:  Sample app counter value
 * @param size          Out: Size of pnio data
 * @param iops          Out: Provider status. If for example
 *                           a sensor is failing or a short
 *                           circuit detected on digital
 *                           input this shall be set to BAD.
 * @return Reference to PNIO data, NULL on error
 */
uint8_t * app_data_get_input_data (
   uint32_t submodule_id,
   uint16_t * size,
   uint8_t * iops, 
   uint8_t counter);

/**
 * Set PNIO output data using module id.
 * @param submodule_id  In:  Submodule id
 * @param data          In:  Reference to output data
 * @param size          In:  Length of output data
 * @return 0 on success, -1 on error
 */
int app_data_set_output_data (
   uint32_t submodule_id,
   uint8_t * data,
   uint16_t size, 
   uint8_t counter);

/**
 * Set default outputs.
 * For the sample application this means that
 * LED 1 is turned off.
 * @param submodule_id  In:  Submodule id
 * @param data          In:  Reference to output data
 * @param size          In:  Length of output data
 * @return 0 on success, -1 on error
 */
int app_data_set_default_outputs (void);

int app_data_update_database (char* database_path, char* database_name, uint8_t pid);

/**
 * Updates values in SQLite Database
 * @param database_path    In:  Database Path
 * @param database_name    In:  Database Name
 * @param pid              In:  PID of Device Process
 * @return 0 on success, -1 on error
 */

void app_update_sql_values (
   sqlite3 * db,
   int pid,
   char * name[],
   int amount_names,
   double values[]);

void app_get_sql_values (
   sqlite3 * db,
   int pid,
   char * name[],
   int amount_names);

/**
 * Write parameter index.
 * @param submodule_id  In:  Submodule id
 * @param index         In:  Parameter index
 * @param data          In:  New parameter value
 * @param size          In:  Length of parameter data
 * @return 0 on success, -1 on error
 */
// int app_data_write_parameter (
//    uint32_t submodule_id,
//    uint32_t index,
//    const uint8_t * data,
//    uint16_t write_length);

/**
 * Read parameter index.
 * @param submodule_id  In:  Submodule id
 * @param index         In:  Parameter index
 * @param data          In:  Refernce to parameter data
 * @param size          In:  Length of parameter data
 * @return 0 on success, -1 on error
 */
// int app_data_read_parameter (
//    uint32_t submodule_id,
//    uint32_t index,
//    uint8_t ** data,
//    uint16_t * length);

#ifdef __cplusplus
}
#endif

#endif /* APP_DATA_H */
