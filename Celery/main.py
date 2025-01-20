from tasks import cpu_bound
import datetime


def main():
    async_result_1 = cpu_bound.delay(1, 2)
    async_result_2 = cpu_bound.delay(2, 2)
    async_result_3 = cpu_bound.delay(3, 2)
    async_result_4 = cpu_bound.delay(4, 2)
    result_1 = async_result_1.get()
    result_2 = async_result_2.get()
    result_3 = async_result_3.get()
    result_4= async_result_4.get()
    print(result_1, result_2, result_3, result_4)


if __name__ == '__main__':
    start = datetime.datetime.now()
    main()
    end = datetime.datetime.now()
    print(end - start)
