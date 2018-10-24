#ifndef __TIMER_MANAGEMENT_SERVICE_H__
#define __TIMER_MANAGEMENT_SERVICE_H__

#include "ry_type.h"


#define MAX_ALARM_REPEAT_TYPE_NUM         9     
#define MAX_ALARM_NUM                     5
#define MAX_ALARM_TAG_LEN                  25

#define MAX_ALARM                             5
#define MAX_PERIODIC_TASK_NUM                 5

#define BATTERY_CHECK_PERIOID                 10
#define TOUCH_RESET_PERIOID                   30
#define AUTO_HR_DETECT_PERIOID                60	//every minuet
#define AUTO_DATA_SAVE_PERIOID                600
#define AUTO_SLEEP_HRM_WEARED_DETECT_PERIOID  600
#define DND_MODE_MONITOR_PERIOID              60

#define FLASH_ADDR_ALARM_TABLE                0xFFE00
#define SOFT_WATCH_DOG_THRESH                 10
#define SOFT_WATCH_DOG_SE_WIRED_THRESH        10

#define LOG_MONITOR_STACK                     0



//#pragma pack(4)
typedef struct {
    int weekday;
    int year;
    int month;
    int day;
    int hour;
    int minute;
    int second;
} ry_time_t;


/**
 * @brief Definitaion for alarm type
 */
typedef struct {
    int  id;
    u8_t hour;
    u8_t minute;
    char tag[25];
    bool enable;
    u8_t repeatType[MAX_ALARM_REPEAT_TYPE_NUM];
} tms_alarm_t;

typedef struct {
    u32_t  msgType;
    u32_t  dataAddr;
} monitor_msg_t;

typedef struct {
    uint32_t       dog_alg;
    uint32_t       dog_scedule;    
    uint32_t       dog_wms;
    uint32_t       dog_gui;
    uint32_t       dog_hrm;
    uint32_t       dog_ble_tx;
    uint32_t       dog_ble_rx;
    uint32_t       dog_nfc;
    uint32_t       dog_cms;
    uint32_t       dog_se_wired;
    uint32_t       dog_r_xfer;
    uint32_t       free_heap;
} monitor_info_t;

/**
 * @brief Definitaion for general periodic task handler
 */
typedef void (*periodic_taskHandler_t)(void* usrdata);


typedef enum {
    BATT_LOW_PERCENT_0,
    BATT_LOW_PERCENT_5,
    BATT_LOW_PERCENT_10,
    BATT_LOW_PERCENT_15,
    BATT_LOW_PERCENT_20,  
    BATT_LOW_PERCENT_NORMAL,  
    BATT_LOW_PERCENT_NUM,    
}battery_low_level_t;

typedef struct {
    periodic_taskHandler_t  handler;
    int                     interval;
    void*                   usrdata;
    int                     lastTick;
    u8_t                    enable;
} periodic_task_t;


/*
 * @brief Periodic Task Table
 */
typedef struct {
    u32_t curNum;
    periodic_task_t tasks[MAX_PERIODIC_TASK_NUM];
} periodic_task_tbl_t;



/**
 * @brief Definitaion for alarm table type
 */
typedef struct {
    u32_t curNum;
    tms_alarm_t alarms[MAX_ALARM_NUM];
} tms_alarm_tbl_t;





typedef struct {
    uint8_t off_level;
    uint8_t low_protect;
    uint8_t halt_en;    
} battery_info_t;


/*
 * @brief Time service control block
 */
typedef struct {
    int                 tick;
    ry_time_t           systemTime;
    periodic_task_tbl_t ptt;
    tms_alarm_tbl_t     alarmTbl;
    uint8_t             batt_percent;
    uint8_t             batt_percent_last_log;    
    uint8_t             alg_enable;   
    uint8_t             sleep_hrm_log_count;       
    uint8_t             oled_max_brightness;
    int                 interval_ms;
} tms_ctx_t;
//#pragma pack()

#endif

