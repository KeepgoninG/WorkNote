#include <stdio.h>
#include <stdlib.h>
#include <io.h>
#include <ctype.h>
#include <ff.h>
#include <stdbool.h>

#define FAT_FILE_SYSTEM_SIZE            (6*1024*1024)
#define SECTOR_SIZE                     4096

#define LOG_DEBUG                       printf
#define HEX_FS_FILE_NAME                "fs_hex.ryfs"

#define RES_VERSION                     "70"


typedef unsigned int u32_t;

char fs_buf[FAT_FILE_SYSTEM_SIZE] = {0};

unsigned char work[4096];
FATFS ry_system_fs = {0};

void test_FATfs(void);
bool create_fatfs(void);
bool store_file(char * file_name,char * path);
void create_fatfs_hex_file(void );


void ry_hal_sector_read_exflash(unsigned int  sector,unsigned char  *buff, unsigned int  count)
{
    int i = 0;
    for(i = 0; i < count ; i++)
    {
        memcpy( &buff[i * SECTOR_SIZE], &fs_buf[ (i + sector) * SECTOR_SIZE ]  , SECTOR_SIZE);
    }

}

void ry_hal_sector_write_exflash(unsigned int  sector,unsigned char  *buff, unsigned int  count)
{
    int i = 0;
    for(i = 0; i < count ; i++)
    {
        memcpy( &fs_buf[ (i + sector) * SECTOR_SIZE ]  , &buff[i * SECTOR_SIZE],  SECTOR_SIZE);
    }
}

int main(int argc , char ** argv)
{
    //文件存储信息结构体
    struct _finddata_t fileinfo;
    //保存文件句柄
    long fHandle;
    //文件数记录器
    int i = 0;

    printf("%d",sizeof(int));
    printf("------------------------------------------------------------------\n");
    //test_FATfs();

    create_fatfs();
    printf("------------------------------------------------------------------\n");
    test_FATfs();

    FRESULT res = 0;
    char default_path[] = "../../data";
    char * path = default_path;

    if(argc == 2){
        path = argv[1];
        printf("path = %s\n", path);
    }

    char full_path[1024]= {0};

    sprintf(full_path, "%s/*", path);

    if( (fHandle=_findfirst( full_path, &fileinfo )) == -1L )
    {
        printf( "当前目录下没有txt文件\n");
        goto exit;
    }
    else{
        do{
            if((strcmp(fileinfo.name, ".") == 0) || (strcmp(fileinfo.name, "..") == 0))
            {
                continue;
            }
            i ++;
            printf( "找到文件:%s,文件大小：%d\n", fileinfo.name,fileinfo.size);
            store_file(fileinfo.name, path);
        }while( _findnext(fHandle,&fileinfo)==0);
    }
    //关闭文件
    _findclose( fHandle );

    printf("文件数量：%d\n",i);

    printf("------------------------------------------------------------------\n");
    create_fatfs_hex_file();
    printf("------------------------------------------------------------------\n");

exit:
    //while(1);
    system("pause");
    return 0;
}
void create_fatfs_hex_file(void )
{
    FILE * fd = NULL;

    fd = fopen(HEX_FS_FILE_NAME, "wb+");
    if(fd == NULL){
        LOG_DEBUG("--%d failed \n",__LINE__);
        return;
    }

    //fseek(fd, 0, SEEK_SET);

    int size = fwrite(&fs_buf[0] , 1,FAT_FILE_SYSTEM_SIZE,  fd);
    printf("fwrite size = %d \n", size);
    size = fwrite(RES_VERSION, 1, strlen(RES_VERSION)+1, fd);
    //size = fwrite(__TIME__, 1, strlen(__TIME__)+1, fd);
    fflush(fd);
    fclose(fd);

    printf("hex file created \n");

    return ;
}

bool create_fatfs(void)
{
    FRESULT res ;
    res = f_mount(&ry_system_fs, "", 1);
	//res = FR_NO_FILESYSTEM;

	if (res == FR_NO_FILESYSTEM) {

		res = f_mkfs("", FM_ANY| FM_SFD, 4096, work, sizeof(work));

		if (res == FR_OK) {

			res = f_mount(&ry_system_fs, "", 1);
		}
		else {
			LOG_DEBUG("file system create failed \n");
			goto exit;
		}
	}

	if (res != FR_OK) {

		LOG_DEBUG("file system mount failed \n");
		goto exit;
	}

    printf("create file system is OK ! \n");
	return true;

exit:
    return false;
}

