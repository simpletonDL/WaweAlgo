Cначала нужно установить зависимости:
```shell script
pip3 install -r requirements.txt
```
Запускать нужно следующим образом:
```shell script
mpiexec --oversubscribe -n 10 python3 main.py
```
После запуска в папке results появляется новая папка с сетом изображений работы алгоритма.
Пример того, что должнополучится, находится в results/2020-05-12_03:04:49.