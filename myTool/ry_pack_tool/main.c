#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <string.h>
#include <time.h>
#include"stdint.h"


#include "cJSON.h"

#define RY_DEVICE_INFO_ADDR         0x7000

#define RY_DEVICE_FW_VER_ADDR       0x9C00
#define RY_HARDWARE_VER_ARRD		0x9C70

#define DEV_INFO_SAFE_HEX_MD5_LEN       16


#define LIB_VERSION					"0.0.7"
#define CONFIG_HEX_HEAD_MASK_SIZE	4
#define CONFIG_HEX_VER_MASK_SIZE	4
#define CONFIG_HEX_TYPE_MASK_SIZE	4
#define CONFIG_HEX_LEN_MASK_SIZE	4
#define START_ADDR					0x1000

#define CONFIG_HEX_HEAD_LEN			(CONFIG_HEX_HEAD_MASK_SIZE + CONFIG_HEX_VER_MASK_SIZE + CONFIG_HEX_TYPE_MASK_SIZE + CONFIG_HEX_LEN_MASK_SIZE)

 /* options descriptor */
static struct option longopts[] = {
	{"file", required_argument, NULL, 'f'},
	{"mac", required_argument, NULL, 'm'},
	{"string", required_argument, NULL, 's'},
	{"debug",required_argument,NULL,'d'},
  //{"bpp", optional_argument, NULL, 'b'},
	{NULL, 0, NULL, 0}
};

char * input_file = NULL;//"test3";
char * mac = NULL;
char * j_str = NULL;
int debug_flag = 0;
FILE * output_bin = NULL;

#define OUTPUT_BIN_FLIE		"ryeex_file"

#define DATA_SECTION		128

#define OUTPUT_FILE_SIZE		(12*1024)


int inputJsonString(char * jsonString);

void usage(void)
{

	printf("error: arg failed \n");
}


int * stringToInt(char * str, int * size,char * split)
{
	char * ch = str;

	//char * split = " ";

	char * head = "0x";

	int * data = NULL;

	int index = 0;

	int temp = 0;

	unsigned int str_length = strlen(str);

	data = (int *)malloc(str_length*10);

	if(data == NULL) {
		goto exit;
	}

	ch = strtok(str, split);

	while( ch != NULL ){

		char * temp_str = (char *)malloc(strlen(ch) + 10);

		if(temp_str == NULL){
			printf("malloc failed---%d\n",__LINE__);
			return NULL;
		}

		memset(temp_str, 0 ,strlen(ch));

		strcat(temp_str, head);

		strcat(temp_str, ch);

		printf("%s\n", temp_str);

		data[temp++] = strtol(temp_str, NULL, 16);

		ch = strtok(NULL, split);

		free(temp_str);
	}

	*size = temp;

exit:
	return data;
}

char * stringToBytes(char * str, int * size )
{
	char * bytes = (char * )malloc( strlen(str) + 10);

	if(bytes == NULL){
		printf("malloc failed---%d\n",__LINE__);
		return NULL;
	}

	char temp[4] = {0};
	char * ch = str;
	int count = 0;
	int index = 0;
	//printf("%s:%d\n",__FUNCTION__, __LINE__);
	while( *ch != '\0'){

		temp[count++] = *ch;
		if(count == 2) {

			count = 0;
			//printf("%s:%d\n",__FUNCTION__, __LINE__);
			bytes[index++] = strtol(temp, NULL, 16);
			//printf("%s:%d\n",temp, index);
		}

		ch++;
	}
	*size = index;
	//printf("%s:%d\n",__FUNCTION__, __LINE__);




	return bytes;
}

void test_py(void)
{
	
	printf("----%s----\n",__FUNCTION__);
	
}

