# Database

## Table: files
| Column | Type | Extra                       | Purpose             |
|--------|------|-----------------------------|---------------------|
| id     | int  | auto increment, primary key | File id, join point |
| name   | varchar 128 | unique index         | name of the file    |
| mime   | varchar 255 |                | content type for the file |

## Table: words
| Column | Type | Extra                       | Purpose             |
|--------|------|-----------------------------|---------------------|
| id     | int  | auto increment, primary key | word id, join point |
| word   | varchar 128 | unique index         | the word itself     |

## Table: file_words
| Column  | Type | Extra                                    | Purpose             |
|---------|------|------------------------------------------|---------------------|
| file_id | int  | foreign key: files (id), primary key     | File reference      |
| word_id | int  | foreign key: words (id), primary key     | Word reference      |


