#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
/*
есть два подхода: shmget и mmap. Я буду говорить о mmap, так как он более современный и гибкий,
но можно взглянуть на man shmget (или в этом уроке) если вы предпочитаете использовать инструменты старого стиля.
на mmap() функция может использоваться для выделения буферов памяти с настраиваемыми параметрами для управления доступом
и разрешениями, а также для их резервного копирования с хранилищем файловой системы, если это необходимо.

Cледующая функция создает буфер в памяти, которым процесс может поделиться со своими дочерними элементами:
*/
void* create_shared_memory(size_t size) {
  // Our memory buffer will be readable and writable:
  int protection = PROT_READ | PROT_WRITE;

  // The buffer will be shared (meaning other processes can access it), but
  // anonymous (meaning third-party processes cannot obtain an address for it),
  // so only this process and its children will be able to use it:
  int visibility = MAP_ANONYMOUS | MAP_SHARED;

  // The remaining parameters to `mmap()` are not important for this use case,
  // but the manpage for `mmap` explains their purpose.
  return mmap(NULL, size, protection, visibility, 0, 0);
}
/*
Ниже приведен пример программы, которая использует функцию, описанную выше, чтобы выделить буфер.
Родительский процесс напишет сообщение, вилку, а затем дождется, пока его дочерний элемент изменит буфер.
Оба процесса могут читать и записывать общую память.
*/
#include <string.h>
#include <unistd.h>

int main() {
  char* parent_message = "hello";  // parent process will write this message
  char* child_message = "goodbye"; // child process will then write this one

  void* shmem = create_shared_memory(128);

  memcpy(shmem, parent_message, sizeof(parent_message));

  int pid = fork();

  if (pid == 0) {
    printf("Child read: %s\n", shmem);
    memcpy(shmem, child_message, sizeof(child_message));
    printf("Child wrote: %s\n", shmem);

  } else {
    printf("Parent read: %s\n", shmem);
    sleep(1);
    printf("After 1s, parent read: %s\n", shmem);
  }
}