int resolve_config_hex(char * data, char  *desk_ptr, char * xiaomi_ptr)
{
	int ryeex_len = 0, xiaomi_len = 0;
	int *data_len_ptr = NULL;

	if(data[CONFIG_HEX_HEAD_MASK_SIZE + CONFIG_HEX_VER_MASK_SIZE] == 1){
		data_len_ptr = (int *)( &data[CONFIG_HEX_HEAD_MASK_SIZE + CONFIG_HEX_VER_MASK_SIZE + CONFIG_HEX_TYPE_MASK_SIZE] );
		ryeex_len = *data_len_ptr;
		memcpy(desk_ptr, data, (CONFIG_HEX_HEAD_LEN + (ryeex_len)  ) );
	}else if( data[CONFIG_HEX_HEAD_MASK_SIZE + CONFIG_HEX_VER_MASK_SIZE] == 2 ){
		printf("what happen ---%d\n", __LINE__);
	}else{
		printf("what happen ---%d\n", __LINE__);
	}

	if(data[(CONFIG_HEX_HEAD_LEN + (ryeex_len)  )] == 2){
		data_len_ptr = (int *)(&data[(CONFIG_HEX_HEAD_LEN + (ryeex_len) + CONFIG_HEX_TYPE_MASK_SIZE  )]);
		xiaomi_len = *data_len_ptr + CONFIG_HEX_HEAD_MASK_SIZE + CONFIG_HEX_LEN_MASK_SIZE + DEV_INFO_SAFE_HEX_MD5_LEN;
		
		memcpy(xiaomi_ptr, &data[(CONFIG_HEX_HEAD_LEN + (ryeex_len))], xiaomi_len);
	}else{
		printf("what happen ---%d\n", __LINE__);
	}
	return ryeex_len;
}

int inputJsonFile(char * jsonFileName)
{
    int ch = 0;

	input_file = jsonFileName;
	
	if ((input_file != NULL ) &&(j_str != NULL )) {
		//����ͬʱ���������뷽ʽ
		printf("error: input too more \n");
		return (1);
	}

	if ((input_file == NULL) && (j_str ==NULL)) {
		//����û����������
		printf("error: input too less \n");
		return (2);
	}


	if (input_file != NULL) {

		printf("input file : %s\n",input_file);

		FILE * fp = fopen(input_file,"r");

		if(fp == NULL) {
			printf("file open failed\n");

			return (5);
		}

		long j_file_size = 0;

		fseek(fp, 0 ,SEEK_END);
		j_file_size = ftell(fp);

		printf("file size is %d\n",j_file_size);

		j_str = (char *) malloc(j_file_size+10);

		fseek(fp, 0 ,SEEK_SET);

		fread(j_str, 1, j_file_size, fp);


	}

	inputJsonString(j_str);

	free(j_str);
	j_str = NULL;

    return 0;
}

