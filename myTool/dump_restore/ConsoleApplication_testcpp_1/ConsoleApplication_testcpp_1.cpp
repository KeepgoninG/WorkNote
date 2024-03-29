// ConsoleApplication_testcpp_1.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"

#include <stdio.h>

#include <stdint.h>
#include <string.h>
#include "timer_management_service.h"
#include "ry_statistics.h"

#pragma warning(disable : 4996)  

#if defined(_WIN64)
#error NOT SUPPORTED
#endif

#include <regex>
#include <iostream>
#include <list>

/*! \brief      BD address length */
#define BDA_ADDR_LEN                  6
/*! Various parameter lengths */
#define SMP_RAND_LEN                  16
#define SMP_CONFIRM_LEN               16
#define SMP_KEY_LEN                   16
#define SMP_RAND8_LEN                 8
#define SMP_PRIVATE_KEY_LEN           32
#define SMP_PUB_KEY_LEN               32
#define SMP_DHKEY_LEN                 32
#define SMP_DHKEY_CHECK_LEN           16
/*! Number of client characteristic configuration descriptor handles per record */
#ifndef APP_DB_NUM_CCCD
#define APP_DB_NUM_CCCD 10
#endif
/*! Number of ATT client cached handles per record */
#ifndef APP_DB_HDL_LIST_LEN
#define APP_DB_HDL_LIST_LEN 20
#endif

/*! \brief      BD address data type */
typedef uint8_t bdAddr_t[BDA_ADDR_LEN];

/*! IRK data type */
typedef struct
{
	uint8_t                   key[SMP_KEY_LEN];
	bdAddr_t                  bdAddr;
	uint8_t                   addrType;

} dmSecIrk_t;
/*! CSRK data type */
typedef struct
{
	uint8_t                   key[SMP_KEY_LEN];
} dmSecCsrk_t;
/* Boolean data type */
typedef uint8_t bool_t;
/*! LTK data type */
typedef struct
{
	uint8_t                   key[SMP_KEY_LEN];
	uint8_t                   rand[SMP_RAND8_LEN];
	uint16_t                  ediv;
} dmSecLtk_t;
/*! Database record */
typedef struct
{
	/*! Common for all roles */
	bdAddr_t    peerAddr;                     /*! Peer address */
	uint8_t     addrType;                     /*! Peer address type */
	dmSecIrk_t  peerIrk;                      /*! Peer IRK */
	dmSecCsrk_t peerCsrk;                     /*! Peer CSRK */
	uint8_t     keyValidMask;                 /*! Valid keys in this record */
	bool_t      inUse;                        /*! TRUE if record in use */
	bool_t      valid;                        /*! TRUE if record is valid */
	bool_t      peerAddedToRl;                /*! TRUE if peer device's been added to resolving list */
	bool_t      peerRpao;                     /*! TRUE if RPA Only attribute's present on peer device */

											  /*! For slave local device */
	dmSecLtk_t  localLtk;                     /*! Local LTK */
	uint8_t     localLtkSecLevel;             /*! Local LTK security level */
	bool_t      peerAddrRes;                  /*! TRUE if address resolution's supported on peer device (master) */

											  /*! For master local device */
	dmSecLtk_t  peerLtk;                      /*! Peer LTK */
	uint8_t     peerLtkSecLevel;              /*! Peer LTK security level */

											  /*! for ATT server local device */
	uint16_t    cccTbl[APP_DB_NUM_CCCD];      /*! Client characteristic configuration descriptors */
	uint32_t    peerSignCounter;              /*! Peer Sign Counter */

											  /*! for ATT client */
	uint16_t    hdlList[APP_DB_HDL_LIST_LEN]; /*! Cached handle list */
	uint8_t     discStatus;                   /*! Service discovery and configuration status */
} appDbRec_t;



#define ANCS_WHITELIST_MAX_ENRTY 20
#define APPID_RY_MAX_SIZE       32
typedef struct
{
	uint8_t appid[APPID_RY_MAX_SIZE];
	uint8_t isEnabled;
} notificaion_whitelist_resource_t;

