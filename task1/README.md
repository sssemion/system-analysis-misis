# Задание 1

Парсит дерево из json

пример запуска:
```bash
python3 task1/task.py task1/tree.json
```

пример входного файла:
```json
{
    "nodes":{
        "level1_1": ["level2"],
        "root": ["level1_1", "level1_2"],
        "level2": ["level3"],
        "level3": [],
        "level1_2": []
    }
}
```

пример вывода дерева через `print_tree`:
```
root
         level1_1
                 level2
                         level3
         level1_2
```