int inputJsonString(char * jsonString)
{
    int ch = 0;
	printf("SO version %s\n", LIB_VERSION);

	j_str = jsonString;



	if (j_str == NULL) {
		printf("error: date is NULL \n");
		return (3);
	}

	cJSON * root = cJSON_Parse(j_str);

	if(debug_flag) {

		//printf("%s",j_str);

		char *out;
		out=cJSON_Print(root);
		printf("out = %s\n",out);

	}




	unsigned char output_buf[OUTPUT_FILE_SIZE] = {0};
	srand(time(NULL));

	int j = 0;
	for(j = 0; j < sizeof(output_buf) ; j++ ) {

		output_buf[j] = /*rand()%*/0xFF;

	}


	output_bin = fopen(OUTPUT_BIN_FLIE, "wb");

	cJSON * mac_obj = cJSON_GetObjectItem(root,"mac");
	cJSON * sn_obj = cJSON_GetObjectItem(root,"sn");
	cJSON * did_obj = cJSON_GetObjectItem(root,"did");
	cJSON * configHex_obj = cJSON_GetObjectItem(root,"configHex");
	cJSON * version_obj = cJSON_GetObjectItem(root,"version");
	cJSON * hw_v_obj = cJSON_GetObjectItem(root,"hardwareVersion");
	


	unsigned char * temp_ptr = &output_buf[START_ADDR];

	//device ID
	if( did_obj != NULL){
		printf("did : %s \n",did_obj->valuestring);

		strcpy(temp_ptr, did_obj->valuestring);

	}else {
		printf("did is not find\n");
	}

	//sn
	temp_ptr += DATA_SECTION;
	if( sn_obj != NULL){
		printf("sn : %s \n",sn_obj->valuestring);

		strcpy(temp_ptr, sn_obj->valuestring);

	}else {
		printf("sn is not find\n");
	}

	//MAC
	temp_ptr += DATA_SECTION;
	if (mac_obj != NULL ){

		printf("mac : %s \n",mac_obj->valuestring);
		int mac_length = 0;
		int * mac_data = stringToInt(mac_obj->valuestring, &mac_length, ":");

		for (int i = 0; i < mac_length; i++){


			temp_ptr[i] = mac_data[i];
		}

		free(mac_data);

	}else {
		printf("mac is not find\n");
	}



	//config Hex
	int hexLength = 0;
	int config_hex_size = 0;
	temp_ptr += DATA_SECTION;
	if( configHex_obj != NULL){
		//printf("config Hex : %s \n",configHex_obj->valuestring);

		
		char * configBytes = stringToBytes(configHex_obj->valuestring, &hexLength);

		/*for(int i = 0 ; i < hexLength; i++)
		{
			printf("\t%x\t", configBytes[i]);

		}
		printf("\n");
		printf("%s:hl===%d\n",__FUNCTION__, hexLength);*/
		int x = 0;
		int *data_len_ptr = NULL;
		for(x = 0; x < CONFIG_HEX_HEAD_MASK_SIZE ; x++){
			if(configBytes[x] != 0){
				break;
			}
			
		}
		if(x == CONFIG_HEX_HEAD_MASK_SIZE){
			memcpy(temp_ptr, &hexLength, 4);
			temp_ptr += 4;

			/*int ryeex_len = 0, xiaomi_len = 0;

			if(configBytes[CONFIG_HEX_HEAD_MASK_SIZE + CONFIG_HEX_VER_MASK_SIZE] == 1){
				data_len_ptr = (int *)( &configBytes[CONFIG_HEX_HEAD_MASK_SIZE + CONFIG_HEX_VER_MASK_SIZE + CONFIG_HEX_TYPE_MASK_SIZE] );
				ryeex_len = *data_len_ptr;
				memcpy(temp_ptr, configBytes, (CONFIG_HEX_HEAD_LEN + (ryeex_len)  ) );
			}else if( configBytes[CONFIG_HEX_HEAD_MASK_SIZE + CONFIG_HEX_VER_MASK_SIZE] == 2 ){
				printf("what happen ---%d\n", __LINE__);
			}else{
				printf("what happen ---%d\n", __LINE__);
			}

			if(configBytes[(CONFIG_HEX_HEAD_LEN + (ryeex_len)  )] == 2){
				data_len_ptr = (int *)(&configBytes[(CONFIG_HEX_HEAD_LEN + (ryeex_len) + CONFIG_HEX_TYPE_MASK_SIZE  )]);
				xiaomi_len = *data_len_ptr;
				memcpy(&output_buf[0], &configBytes[(CONFIG_HEX_HEAD_LEN + (ryeex_len))], xiaomi_len);
			}else{
				printf("what happen ---%d\n", __LINE__);
			}*/

			config_hex_size = resolve_config_hex(configBytes, temp_ptr, &output_buf[0]);


		}else{
			memcpy(temp_ptr, &hexLength, 4);
			temp_ptr += 4;
			config_hex_size = hexLength;
			memcpy(temp_ptr, configBytes, hexLength);
		}

		
		free(configBytes);

	}else {
		printf("config Hex is not find\n");
	}


	temp_ptr += (config_hex_size);
	
	while( temp_ptr !=  &output_buf[OUTPUT_FILE_SIZE - 1]){
		*temp_ptr = (char)(rand()%0xFF);
		temp_ptr++;
	}
	
	//version 
	if( version_obj != NULL){
		printf("version : %s \n",version_obj->valuestring);

		strcpy(&output_buf[RY_DEVICE_FW_VER_ADDR - RY_DEVICE_INFO_ADDR], version_obj->valuestring);

	}else {
		printf("version is not find\n");
	}
	
	// hardware version 
	if( hw_v_obj != NULL){
		printf("hardware version : %s \n",hw_v_obj->valuestring);

		strcpy(&output_buf[RY_HARDWARE_VER_ARRD - RY_DEVICE_INFO_ADDR], hw_v_obj->valuestring);

	}else {
		printf("hardware version is not find\n");
	}





	//printf("%s:%d\n",__FUNCTION__, __LINE__);
	fwrite(output_buf, 1, OUTPUT_FILE_SIZE, output_bin);
	//printf("%s:%d\n",__FUNCTION__, __LINE__);

	fclose(output_bin);//printf("%s:%d\n",__FUNCTION__, __LINE__);
	//fclose(input_file);printf("%s:%d\n",__FUNCTION__, __LINE__);
	/*unsigned int len,size, * head,k;
	char md5_hash[100];
	head = (unsigned int *)(output_buf);
	size = head[1];
	printf("size = %x\n", size);
	char * safe_hex = (char *)&head[2];
	len = DEV_INFO_SAFE_HEX_MD5_LEN;
	memcpy(md5_hash, &safe_hex[size], DEV_INFO_SAFE_HEX_MD5_LEN);

	for(k = 0; k < DEV_INFO_SAFE_HEX_MD5_LEN; k++){
		printf("\t %x", md5_hash[k]);

	}
	printf("\n");*/
    
	
	/*output_bin = fopen(OUTPUT_BIN_FLIE, "rb");
	
	memset(output_buf,0,OUTPUT_FILE_SIZE);
	fread(output_buf, 1, OUTPUT_FILE_SIZE, output_bin);
	
	fclose(output_bin);
	
	output_bin = fopen(OUTPUT_BIN_FLIE, "wb");
	
	fwrite(output_buf, 1, OUTPUT_FILE_SIZE, output_bin);*/
	
	
	

	//system("pause");
	
    return 0;
}

