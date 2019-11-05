#include <sys/types.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>
#include <fcntl.h>

#define BUFFERSIZE 512
#define BYTE 4
void Client(int fd_cread, int fd_cwrite);
void Server(int fd_sread, int fd_swrite);
char success[]="Input_write_success";

int main(int argc, char *argv[])
{
	// 0 = read, 1 = write
	int fd_1[2], fd_2[2]; 

	pid_t pid;
	
	if(pipe(fd_1) == -1 || pipe(fd_2) == -1){
	  printf("Pipe create Failed\n");
	  return 1;
	}else{
		printf("Pipe cretae Success/n");
	}



	pid=fork();
	
	while(1){
 	  if(pid <0){
	    fprintf(stderr, "Server access Failed");
	    exit(0);
	  }
	  //child process, server
	  else if (pid ==0){
	    close(fd_1[0]);//read close
	    close(fd_2[1]);//write close
	    Server(fd_2[0],fd_1[1]);
 	  }
 	  //parent process, client 
	  else{
	   close(fd_1[1]);//write close
	   close(fd_2[0]);//read close
	   Client(fd_1[0], fd_2[1]);	
	   sleep(1);
	  }
	}

}




void Client(int fd_read, int fd_write)
{

  int Read_byte=0, len;
  char Write_file[BUFFERSIZE]="\0";
  char Read_file[BUFFERSIZE]="\0";

  printf("name  type  readnum   changewrite\n ");
  printf("type : r = read, w = write\n");
  printf("example: aaa.txt r  3 kkk\n ");
  printf("input text >>>>");

  //input text
  fgets(Write_file,BUFFERSIZE,stdin);
  //transfor to server
  write(fd_write,Write_file,BUFFERSIZE);
  Write_file[0]='\0';
  
  len=read(fd_read, Read_file,BUFFERSIZE);
  printf("result: %s\n",Read_file);
 
}




void Server(int fd_read,int fd_write)
{
	//len = contents to recive
    int readbyte, len=0, i,j;

    char buffer[BUFFERSIZE];
    char filename[BUFFERSIZE];
    char filedata[BUFFERSIZE];
    char filetype;
	char byte[BYTE];
	char readbuf[BUFFERSIZE];

    FILE *fp;


    len=read(fd_read, buffer, BUFFERSIZE); 
    buffer[len]='\0';

    for(i=0,j=0;buffer[j] !=' ';i++,j++){
    	filename[i]=buffer[j];
    }

   filename[i]='\0';

   j++;

   filetype=buffer[j];

	for(i=0,j=j+2;buffer[j]!=' ';i++,j++){
		byte[i]=buffer[j];
	}
	
	readbyte=atoi(byte);
   for(i=0,j=j+1;buffer[j] != '\n'; i++, j++){
     filedata[i]=buffer[j];
   }
   filedata[i]='\0';

   printf("server create clear\n");
  
   if(filetype=='w'){
	printf("write start\n");
	fp=fopen(filename,"r+");
	
	// not exist file
	if(fp==NULL){
		printf("not exist file\n");
		exit(0);
	}
	
	fprintf(fp,"%s",filedata);	
	write(fd_write,success,strlen(success));
	fclose(fp);
   	}

  	if(filetype=='r'){
	printf("file read\n");
	fp=fopen(filename,"r");
	if(fp==NULL){
		printf("not exist file\n");
		exit(0);
	}
	fgets(readbuf,readbyte+1,fp);
	write(fd_write,readbuf,readbyte);
	//puts(readbuf);
	fclose(fp);
	
  }
}
