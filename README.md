This program is designed for remote management of the Perfect World server.
Main features:
1) Uploading files to the server. The download paths are described in the file serverlist.txt
The path must include the full path to the file, including the file name. 
   If the file needs to be copied to multiple locations, for example, element.data, this is necessary. 
   specify it in a separate line.
   /home/gamed/config/elements.data # server file
   /patcher/files/new/element/data/elements.data # file for the update server
2) Start/Stop the server.
3) Start creating updates using CPW
For the program to work correctly, copy the edited files to the "new" folder.
The program is able to distinguish whether a file has been changed or not.
The program expects the cpw server to be located in the /patcher/ folder at the root of the file system.
The program uses the Ubuntu 14.04 command set
4) Allows you to launch dungeons, as well as displays their status.
Create the settings.ini file in the program folder.
[Settings]
address = 127.0.0.1
username = root
password = qwerty
port = 22
[Inst]
gs01 = World
is61 = Ferry of souls
is69 = Light cave
is01 = GTZ
is05 = 19 - People
is06 = 19 - Zoo
is07 = 19 - Sidy
id other dungeons can be found online.
!!! The file must be saved in the encoding of your OS, for example, Win-1251
Replace the address and credentials with yours, with the rights to perform operations.

Данная программа предназначена для удаленного управления сервером Perfect World.
Основные возможности:
1) Загрузка файлов на сервер. Пути для загрузки описываються в файле serverlist.txt
   Путь должен включать в себя полный путь к файлу, включая имя файла. 
   Если файл необходимо копировать в несколько мест, например element.data - это необходимо 
   указать в отдельной строкой.
   /home/gamed/config/elements.data # файл сервера
   /patcher/files/new/element/data/elements.data # файл для сервера обновлений
2) Запуск / Остановка сервера.
3) Запуск создания обновлений при помощи CPW
Для корректной работы программы в папку "new" скопируйте редактируемые файлы.
Программа умеет различать был изменен файл или нет.
Программа ожидает что сервер cpw находится в папке /patcher/ в корне файловой системы.
Программа использует набор команд Ubuntu 14.04
4) Позволяет запускать данжи, а так же отображает их статус.
Создайте в папке с программой файл settings.ini
[Settings]
address = 127.0.0.1
username = root
password = qwerty
port = 22
[Inst]
gs01 = Мир
is61 = Переправа душ
is69 = Светлая пещера
is01 = ГТЗ
is05 = 19 - Люди
is06 = 19 - Зоо
is07 = 19 - Сиды
id других данжей можно найти в сети.
!!! Файл необходимо сохранять в кодировке вашей OS, Например Win-1251
Адрес и учетные данные замените на Ваши, с правами на выполнение операций.
