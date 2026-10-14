# Отчёт по обновлению Anki-карточек

Формат файлов: TSV, 3 поля: Front, Back, Tags. В начале файлов оставлены Anki import hints: `#separator:tab`, `#html:true`, `#tags column:3`.

## Итоговые количества

- verbs: 57 карточек
- nouns: 97 карточек
- others: 43 карточек
- phrases: 168 карточек

## Что сделано

- Объединил исходные TSV и `Словарь_v2.ods`.
- Убрал дубли по нормализованному испанскому ответу, включая варианты без артиклей: например `la cama` и `cama` считаются дублем.
- Перенёс предложения и цельные фразы из `otros.tsv` в отдельный файл фраз; в `otros` оставил прилагательные, наречия, союзы, местоимения, предлоги и т.п.
- Добавил deck-теги ко всем карточкам: `deck_verbos`, `deck_sustantivos`, `deck_otros`, `deck_frases_oraciones`.
- Новые строки из ODS помечены `source_ods`; новые тренировочные фразы помечены `added_practice`.

## Места, где не хватило информации или нужен контекст

- **nouns — nerd → “mateo/norio”:** Не добавлено: в словаре выглядит как ошибка; для “nerd” по контексту могут быть friki / empollón(a), но это уже регионально и стилистически разное.
- **nouns — tap → “pulse”:** Не добавлено: “pulse” не переводит кран; карточка “water tap = la llave de agua” уже была в исходной лексике.
- **nouns — torture:** Не добавлено: в ODS нет испанского слова; я не стал подставлять перевод без источника.
- **nouns — memorize → “acoerdar”:** Не добавлено: строка в листе существительных, а испанская форма похожа на ошибку; для “remember” уже есть acordarse de.
- **verbs — suspender/rusticate:** Добавлено с тегом needs_context: suspender не всегда “отчислить”; часто “провалить экзамен/приостановить”.
- **adjectives — high → “algo”:** Не добавлено как новое: это опечатка, правильное alto/alta уже есть.
- **particles — self? → su:** Добавлено с needs_context: su не равняется русскому “свой” во всех случаях; нужен субъект и владелец.
- **particles — still → meintras:** Добавлено как mientras с corrected_from_ods, но исходная английская подсказка “still” неточная; still обычно todavía/aún.
- **phrases — that love you → “qué te quiere”:** Не добавлено: испанская фраза не выглядит корректной без контекста; возможно имелось в виду que te quiere / ¿quién te quiere?
- **phrases — The study was undertaken by/in; It focuses on; Researchers investigated; The main finding is; It’s relevant because:** Не добавлено: в ODS нет испанского перевода.
- **HW — environment, seem, each, approximately, per, synthetic, chemicals, insects, dirty, meanwhile, throw, throw away, can, across, polluted, shower, especially, possible, long-distance, recycle, empty, reuse, packaging, separate, item:** Не добавлено: строки содержат только английский без испанского и русского.
- **phrases — nice to meet you → garbled Russian:** Испанскую формальную фразу добавил, русскую подсказку восстановил как “приятно познакомиться с вами”; исходный русский в ODS был битой раскладкой.

## Примечания к добавленным карточкам с контекстом

- `la criada` (nouns): “criada” can sound old-fashioned; “empleada doméstica” is more neutral.
- `el rescate` (nouns): Context matters: rescate can also mean rescue.
- `la pluma` (nouns): In many contexts “bolígrafo” is the everyday word for pen.
- `la taquilla` (nouns): Context decides whether this is a ticket office or a locker.
- `el billete` (nouns): For event tickets, “entrada” is also common.
- `la estampa` (nouns): The Russian “гравюра” is narrower than Spanish estampa.
- `la carta` (nouns): Carta can also mean menu/card depending on context.
- `el sol` (nouns): ODS English said “sunny”; Spanish sol is “sun”, not “sunny”.
- `el calor` (nouns): For “I am hot” use tengo calor, already in phrase cards.
- `la pista` (nouns): ODS says “record”; pista is usually track/clue/runway, not a vinyl record.
- `el estado` (nouns): ODS had plural estados; singular card is more useful.
- `la suerte` (nouns): Translation supplied by assistant because ODS row contained only Spanish.
- `suspender` (verbs): Not a universal translation for “rusticate”; for expel/rusticate use expulsar in many contexts.
- `igual` (others): Can mean equal/same, or “just like”, depending on sentence.
- `su` (others): Russian “свой” depends on the subject; Spanish su needs context.
- `mientras` (others): ODS had misspelling “meintras” and English “still”; todavía/aún = still.
- `que` (others): Use after comparatives: más alto que...
- `aquel / aquella / aquello` (others): For distant objects/ideas; ese/esa/eso is another common “that”.
- `encantado de conocerlo / encantada de conocerla` (phrases): Formal usted form; informal conocerte already existed.

## Валидация

Все итоговые TSV-строки имеют ровно 3 непустых поля: Front, Back, Tags.