int main(int argc, char **argv)
{
    int ch = 0;
	printf("version 0.0.1\n");

	/*char test1[] = "98:97:96:95:ff:a9";
	int data_length = 0;
	int * test_data = stringToInt(test1, &data_length, ":");

	for(int i = 0 ; i < data_length; i++)
	{
		printf("\t%x\t", test_data[i]);

	}
	printf("\n");*/


	while((ch = getopt_long(argc, argv, "", longopts, NULL)) != -1) {

		switch (ch) {
			case 'f':
				input_file = optarg;
				break;

			case 'm':
				mac = optarg;
				break;

			case 's':
				j_str = optarg;
				break;

			case 'd':
				debug_flag = atoi(optarg);
				break;

			default:
				usage();
				return (1);
		}
	}
	printf("%s",j_str);
	if ((input_file != NULL ) &&(j_str != NULL )) {
		//����ͬʱ���������뷽ʽ
		printf("error: input too more \n");
		return (1);
	}

	if ((input_file == NULL) && (j_str ==NULL)) {
		//����û����������
		printf("error: input too less \n");
		return (2);
	}


	if (input_file != NULL) {

		printf("input file : %s\n",input_file);

		FILE * fp = fopen(input_file,"r");

		if(fp == NULL) {
			printf("file open failed\n");

			return (5);
		}

		long j_file_size = 0;

		fseek(fp, 0 ,SEEK_END);
		j_file_size = ftell(fp);

		printf("file size is %d\n",j_file_size);

		j_str = (char *) malloc(j_file_size+10);

		fseek(fp, 0 ,SEEK_SET);

		fread(j_str, 1, j_file_size, fp);


	}


	if (j_str == NULL) {
		printf("error: date is NULL \n");
		return (3);
	}

	cJSON * root = cJSON_Parse(j_str);

	if(debug_flag) {

		//printf("%s",j_str);

		char *out;
		out=cJSON_Print(root);
		printf("out = %s\n",out);

	}




	unsigned char output_buf[OUTPUT_FILE_SIZE] = {0};
	srand(time(NULL));

	int j = 0;
	for(j = 0; j < sizeof(output_buf) ; j++ ) {

		output_buf[j] = /*rand()%*/0xFF;

	}


	output_bin = fopen(OUTPUT_BIN_FLIE, "wb");

	cJSON * mac_obj = cJSON_GetObjectItem(root,"mac");
	cJSON * sn_obj = cJSON_GetObjectItem(root,"sn");
	cJSON * did_obj = cJSON_GetObjectItem(root,"did");
	cJSON * configHex_obj = cJSON_GetObjectItem(root,"configHex");


	unsigned char * temp_ptr = &output_buf[START_ADDR];

	//device ID
	if( did_obj != NULL){
		printf("did : %s \n",did_obj->valuestring);

		strcpy(temp_ptr, did_obj->valuestring);

	}else {
		printf("did is not find\n");
	}

	//sn
	temp_ptr += DATA_SECTION;
	if( sn_obj != NULL){
		printf("sn : %s \n",sn_obj->valuestring);

		strcpy(temp_ptr, sn_obj->valuestring);

	}else {
		printf("did is not find\n");
	}

	//MAC
	temp_ptr += DATA_SECTION;
	if (mac_obj != NULL ){

		printf("mac : %s \n",mac_obj->valuestring);
		int mac_length = 0;
		int * mac_data = stringToInt(mac_obj->valuestring, &mac_length, ":");

		for (int i = 0; i < mac_length; i++){


			temp_ptr[i] = mac_data[i];
		}

		free(mac_data);

	}else {
		printf("mac is not find\n");
	}



	//config Hex
	int hexLength = 0;
	temp_ptr += DATA_SECTION;
	if( configHex_obj != NULL){
		printf("config Hex : %s \n",configHex_obj->valuestring);

		
		char * configBytes = stringToBytes(configHex_obj->valuestring, &hexLength);

		/*for(int i = 0 ; i < hexLength; i++)
		{
			printf("\t%x\t", configBytes[i]);

		}
		printf("\n");
		printf("%s:hl===%d\n",__FUNCTION__, hexLength);*/
		memcpy(temp_ptr, configBytes, hexLength);
		free(configBytes);

	}else {
		printf("config Hex is not find\n");
	}


	temp_ptr += (hexLength);
	
	while( temp_ptr !=  &output_buf[OUTPUT_FILE_SIZE - 1]){
		*temp_ptr = (char)(rand()%0xFF);
		temp_ptr++;
	}





	//printf("%s:%d\n",__FUNCTION__, __LINE__);
	fwrite(output_buf, 1, OUTPUT_FILE_SIZE, output_bin);
	//printf("%s:%d\n",__FUNCTION__, __LINE__);

	fclose(output_bin);//printf("%s:%d\n",__FUNCTION__, __LINE__);
	//fclose(input_file);printf("%s:%d\n",__FUNCTION__, __LINE__);
	
	
	/*output_bin = fopen(OUTPUT_BIN_FLIE, "rb");
	
	memset(output_buf,0,OUTPUT_FILE_SIZE);
	fread(output_buf, 1, OUTPUT_FILE_SIZE, output_bin);
	
	fclose(output_bin);
	
	output_bin = fopen(OUTPUT_BIN_FLIE, "wb");
	
	fwrite(output_buf, 1, OUTPUT_FILE_SIZE, output_bin);*/
	
	
	

	//system("pause");
	
    return 0;
}













