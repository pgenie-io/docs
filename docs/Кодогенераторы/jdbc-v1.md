# jdbc-v1

Кодогенератор клиентского SDK для языка Java, опирающийся на JDBC.

Производит библиотеку, предоставляющую все запросы в проекте в виде класса-декоратора, расширяющего предоставленное соединение JDBC операциями исполнения запросов с уже осуществлённым мэпингом и структурами данных для параметров и результатов, специфичными для каждого запроса.

Вы можете использовать эту библиотеку в любом другом языке, исполняемом на платформе JVM. Например, в Scala, Kotlin, Clojure.

## Поддерживаемые структуры данных

### Примитивные типы

Таблица поддерживаемых примитивных типов данных Postgres в параметрах и результатах запросов:

| Тип Postgres | В параметрах | В результатах |
| - | - | - |
| bool | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| bytea | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| date | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| char | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| cidr | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| date | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| datemultirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| daterange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| float4 | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| float8 | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| inet | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int2 | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| int4 | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| int4multirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int4range | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int8 | <span style="color:green">:material-check:</span> | <span style="color:green">:material-check:</span> |
| int8multirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int8range | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| interval | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| json | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| jsonb | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
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
| bool | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| bytea | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| date | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| char | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| cidr | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| date | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| datemultirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| daterange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| float4 | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| float8 | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| inet | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int2 | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| int4 | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| int4multirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int4range | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int8 | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| int8multirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| int8range | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| interval | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| json | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| jsonb | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| macaddr | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| macaddr8 | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| money | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| numeric | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| nummultirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| numrange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| text | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| time | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| timestamp | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| timestamptz | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| timetz | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| tsmultirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| tsrange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| tstzmultirange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| tstzrange | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |
| uuid | <span style="color:green">:material-check:</span> | <span style="color:firebrick">:material-close:</span> |
| xml | <span style="color:firebrick">:material-close:</span> | <span style="color:firebrick">:material-close:</span> |


Поддержка массивов в результатах находится в разработке.

### Энумерации

<span style="color:firebrick">:material-close:</span>
В разработке.

### Композитные типы

<span style="color:firebrick">:material-close:</span>
В разработке.