typedef struct
{
	uint32_t curNum;
	notificaion_whitelist_resource_t records[ANCS_WHITELIST_MAX_ENRTY];
} notificaion_whitelist_tbl_t;

typedef struct
{
	uint32_t magic_number;
	uint32_t version;       //version 1 store iOS app id directly, version 2 save ry_appid
	uint32_t op_times;
	uint8_t isOthersEnabled;
	uint8_t isAncsOpend;
	uint8_t isAllOpend;
	uint8_t subVersion;     // use for debug to force clear all stored info
	notificaion_whitelist_tbl_t tbl;
} notification_whitelist_stored_t;

#define APP_DB_NUM_RECS 3
#define ATT_DEFAULT_PAYLOAD_LEN       20        /*! Default maximum payload length for most PDUs */

/*! Database type */
typedef struct
{
	appDbRec_t  rec[APP_DB_NUM_RECS];               /*! Device database records */
	char        devName[ATT_DEFAULT_PAYLOAD_LEN];   /*! Device name */
	uint8_t     devNameLen;                         /*! Device name length */
} appDb_t;

#define MAX_SURFACE_ITEM_NUM                        32

#define SURFACE_HEADER_ITEMS_MAX_COUNTER                MAX_SURFACE_ITEM_NUM
#define SURFACE_HEADER_DATASOURCE_KEYWORD_MAX_LEN   16
#define STORED_CHECKSUM_MAX_ITEM_COUNT                  4
#define MAX_SURFACE_NAME_LEN                        32
#define MAX_SURFACE_NUM                             6


#pragma pack(1)
typedef struct
{
	uint8_t key[SURFACE_HEADER_DATASOURCE_KEYWORD_MAX_LEN];
	uint16_t value;
}map_key_to_value_t;

typedef struct
{
	uint32_t curNum;
	map_key_to_value_t records[SURFACE_HEADER_ITEMS_MAX_COUNTER];
} map_key_to_value_table_t;

typedef struct {
	uint64_t id;
	char name[MAX_SURFACE_NAME_LEN];
	uint32_t status;//surface_header_status_t
	uint32_t resource_checksum[STORED_CHECKSUM_MAX_ITEM_COUNT];
} surface_desc_t;

typedef struct {
	uint32_t curNum;
	surface_desc_t surfaces[MAX_SURFACE_NUM];
} surface_tbl_t;
#pragma pack()

typedef struct {
	uint64_t currentId;
	surface_tbl_t surfaceTbl;
} ss_ctx_t;

typedef struct
{
	uint32_t magic;
	uint16_t version;
	uint16_t sub_version;
	uint32_t op_times;
	ss_ctx_t ctx;
}surface_store_t;

void decode_dump_data(char const* p_str, void* p_struct, uint32_t size)
{
	uint8_t* p_buffer = (uint8_t*)p_struct;
//	uint32_t len = strlen(p_str);
	uint32_t byte_count = strlen(p_str)/2;

	if (byte_count != size)
	{
		printf("!!!error sized, byte_to_dump:%d, size_of_struct:%d\r\n", byte_count, size);
		return;
	}

	for (uint32_t i = 0; i < byte_count; i++)
	{
		int value = 0;
		sscanf(&p_str[i * 2],"%02X", &value);
		p_buffer[i] = value;
		// printf("i:%d, p_buffer:%x, value:%x\r\n", i, p_buffer[i], value);
	}
}

typedef struct
{
	char* p_tag_sting;
	uint8_t* p_raw_bytes;
	uint32_t byte_size;
}dump_raw_t;

typedef struct
{
	dump_raw_t* p_data;
	uint32_t data_counter;
}dump_raw_data_t;

char* filter_remove_time(char const* str_in)
{
	std::string text = str_in;
	std::regex regex_iOS_timeprint("\\s{1,}\\n\\d{4}/\\d{2}/\\d{2}.*\\d{3}\\s{1,}");

	std::string result = std::regex_replace(text, regex_iOS_timeprint, "");
	//std::cout << result << std::endl;
	char* p_result = (char*)malloc(result.size() + 1);
	strcpy(p_result, result.c_str());
	return p_result;
}

