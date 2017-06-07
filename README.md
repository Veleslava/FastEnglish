# FastEnglish
Программа позволяет переводить слова в тексте. Для этого существует 4 режима:
1) word - команда позволяет перевести 1 или несколько слов
2) full - перевод всех слов в тексте, он создан для тех, кто только начинает изучение английского, но уже хочет читать большие тексты. В таком случае количество знакомых слов минимально
3) manual - так называемый ручной режим, он позволяет выбрать какие слова из текста переводить, подойдет для продолжающих, которые знают около 50% текста. Стоит отметить, что текст должен быть небольшим или содержать много повторяющихся слов, иначе отбор может быть довольно утомительным
4) smart - умный режим, он отбирает слова, которые скорее всего пользователь не знает. Сначала, слово проверяется в базе данных, если оно "гуглилось" меньше 3 раз или его нет в базе, то формируется условный корень путем удаления префиксов и суффиксов. Этот корень также проверяется в базе данных, и если встречается менее 3 слов с таким условным корнем, то исходное слово попадает в список к переводу. За основу метода берется утверждение, что "если человек знает одно слово, то он может догадаться и о значении похожего слова." Например, глагол to declare означает декларировать что-либо, а существительное declaration, как не сложно догадаться, декларацию. Недостатком режима является то, что пользователю необходимо знать значение суффиксов и префиксов. Smart-translate рекомендуются для тех, кто уверено чувствует себя в грамматике и словообразовании, но кому не хватает знания слов.
Также существует команда help, дающая краткую характеристику всем режимам. Для режимов 2-4 необходим файл с текстом в txt формате. После самого перевода создается файл в той же директории что и исходный текст. 
В итоге, пользователь получает персональный англо-русский словарь  с указанием части речи и нескольких вариантов перевода
