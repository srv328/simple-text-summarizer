import math
from collections import Counter


def extract_top_keywords(phrases, top_n=20):
    frequency_dict = Counter()
    for phrase in phrases:
        tokens = phrase.lower().split()
        frequency_dict.update(tokens)

    return [token for token, frequency in frequency_dict.most_common(top_n)]


def segment_text_into_phrases(input_text):  # Делим текст на фрагменты
    phrase_list = []
    buffer = ""
    for character in input_text:
        buffer += character
        if character in ".!?" and (len(buffer) > 1 and not buffer[-2].isdigit()):
            phrase_list.append(buffer.strip())
            buffer = ""
    if buffer:
        phrase_list.append(buffer.strip())
    return phrase_list


def simple_summary(input_text, proportion, details=False):
    # Определение размера выходного текста
    fraction = proportion / 100

    # Разбиение текста на предложения
    phrases = segment_text_into_phrases(input_text)

    # Получение всех ключевых слов
    word_collection = []
    for phrase in phrases:
        word_collection.extend(phrase.lower().split())
    key_tokens = extract_top_keywords(phrases, top_n=20)

    # Подсчет частоты появления каждого слова
    token_frequency = {}
    for token in word_collection:
        token_frequency[token] = token_frequency.get(token, 0) + 1

    # Сортировка по частоте
    sorted_token_list = sorted(token_frequency.items(), key=lambda x: x[1], reverse=True)
    total_tokens = len(sorted_token_list)

    # Применение закона Зипфа
    proc_important_tokens = []
    for i, (token, frequency) in enumerate(sorted_token_list, 1):
        expected_frequency = 1 / (i * math.log(total_tokens))
        if frequency >= expected_frequency:
            proc_important_tokens.append(token)
        else:
            break

    # Оценка значимости каждого ключевого слова
    max_frequency = max(token_frequency.values())
    token_relevance = {}
    for token in proc_important_tokens:
        relevance_score = token_frequency[token] / max_frequency
        token_relevance[token] = relevance_score

    # Оценка важности каждого предложения
    phrase_scores = []
    for phrase in phrases:
        phrase_tokens = phrase.lower().split()
        token_count = len(phrase_tokens)
        if token_count > 0:
            score_sum = sum(token_relevance.get(token, 0) for token in phrase_tokens)
            average_score = score_sum / token_count

            # Повышающий коэффициент для важных фраз
            if any(marker in phrase.lower() for marker in ["вывод", "необходимо подчеркнуть"]):
                average_score *= 1.5

            # Снижающий коэффициент для вопросов
            if phrase.strip().endswith('?'):
                average_score *= 0.8

            phrase_scores.append((phrase, average_score))

    # Фильтрация слишком коротких фраз
    minimum_length = 5  # Минимум слов в предложении
    phrase_scores = [(p, s) for p, s in phrase_scores if len(p.split()) >= minimum_length]

    # Сохранение n% лучших предложений
    phrase_scores_sorted = sorted(phrase_scores, key=lambda x: x[1], reverse=True)
    top_phrases_to_keep = int(len(phrases) * fraction)
    selected_phrases = phrase_scores_sorted[:top_phrases_to_keep]

    # Возвращение предложений в исходном порядке
    selected_phrases.sort(key=lambda x: phrases.index(x[0]))

    # Формирование итогового текста
    final_summary = ' '.join(phrase for phrase, _ in selected_phrases)

    if details:
        return final_summary, phrases, proc_important_tokens, token_relevance, phrase_scores
    else:
        return final_summary


def rank_texts_by_keywords(content_list, keywords_list):
    ranking = []
    for content in content_list:
        keyword_match_count = sum(1 for word in keywords_list if word in content.lower())
        ranking.append((content, keyword_match_count))
    return [content for content, _ in sorted(ranking, key=lambda x: x[1], reverse=True)]