void dump_restore_to_structs(char const* p_data, dump_raw_data_t* p_raw)
{
	std::regex regex_lines("([^\\r\\n].+)");
	std::regex regex_stamp_raw("(\\w.+):([\\w\\d\\s].+)");
	std::regex regex_byte_space_format(" ");
	std::string text = p_data;
	std::list<dump_raw_t> list_raws = {};


	std::smatch line_match;
	while (std::regex_search(text, line_match, regex_lines))
	{
		std::string line = line_match[0];
		text = line_match.suffix();
//		std::cout << "find from str: \r\n" << line << std::endl;
		std::smatch dump_match;
		if (std::regex_search(line, dump_match, regex_stamp_raw))
		{
			std::string key = dump_match[1];
			std::string payload_with_space = dump_match[2];
			std::string payload = std::regex_replace(payload_with_space, regex_byte_space_format, "");
			int bytes_size = payload.size() / 2;

			char* p_tag_sting = (char*)malloc(key.size() + 1);
			strcpy(p_tag_sting, key.c_str());

			uint8_t* p_bytes = (uint8_t*)malloc(bytes_size);
			decode_dump_data(payload.c_str(), p_bytes, bytes_size);

			dump_raw_t raw;
			raw.byte_size = bytes_size;
			raw.p_tag_sting = p_tag_sting;
			raw.p_raw_bytes = p_bytes;


			list_raws.insert(list_raws.end(), raw);
		}
	}

	p_raw->data_counter = list_raws.size();
	p_raw->p_data = (dump_raw_t*)malloc(sizeof(dump_raw_t)*p_raw->data_counter);
	std::copy(list_raws.begin(), list_raws.end(), p_raw->p_data);

	return;
}

uint8_t* get_buffer_with_tag(char const* p_tag, dump_raw_data_t* p_data)
{
	for (uint32_t i = 0; i < p_data->data_counter; i++)
	{
		if (strcmp(p_tag, p_data->p_data[i].p_tag_sting) == 0)
		{
			return &p_data->p_data[i].p_raw_bytes[0];
		}
	}
	return NULL;
}


int main()
{
	//printf("sizeof appDb_t is %d\r\n", sizeof(appDb_t));
	//printf("sizeof notification_whitelist_stored_t is %d\r\n", sizeof(notification_whitelist_stored_t));
	//printf("sizeof surface_store_t is %d\r\n", sizeof(surface_store_t));
	//sizeof appDb_t is 552
	//sizeof notification_whitelist_stored_t is 680
	//sizeof surface_store_t is 392


	const uint32_t max_size = 1024 * 1024;

	char * p_dump_all = (char*)malloc(max_size);
	char * p_raw = NULL;
	dump_raw_data_t raw_data;
	memset(p_dump_all, 0, max_size);

	FILE* pf;
	pf = fopen("dump.txt", "r");
	uint32_t length = fread(p_dump_all, max_size, 1, pf);

	p_raw = filter_remove_time(p_dump_all);
	free(p_dump_all);
	dump_restore_to_structs(p_raw, &raw_data);
	
	surface_store_t surface = *(surface_store_t*)get_buffer_with_tag("Surface", &raw_data);
	notification_whitelist_stored_t ancs = *(notification_whitelist_stored_t*)get_buffer_with_tag("AncsList", &raw_data);
	appDb_t bledb = *(appDb_t*)get_buffer_with_tag("BleDB", &raw_data);
	tms_ctx_t tms_ctx_v = *(tms_ctx_t*)get_buffer_with_tag("tms_ctx_v", &raw_data);
	ry_DevStatisticsResult_t dev_statistics_v = *(ry_DevStatisticsResult_t*)get_buffer_with_tag("dev_statistics", &raw_data);

	getchar();

    return 0;
}

 