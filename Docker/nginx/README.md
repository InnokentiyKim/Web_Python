# Docker. Задание 1. 

## Задача

По аналогии с практикой из лекции создайте свой docker image с http сервером nginx. Замените страницу приветсвия Nginx на своё (измените текст приветствия на той же странице).

## Алгоритм решения
### Последовательность действий:

1. Перейти в консоли (bash, zsh, ...) в директорию 'nginx'   

2. Собрать docker image путем ввода в консоли команды:  
`docker image build . -t my_nginx:1.0`  
3. Запустить docker контейнер из образа:  
`docker run -d -p 8080:80 my_nginx:1.0`  
4. Новая страница приветствия NGINX доступна по адресу:  
`localhost:8080`  


