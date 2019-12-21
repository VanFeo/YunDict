--建立dict数据库
CREATE DATABASE dict CHARSET='utf8'
--建立单词表
CREATE TABLE words(
    id int primary key auto_increment,
    word varchar(50) not null,
    mean text)
--建立用户表
CREATE TABLE user (
    id int primary key auto_increment,
    name char(20) not null,
    password char(64) not null)
--建立关系表(user 与 words 多对多)
CREATE TABLE user_words (
    id int primary key auto_increment,
    uid int, wid int,
    time datetime default now(),
    CONSTRAINT user_fk FOREIGN KEY(uid) REFERENCES user(id),
    CONSTRAINT words_fk FOREIGN KEY(wid) REFERENCES words(id))
--添加索引
CREATE Index word_index on words(word)
--建立新的关系表产生历史记录
SELECT word, h.time FROM words INNER JOIN
(SELECT wid, time FROM user_words WHERE uid =
(SELECT id FROM user WHERE name = 'Feo') ORDER BY time DESC LIMIT 10)
as h ON words.id = h.wid