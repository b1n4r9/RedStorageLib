# RedStorageLib

Простая библиотека для запоминания уникальных данных в эксплоитах  Attack/Defense CTF

## Установка
```bash
pip3 install git+https://github.com/b1n4r9/RedStorageLib
```


## Использование хранилища

Под капотом два класса - один для файловой хранилки, другая для редиса. По дефолту пингуется редис на `127.0.0.1:6379`. Если недоступно, то используется файлик.

Файловая хранилка пока реализована криво, если несколько потоков будут писать в один файл, то данные не будут обновляться. Рекомендуется тогда использовать под каждый сплоит уникальное хранилище, например:

```python
s = Storage(filedb=f"{IP}_sploit3.txt")
```

### Примеры использования

```python
from redstorage import Storage

s = Storage('8.8.8.8', 8888)

# Хранить данные можно любого типа
s.add(b'\xca\xfe\xba\xbe', 'key') # байты
s.add('string', 'key') # строки
s.add(1337, 'key') # числа
s.add([1, 'a', '\xca'], 'key') # спиcки
s.add({2,'b', '\xfe'}, 'key') # кортежи

# Получаем новые данные
s.getNew('newstring', 'key')

# Получаем все значения по ключу
s.get('key')
```

#### Чаще всего используется следующим образом

```python
s = Storage()

users = get_users_from_some_place()

new_users = storage.getNew(users, "users")

for user in new_users:
    make_something_with_user(user)
    storage.add(user, "users")
```
