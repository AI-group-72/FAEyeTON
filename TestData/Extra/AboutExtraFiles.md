О преимпульсном ингибировании

При разработке библиотеки была рассмотрена возможность использования данных о преимпульсном ингибировании для определения утомления. В рамках работы, полученные результаты были признаны неудовлетворительными, однако была оставлена возможность работы с разработанным функционалом.

В приложении dataGather.exe, или же при запуске визуального интерфейса в классе DataGather, присутствуют кнопка «Выбрать файлы PPI».

Кнопка «Выбрать файлы PPI» открывает окно для выбора файлов, содержащих информацию о преимпульсном ингибировании (сокращение от английского «prepulse inhibition», PPI) оператора. Эти файлы собираются с помощью стороннего приложения и специального оборудования в то же время, как и запись данных с окулографа (являются опциональным). Данные о PPI вставляются в общую таблицу данных автоматически, путем поиска соответствия в названии файлов. 

!! Для того, чтобы автоматическая вставка сработала, названия файлов с данными о преимпульсном ингибировании должны соответствовать названиям файлов в выходной таблице (за исключением расширения). !!

Порядок действия такой - сначала обычный расчёт характеристик во выбранному методу. В результате формируется выходной файл "*.csv", внутри которого содержится таблица. Первый столбец в таблице - 'File', содержит наименования файлов с записями окулографа, обработанных программой. При нажатии кнопки "Выбрать файлы PPI" нужно выбрать набор файлов, рассчитанные показатели PPI автоматически добавятся в выходной файл, при необходимости дополнительно создав нужные столбцы. В момент работы программы, выходной файл должен быть закрыт.

Для демонстрации работы этого функционала, в папке «Extra» присутствуют 5 файлов-примеров, имеющих расширение «.txt», и соответствующих записями из папки «Fresh»

О файлах pupillabs

В рамках исследовательской работы был разработан функционал использования внешних алгоритмов определения глазодвигательных стратегий. 
Для использования такого алгоритма, необходимо в пользовательском интерфейсе (приложение dataGather.exe, или же запуск визуального интерфейса в классе DataGather) нужно нажать кнопку «Файлы pupillabs». Далее последовательно откроются два диалоговых окна выбора файлов, где в первом нужно выбрать сами файлы с записями полученными от окулографа, а во втором – файлы с размеченными стратегиями. Количество выбранных файлов в первом и втором окне должно совпадать, соответствие между файлами записей и файлами с размеченными стратегиями строится по их порядку. Т.Е. не обязательно полное совпадение названий, но необходим одинаковый алфавитный порядок файлов.

Для демонстрации работы этого функционала, в папке «Extra» присутствуют 5 файлов-примеров, имеющих расширение «.csv», и соответствующих записями из папки «Fresh»



About preimpulse inhibition

During the development of the library, the possibility of using data on preimpulse inhibition to determine fatigue was considered. As part of the work, the results obtained were considered unsatisfactory, but the possibility of working with the developed functionality was left.

In the application dataGather.exe or, when launching the visual interface in the DataGather class, there is a button "Выбрать файлы PPI".

The "Выбрать файлы PPI" button opens a window for selecting files containing information about pre-pulse inhibition (short for "pulse inhibition", PPI) of the operator. These files are collected using a third-party application and special equipment at the same time as recording data from an oculoscope (optional). The PPI data is inserted into the general data table automatically by searching for a match in the file names.

!! In order for the automatic insertion to work, the names of the files with pre-pulse inhibition data must match the names of the files in the output table (with the exception of the extension). !!

The procedure is as follows: first, the usual calculation of characteristics according to the selected method. As a result, the output file "*.csv" is generated, which contains a table inside. The first column in the table is 'File', which contains the names of files with oculograph records processed by the program. When you click the "Выбрать файлы PPI" button, you need to select a set of files, the calculated PPI indicators will be automatically added to the output file, if necessary, additionally creating the necessary columns. When the program is running, the output file must be closed.

To demonstrate the operation of this functionality, there are 5 sample files in the "Extra" folder with the ".txt" extension, and corresponding entries from the "Fresh" folder

About pupillabs files

As part of the research work, the functionality of using external algorithms for determining oculomotor strategies was developed.
To use such an algorithm, it is necessary in the user interface (application dataGather.exe , or launching the visual interface in the DataGather class) you need to click the "Файлы pupillabs" button. Next, two file selection dialog boxes will open sequentially, where in the first you need to select the files themselves with the recordings received from the oculoscope, and in the second – files with marked strategies. The number of selected files in the first and second windows must match, the correspondence between the record files and the files with marked-up strategies is based on their order. I.e. The names do not necessarily match completely, but the same alphabetical order of the files is required.

To demonstrate the operation of this functionality, there are 5 sample files in the "Extra" folder with the ".csv" extension, and corresponding entries from the "Fresh" folder
