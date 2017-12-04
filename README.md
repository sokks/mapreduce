# MapReduce
Примеры использования фреймворка mincemeatpy.

## Богатство языка
По субтитрам сериала Саус парк (сезоны 1- 18) находит language diversity персонажей.  
Ввод: ./southpark/All-seasons.csv  
Вывод: lang_divers.csv

```console
# if needed run pip package installations with prepare
$ make prepare
$ make task1
```

## Обратный индекс с частотностью
По нескольким файлам с рассказами из серии Приключения Шерлока Холмса строит обратный индекс.  
Ввод: ./sherlock/*  
Вывод: inv_index.csv

```console
$ make task2
```

## Произведение матриц
Перемножаем две квадратные матрицы из одного csv-файла и дописывает результат в конец.  
Ввод: ./matricies/AB.csv  
Вывод: AB_C.csv

```console
$ make gen
$ make task3
```