bool store_file(char * file_name,char * path)
{
    FRESULT res = 0;

    FIL file;
    u32_t written_bytes;

    char full_name[1024] = {0};

    sprintf(full_name, "%s/%s",path, file_name);
    printf("file - %s -full - %s\n",file_name, full_name);
	res = f_open(&file, file_name, FA_CREATE_ALWAYS | FA_WRITE);
	if (res != FR_OK) {

		LOG_DEBUG("--%d failed res = %d \n",__LINE__, res);
		goto exit;
	}
    FILE * fd = NULL;

    fd = fopen(full_name, "rb");
    if(fd == NULL){
        LOG_DEBUG("--%d failed \n",__LINE__);
		goto exit;
    }

    if(fseek(fd, 0 , SEEK_END) != 0){
        LOG_DEBUG("--%d failed \n",__LINE__);
		goto exit;
    }
    int file_size = ftell(fd);
    printf("name = %s; size = %d\n",file_name, file_size);
    if(fseek(fd, 0 , SEEK_SET)!= 0){
        LOG_DEBUG("--%d failed \n",__LINE__);
		goto exit;
    }

    char *file_temp_buf = (char *)malloc(file_size);

    int rd_size = fread(file_temp_buf, 1, file_size, fd);
    printf("rd_size = %d\n", rd_size);
    res = f_write(&file, file_temp_buf, file_size, &written_bytes);
    if (res != FR_OK) {

		LOG_DEBUG("--%d failed \n",__LINE__);
		goto exit;
	}

	fclose(fd);

    res = f_close(&file);
    if (res != FR_OK) {

		LOG_DEBUG("--%d failed \n",__LINE__);
		goto exit;
	}



	return true;
exit:
    return false;
}



#if 1

unsigned char writeBuf[4096 * 3];
unsigned char testBuf[4096 * 3];

void test_FATfs(void)
{


    //ry_hal_spi_flash_init();
	u32_t written_bytes;


	FRESULT res ;

	memset(writeBuf, 0x32, sizeof(writeBuf) );

	res = f_mount(&ry_system_fs, "", 1);
	//res = FR_NO_FILESYSTEM;

	if (res == FR_NO_FILESYSTEM) {

		res = f_mkfs("", FM_ANY| FM_SFD, 4096, work, sizeof(work));

		if (res == FR_OK) {

			res = f_mount(&ry_system_fs, "", 1);
		}
		else {
			LOG_DEBUG("file system create failed \n");
			goto exit;
		}
	}

	if (res != FR_OK) {

		LOG_DEBUG("file system mount failed \n");
		goto exit;
	}

	FIL file;

	res = f_open(&file, "hello.txt", FA_CREATE_NEW | FA_WRITE);

	if (res != FR_OK) {

		LOG_DEBUG("file open failed \n");
		goto exit;
	}

	char hello_str[] = "Hello, lixueliang !\nYou are very good boy!!! \n";

	res = f_write(&file, hello_str, sizeof(hello_str), &written_bytes);
    printf("%d written_bytes = %d\n",__LINE__, written_bytes);
	if (res != FR_OK) {

		LOG_DEBUG("file write failed \n");
		goto exit;
	}

    //res = f_write(&file, writeBuf , sizeof(writeBuf), &written_bytes);
    printf("%d written_bytes = %d\n",__LINE__, written_bytes);
	if (res != FR_OK) {

		LOG_DEBUG("file write failed \n");
		goto exit;
	}

	res = f_close(&file);

	if (res != FR_OK) {

		LOG_DEBUG("file close failed \n");
		goto exit;
	}

	res = f_open(&file, "hello.txt",  FA_READ);

	if (res != FR_OK) {

		LOG_DEBUG("file open failed \n");
		goto exit;
	}

	res = f_read(&file, testBuf, 2048, &written_bytes);
    printf("testBuf = %s\n", testBuf);

    printf("%d written_bytes = %d\n",__LINE__, written_bytes);
	if (res != FR_OK) {

		LOG_DEBUG("file read failed \n");
		goto exit;
	}

	res = f_close(&file);

	if (res != FR_OK) {

		LOG_DEBUG("file close failed \n");
		goto exit;
	}


exit:

	return ;

}

#endif






