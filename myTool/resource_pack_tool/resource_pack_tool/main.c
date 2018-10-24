#include <stdio.h>
#include <stdlib.h>
#include <io.h>

#define MAX_FILE_NUMBER         500



typedef struct resHead{
    unsigned short num;
    unsigned short rec;
}resHead;

typedef struct resFileInfo{
    unsigned int nameOffset;
    unsigned int dataOffset;
    unsigned int dataLen;
}resFileInfo;
//name data
//file data
resHead res_head = {0};
resFileInfo file_info[MAX_FILE_NUMBER] = {0};

typedef struct resFileToken{
    int num;
    int len;
    char * name;
    char * data;
}resFileToken;

resFileToken file_token[MAX_FILE_NUMBER] = {0};

char * resPackName = "res_pack.bin";


void store_fileToken(char * name, int size, char * path, int count);

int main(int argc , char ** argv)
{
    //文件存储信息结构体
    struct _finddata_t fileinfo;
    //保存文件句柄
    long fHandle;
    int count = 0;

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
            count ++;
            printf( "找到文件:%s,文件大小：%d\n", fileinfo.name,fileinfo.size);
            store_fileToken(fileinfo.name, fileinfo.size, path,count);
        }while( _findnext(fHandle,&fileinfo)==0);
    }
    //关闭文件
    _findclose( fHandle );

    FILE * outFile = NULL;

    outFile = fopen(res_pack, "wb+");

    fseek(outFile, 0, SEEK_SET);

    res_head.num = count;

    fwrite(&res_head, 1, sizeof(res_head), outFile);

    fwrite(&file_info, sizeof(resFileToken), count, outFile);



    int i = 0;

    for(i = 0; i < count ; i++ ){

        cur_offset = ftell(outFile);



    }


exit:

    return 0;
}

void store_fileToken(char * name, int size, char * path, int count)
{
    file_token[count - 1].num = count - 1;
    file_token[count - 1].name = malloc(strlen(name) +1);
    strcpy(file_token[count - 1].name, name);

    char *full_file_name = malloc(strlen(name) + strlen(path) + 20);
    sprintf(full_file_name, "%s/%s", path, name);

    FILE * fd = NULL;

    fd = fopen(full_file_name, "rb+");

    fseek(full_file_name, 0, SEEK_END);
    file_token[count - 1].len = ftell();

    file_token[count - 1].data = malloc(file_token[count - 1].len);

    fread(file_token[count - 1].data, 1, file_token[count - 1].len, fd);

    fclose(fd);


}




























