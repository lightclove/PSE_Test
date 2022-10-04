__author__ = 'Venkatesh-Prasad Ranganath'
# Python -- v3.8
# https://medium.com/@rvprasad/performance-of-system-v-style-shared-memory-support-in-python-3-8-d7a7d1b1fb96
# Performance of System V Style Shared Memory Support in Python 3.8
'''
Это изменение представляет новый менеджер multiprocessing.managers.SharedMemoryManager, который позволяет менеджеру
получать доступ к этой общей памяти. Изменение также представляет новый пакет с именем multiprocessing.shared_memory.
Этот пакет содержит классы SharedMemory и ShareableList.
В то время как первый класс предоставляет «сырой» доступ к разделяемой памяти,
последний предоставляет доступ к разделяемой памяти, абстрагируя ее как список в Python, но с некоторыми ограничениями.
Чтобы оценить выигрыш в производительности от совместной памяти, выполняется следующий простой тест -
создается список целых чисел и удваивется каждое целое число в списке параллельно,
разбивая его на части и обрабатывая каждый кусок параллельно.
'''
from multiprocessing import Process, Queue, managers
import time


def worker(id, data, queue, *args):
    tmp1 = time.time()
    if args:
        for i in range(args[0], args[1]):
            data[i] *= 2
        queue.put(0)
    else:
        queue.put([data[x]*2 for x in range(len(data))])


def without_shared_memory():
    print("Without shared memory")
    iterations = 6
    for i in range(2, 6):
        start_time = time.time()
        num_procs = 4
        data = list(range(1, 10**i))
        chunk_size = len(data) // num_procs
        for _ in range(iterations):
            queue = Queue()
            procs = [Process(target=worker,
                             args=(j, data[j*chunk_size:(j+1)*chunk_size],
                                   queue))
                     for j in range(num_procs)]
            for p in procs:
                p.start()

            tmp = 0
            for _ in range(num_procs):
                tmp += sum(queue.get())

            for p in procs:
                p.join()
                p.close()

        end_time = time.time()
        secs_per_iteration = (end_time - start_time) / iterations
        print("data {0:>10,} ints : {1:>6.6f} secs per iteration"
              .format(len(data), secs_per_iteration))


def with_shared_memory():
    print("With shared memory")
    iterations = 6
    for i in range(2, 6):
        num_procs = 4
        with managers.SharedMemoryManager() as smm:
            start_time = time.time()
            data = smm.ShareableList(range(1, 10**i))
            chunk_size = len(data) // num_procs
            for _ in range(iterations):
                queue = Queue()
                procs = [Process(target=worker,
                                 args=(j, data, queue, j*chunk_size,
                                       (j+1)*chunk_size))
                         for j in range(num_procs)]
                for p in procs:
                    p.start()

                for _ in range(num_procs):
                    queue.get()
                tmp = sum(data)

                for p in procs:
                    p.join()
                    p.close()

            end_time = time.time()
            secs_per_iteration = (end_time - start_time) / iterations
            print("data {0:>10,} ints : {1:>6.6f} secs per iteration"
                  .format(len(data), secs_per_iteration))

'''
Чтобы понять преимущества, тест был выполнен как с обычными (не разделяемыми) списками Python, так и с общими списками.
Тест проводился на 8-ядерном 64-ГБ ОЗУ Linux, работающем под управлением Pop OS (Ubuntu) 19.10 и Python 3.8.
'''
without_shared_memory()
with_shared_memory()