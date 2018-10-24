#include <stdio.h>
#include <stdlib.h>
#include <io.h>

#define MAX_FILE_NUMBER         500

#define FILE_START_MAGIC		0xDEAD

typedef struct fileHead{
	unsigned short magic;
	unsigned short name_len;
	unsigned int file_len;

}fileHead;

char * resPackName = "res_pack.bin";


int main(int argc, char ** argv)
{
	struct _finddata_t fileinfo;
    //保存文件句柄
    long fHandle;
    int count = 0;

    char default_path[] = "./data";
    char * path = default_path;

    if(argc == 2){
        path = argv[1];
        printf("path = %s\n", path);
    }

    char full_path[1024]= {0};
    char full_name[1024]= {0};

    sprintf(full_path, "%s/*", path);

	FILE * in_fd = NULL;
	FILE * out_fd = NULL;

	out_fd = fopen(resPackName, "wb");

    if( (fHandle=_findfirst( full_path, &fileinfo )) == -1L )
    {
        printf( "no file\n");
        goto exit;
    }
    else{
        do{

			if((strcmp(fileinfo.name, ".")==0 ) || (strcmp(fileinfo.name, "..")==0 ))
			//if((strcpy(fileinfo.name, ".")==0 ))
			{


			}else{

				count ++;

				printf( "file :%s,size : %d\n", fileinfo.name,fileinfo.size);
				//store_fileToken(fileinfo.name, fileinfo.size, path,count);

				fileHead temp_head = {0};
				temp_head.magic = FILE_START_MAGIC;
				temp_head.name_len = strlen(fileinfo.name) + 1;
				temp_head.file_len = fileinfo.size;

				sprintf(full_name, "%s/%s", path, fileinfo.name);
				printf("full_name = %s\n",full_name);
				in_fd = fopen(full_name, "rb");
				if(in_fd == NULL)
                {
                    printf("file open failed\n");
                    while(1);
                }
				char *file_buf = malloc(fileinfo.size);
				int read_size = fread( file_buf, 1, fileinfo.size, in_fd);
                printf("read_size = %d\n",read_size);

				fwrite( &temp_head, 1, sizeof(fileHead), out_fd);
				fwrite( fileinfo.name, 1, temp_head.name_len, out_fd);
				fwrite( file_buf, 1, temp_head.file_len, out_fd);

				fclose(in_fd);
				free(file_buf);
			}



        }while( _findnext(fHandle,&fileinfo)==0);
    }
    //关闭文件
    _findclose( fHandle );


	fclose(out_fd);



exit:

	system("pause");
	return 0;
}


















