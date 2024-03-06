# hasql-v1

Кодогенератор клиентского SDK для языка Haskell. Опирается на библиотеку ["hasql"](https://hackage.haskell.org/package/hasql).

Производит библиотеку, предоставляющую все запросы в проекте в виде объявлений [`Statement`](https://hackage.haskell.org/package/hasql-1.6.4.1/docs/Hasql-Statement.html) с уже осуществлённым мэпингом и структурами данных для параметров и результатов, специфичными для каждого запроса.

## Поддерживаемые структуры данных

### Примитивные типы

Таблица поддерживаемых примитивных типов данных Postgres в параметрах и результатах запросов:

| Тип Postgres | В параметрах | В результатах |
| - | - | - |
| bool | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| bytea | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| char | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| cidr | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| date | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| datemultirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| daterange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| float4 | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| float8 | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| inet | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| int2 | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| int4 | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| int4multirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int4range | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int8 | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| int8multirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int8range | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| interval | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| json | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| jsonb | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| macaddr | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| macaddr8 | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| money | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| numeric | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| nummultirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| numrange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| text | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| time | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| timestamp | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| timestamptz | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| timetz | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| tsmultirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| tsrange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| tstzmultirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| tstzrange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| uuid | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| xml | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |

### Массивы

| Тип элемента массива Postgres | В параметрах | В результатах |
| - | - | - |
| Примитив | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| Композитный тип | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| Энумерация | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |

### Энумерации

<span style="color:green">:material-check-all:</span>
Поддерживаются как в параметрах так и в результатах.

### Композитные типы

<span style="color:green">:material-check-all:</span>
Поддерживаются как в параметрах так и в результатах.

## Версионирование библиотек

Так как в Haskell применяется конвенция версионирования [PVP](https://pvp.haskell.org/), а не [SemVer](https://semver.org/), кодогенератор приводит значение `version` из файла конфигурации к PVP путём подставления префикса `0.`. Например, версия `1.0.0` превратится в `0.1.0.0`.