if __name__ == "__main__":
    documents = [
        """
        Базовые задачи - это задачи, качественное решение которых невозможно получить без компьютерного 
        семантического анализа текста.
        """,

        """
        Распознавание текстов. Под распознаванием текстов понимается построение полной синтаксической структуры 
        предложений, адекватной его семантической структуре. Другими словами, осуществляется перевод с естественного 
        языка на формальный семантический язык, с которым способен оперировать компьютер. В чистом виде такая 
        возможность может быть полезна во всех задачах, где требуется распознавание текстов или речи. 
        Наиболее распространенными являются задачи голосового управления и оптического распознавания текстов. 
        Использование полноценного анализатора текстов способно значительно поднять качество распознавания 
        в этих задачах. В особенности это касается распознавания речи, где до сих пор существуют значительные 
        трудности при различении похоже звучащих слов. Механизм корректного выбора альтернатив с учетом смысла 
        способен значительно (в несколько раз) сократить неоднозначность.
        """,

        """
        Поиск документов. Исходной основой для поиска обычно являются большие массивы неструктурированных или 
        слабоструктурированных текстов на естественном языке. Массив текстов предварительно индексируется. 
        Индекс содержит соответствия между некими базовыми сущностями, использующимися для поиска и документами 
        их содержащими. В простейшем случае этими сущностями являются слова (или словоформы). В более развитых 
        вариантах это может быть тема текста (документа), фрагменты фраз и утверждений или целые фразы или предложения. 
        Возможен также поиск документов "похожих на данный". Качественный поиск по теме документа или степени похожести 
        на данный документ требует умения правильно определять тематику документа. Индексы могут строится как 
        автоматически, так и вручную. Автоматически строятся, как правило, только индексы на основе слов 
        (и в очень ограниченном виде на основе определения тематики текста). 
        SemLP-технология позволяет строить индексы любого типа, что дает возможность проводить очень точный поиск. 
        Для локальных поисковых систем достижима полнота и релевантность порядка 90-95% и более.
        """,

        """
        Классификация и рубрикация документов, определение тематики документов. Несмотря на внешнюю простоту задачи 
        рубрикации и определения тематики документов являются очень сложными в реализации. На основе только ключевых 
        слов или синтаксической структуры простых словосочетаний удовлетворительно решить задачу нельзя. Фрагментарное 
        использование общих семантических классов также принципиально ничего не меняет. Существующие системы 
        обеспечивают точность классификации (а значит, и определения тематики) по сравнению с человеческой оценкой: 
        без использования заранее заданных классов - порядка 10%, с использованием заранее заданных классов и 
        настройкой на тематику текстов - до 60%. Другими словами, существующие системы не обеспечивают 
        удовлетворительного решения этих задач. Рубрикация на основе SemLP-технология способна обеспечить 
        точность без использования заранее заданных классов порядка 90-95% и при настройкой на тематику текстов 
        близко к 100%. Предлагаемая система позволяет осуществлять гибкую настройку глубины и направления 
        классификации и рубрикации в соответствии с требованиями заказчика. Большинство задач такого рода может 
        быть решено с помощью системы на уровне, близком к тому, который доступен только эксперту.
        """,

        """
        Синтез текстов. В узком смысле под синтезом текстов здесь понимается построение фраз и предложений на 
        естественном языке по записям на формальном языке. К порождаемым фразам может предъявляться или не 
        предъявляться требование стилистической корректности, однако они в любом случае не должны содержать 
        смысловых и грамматических ошибок. В систему заложены возможности, позволяющие проводить синтез текста, 
        в том числе, и стилистически корректного. В случае полномасштабного синтеза, это, однако, является 
        трудоемкой задачей, поскольку требует некоторой модификации словарей. В существующем виде возможен синтез 
        простых двух- трех-словных словосочетаний, не всегда стилистически корректных. Эта возможность может быть 
        очень полезна при аннотировании документов, краткой характеризации тем документов и т.п.
        """,

        """
        Проверка корректности текстов. Поскольку анализатор производит полный разбор предложений, с его помощью можно 
        проверять грамматическую корректность текстов. Уровень ошибок анализатора (корректных сочетаний слов и фраз, 
        которые анализатор принимает за ошибочные) на данный момент составляет от 2% до 5%. Однако, примерно в половине 
        случаев такие употребления являются пограничными: это либо слишком сложные обороты, либо слишком неоднозначные, 
        либо редко употребляемые. Уровень некорректных употреблений, которые допускает текущая версия анализатора, в 
        несколько раз выше, поскольку он был ориентирован на работу с правильными предложениями и специальная задача 
        поиска ошибок не ставилась. Модификация анализатора с целью диагностики ошибок может быть выполнена достаточно 
        легко. В целом, система способна обеспечить качественно более высокий уровень проверки корректности текстов, 
        чем существующие автоматические корректоры.
        """,

        """
        Построение тезаурусов и онтологий. Создание тезаурусов и онтологий до сих пор остается крайне сложной 
        и трудоемкой работой. Степень автоматизации этого процесса очень низка. По сути дела, все определения 
        создаются вручную. Автоматически может проверяться лишь согласованность накопленных определений. Альтернативой 
        мог бы быть подход, когда определения понятий создаются по существующим текстам с такими описаниями 
        (энциклопедии, учебники, справочники), а затем, при необходимости, корректируются в процессе диалога с 
        экспертом. Для реализации такого подхода необходимо уметь проводить подробный анализ семантики текстов. 
        Текущая реализация анализатора текста в рамках SemLP-технология обеспечивает детализацию семантических 
        описаний достаточную для создания определений в базе знаний. На основе дальнейших преобразований и логического 
        вывода в базе знаний возможно формирование определений понятий и ситуаций для тезаурусов и онтологий.
        """,

        """
        Автоматическое реферирование и аннотирование. Суть аннотирования (реферирования) текста заключается 
        в формировании краткого описания основных тем текста. Существует два разных подхода к аннотированию. 
        В первом случае выявляется небольшое количество предложений, существующих в тексте, которые наиболее 
        полно отражают основные темы текста. Дополнительно часто выделяются ключевые слова. Во втором случае 
        основные темы текста выявляются как смыслы, и уже эти смыслы выражаются новыми предложениями, новым 
        текстом. Второй вариант в большинстве случаев значительно более предпочтителен, но он и значительно сложнее. 
        Все современные системы аннотирования/реферирования основаны на первом варианте. SemLP-технология позволяет 
        реализовать второй вариант в ограниченном виде: автоматический синтез коротких (в несколько слов) простых фраз 
        или предложений. В целом, задача аннотирования включает определение тематики документов, выделение ключевых 
        (по темам) слов и фраз с учетом смысла, поиск предложений, содержащих ключевые слова и фразы, и синтез на этой 
        основе фраз и предложений, отражающих основные темы текста.
        """
    ]

    summary_percentage = 50
    document_summaries = [simple_summary(doc, summary_percentage) for doc in documents]

    keyword_collection = set()
    for doc in documents:
        _, _, important_tokens, _, _ = simple_summary(doc, summary_percentage, details=True)
        keyword_collection.update(important_tokens)

    ranked_documents = rank_texts_by_keywords(document_summaries, list(keyword_collection))

    print("Ранжированные тексты по ключевым словам:")
    for index, doc in enumerate(ranked_documents, 1):
        print(f"\nТекст {index}:")
        print(f"\t\t{doc}")
