/*********************************************************************
 *        _       _         _
 *  _ __ | |_  _ | |  __ _ | |__   ___
 * | '__|| __|(_)| | / _` || '_ \ / __|
 * | |   | |_  _ | || (_| || |_) |\__ \
 * |_|    \__|(_)|_| \__,_||_.__/ |___/
 *
 * www.rt-labs.com
 * Copyright 2020 rt-labs AB, Sweden.
 *
 * This software is dual-licensed under GPLv3 and a commercial
 * license. See the file LICENSE.md distributed with this software for
 * full license information.
 ********************************************************************/

/*
 * Note: this file originally auto-generated by mib2c
 * using mib2c.iterate.conf
 */

#include <net-snmp/net-snmp-config.h>
#include <net-snmp/net-snmp-includes.h>
#include <net-snmp/agent/net-snmp-agent-includes.h>

#undef LOG_DEBUG
#undef LOG_WARNING
#undef LOG_INFO
#undef LOG_ERROR
#undef LOG_FATAL

#include "lldpConfigManAddrTable.h"

/** Initializes the lldpConfigManAddrTable module */
void init_lldpConfigManAddrTable (pnet_t * pnet)
{
   /* here we initialize all the tables we're planning on supporting */
   initialize_table_lldpConfigManAddrTable (pnet);
}

/** Initialize the lldpConfigManAddrTable table by defining its contents and how
 * it's structured */
void initialize_table_lldpConfigManAddrTable (pnet_t * pnet)
{
   const oid lldpConfigManAddrTable_oid[] = {1, 0, 8802, 1, 1, 2, 1, 1, 7};
   const size_t lldpConfigManAddrTable_oid_len =
      OID_LENGTH (lldpConfigManAddrTable_oid);
   netsnmp_handler_registration * reg;
   netsnmp_iterator_info * iinfo;
   netsnmp_table_registration_info * table_info;

   reg = netsnmp_create_handler_registration (
      "lldpConfigManAddrTable",
      lldpConfigManAddrTable_handler,
      lldpConfigManAddrTable_oid,
      lldpConfigManAddrTable_oid_len,
      HANDLER_CAN_RONLY);

   reg->my_reg_void = pnet;

   table_info = SNMP_MALLOC_TYPEDEF (netsnmp_table_registration_info);
   netsnmp_table_helper_add_indexes (
      table_info,
      ASN_INTEGER,   /* index: lldpLocManAddrSubtype */
      ASN_OCTET_STR, /* index: lldpLocManAddr */
      0);
   table_info->min_column = COLUMN_LLDPCONFIGMANADDRPORTSTXENABLE;
   table_info->max_column = COLUMN_LLDPCONFIGMANADDRPORTSTXENABLE;

   iinfo = SNMP_MALLOC_TYPEDEF (netsnmp_iterator_info);
   iinfo->get_first_data_point = lldpConfigManAddrTable_get_first_data_point;
   iinfo->get_next_data_point = lldpConfigManAddrTable_get_next_data_point;
   iinfo->table_reginfo = table_info;

   iinfo->myvoid = pnet;

   netsnmp_register_table_iterator (reg, iinfo);
}

netsnmp_variable_list * lldpConfigManAddrTable_get_first_data_point (
   void ** my_loop_context,
   void ** my_data_context,
   netsnmp_variable_list * put_index_data,
   netsnmp_iterator_info * mydata)
{
   netsnmp_variable_list * idx = put_index_data;
   pnet_t * pnet = (pnet_t *)mydata->myvoid;
   pf_snmp_management_address_t address;

   pf_snmp_get_management_address (pnet, &address);

   snmp_set_var_typed_integer (idx, ASN_INTEGER, address.subtype);
   idx = idx->next_variable;

   snmp_set_var_value (idx, &address.value[1], address.value[0]);

   /* Set my_data_context to a value that is not NULL */
   *my_data_context = (void *)(uintptr_t) true;

   return put_index_data;
}

netsnmp_variable_list * lldpConfigManAddrTable_get_next_data_point (
   void ** my_loop_context,
   void ** my_data_context,
   netsnmp_variable_list * put_index_data,
   netsnmp_iterator_info * mydata)
{
   return NULL;
}

/** handles requests for the lldpConfigManAddrTable table */
int lldpConfigManAddrTable_handler (
   netsnmp_mib_handler * handler,
   netsnmp_handler_registration * reginfo,
   netsnmp_agent_request_info * reqinfo,
   netsnmp_request_info * requests)
{

   netsnmp_request_info * request;
   netsnmp_table_request_info * table_info;
   pnet_t * pnet = reginfo->my_reg_void;
   void * my_data_context;
   pf_lldp_port_list_t port_list;

   switch (reqinfo->mode)
   {
      /*
       * Read-support (also covers GetNext requests)
       */
   case MODE_GET:
      for (request = requests; request; request = request->next)
      {
         my_data_context = netsnmp_extract_iterator_context (request);
         table_info = netsnmp_extract_table_info (request);

         LOG_DEBUG (
            PF_SNMP_LOG,
            "lldpConfigManAddrTable(%d): GET. Column number: %u\n",
            __LINE__,
            table_info->colnum);

         switch (table_info->colnum)
         {
         case COLUMN_LLDPCONFIGMANADDRPORTSTXENABLE:
            if (my_data_context == NULL)
            {
               netsnmp_set_request_error (reqinfo, request, SNMP_NOSUCHINSTANCE);
               continue;
            }

            pf_snmp_get_port_list (pnet, &port_list);
            snmp_set_var_typed_value (
               request->requestvb,
               ASN_OCTET_STR,
               port_list.ports,
               sizeof (port_list.ports));
            break;
         default:
            netsnmp_set_request_error (reqinfo, request, SNMP_NOSUCHOBJECT);
            break;
         }
      }
      break;
   default:
      LOG_DEBUG (
         PF_SNMP_LOG,
         "lldpConfigManAddrTable(%d): Unknown mode: %u\n",
         __LINE__,
         reqinfo->mode);
      break;
   }
   return SNMP_ERR_NOERROR;
}
